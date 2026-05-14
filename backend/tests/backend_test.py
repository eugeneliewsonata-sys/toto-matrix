"""HuatPick backend API tests (iteration 2).

Covers:
- Public endpoints (root, games, packages)
- Auth (register/login/me)
- Generate for pick games (6_58/6_55/6_52/6_50)
- Generate for digit games (4D/5D/6D) - NEW
- Payments checkout + status (REGRESSION: status must NOT 500 on unknown session)
"""
import os
import time
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL"):
                BASE_URL = line.strip().split("=", 1)[1].strip().strip('"')
BASE_URL = BASE_URL.rstrip("/")

EMAIL = f"tester+{int(time.time()*1000)}@huatpick.com"
PASSWORD = "lucky123"


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def auth(session):
    r = session.post(f"{BASE_URL}/api/auth/register", json={"email": EMAIL, "password": PASSWORD, "name": "Tester"})
    assert r.status_code == 200, r.text
    data = r.json()
    return {"token": data["access_token"], "user": data["user"]}


@pytest.fixture(scope="session")
def auth_headers(auth):
    return {"Authorization": f"Bearer {auth['token']}", "Content-Type": "application/json"}


# ---------- Public ----------
def test_root(session):
    r = session.get(f"{BASE_URL}/api/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_games_returns_7_with_digit_and_pick(session):
    r = session.get(f"{BASE_URL}/api/games")
    assert r.status_code == 200
    games = r.json()["games"]
    ids = {g["id"] for g in games}
    assert ids == {"4d", "5d", "6d", "6_58", "6_55", "6_52", "6_50"}
    types = {g["id"]: g["type"] for g in games}
    assert types["4d"] == "digit"
    assert types["5d"] == "digit"
    assert types["6d"] == "digit"
    assert types["6_58"] == "pick"
    # verify digits counts
    by_id = {g["id"]: g for g in games}
    assert by_id["4d"]["digits"] == 4
    assert by_id["5d"]["digits"] == 5
    assert by_id["6d"]["digits"] == 6


def test_list_packages(session):
    r = session.get(f"{BASE_URL}/api/packages")
    assert r.status_code == 200
    ids = {p["id"] for p in r.json()["packages"]}
    assert ids == {"premium_pick", "credits_10", "vip_monthly"}


# ---------- Auth ----------
def test_register_grants_3_credits(auth):
    assert auth["user"]["credits"] == 3
    assert auth["user"]["is_vip"] is False


def test_register_duplicate(session):
    r = session.post(f"{BASE_URL}/api/auth/register", json={"email": EMAIL, "password": PASSWORD})
    assert r.status_code == 400


def test_login_success(session):
    r = session.post(f"{BASE_URL}/api/auth/login", json={"email": EMAIL, "password": PASSWORD})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_invalid(session):
    r = session.post(f"{BASE_URL}/api/auth/login", json={"email": EMAIL, "password": "wrong"})
    assert r.status_code == 401


def test_me(session, auth_headers):
    r = session.get(f"{BASE_URL}/api/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == EMAIL


def test_me_unauthorized(session):
    r = session.get(f"{BASE_URL}/api/auth/me")
    assert r.status_code in (401, 403)


# ---------- Generate: PICK games ----------
def test_generate_quick_pick_658(session, auth_headers):
    r = session.post(f"{BASE_URL}/api/generate", json={"game_id": "6_58", "mode": "quick"}, headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    nums = data["pick"]["numbers"]
    assert len(nums) == 6
    assert len(set(nums)) == 6
    assert all(1 <= n <= 58 for n in nums)
    assert nums == sorted(nums)
    assert data["user"]["credits"] == 3  # quick does not consume


def test_generate_quick_bad_game(session, auth_headers):
    r = session.post(f"{BASE_URL}/api/generate", json={"game_id": "nope", "mode": "quick"}, headers=auth_headers)
    assert r.status_code == 400


# ---------- Generate: DIGIT games (NEW) ----------
def test_generate_quick_4d(session, auth_headers):
    r = session.post(f"{BASE_URL}/api/generate", json={"game_id": "4d", "mode": "quick"}, headers=auth_headers)
    assert r.status_code == 200, r.text
    pick = r.json()["pick"]
    assert pick["game_type"] == "digit"
    seq = pick["digit_sequence"]
    assert isinstance(seq, str) and len(seq) == 4 and seq.isdigit()
    assert pick["numbers"] == []
    # credit unchanged
    assert r.json()["user"]["credits"] == 3


def test_generate_quick_5d(session, auth_headers):
    r = session.post(f"{BASE_URL}/api/generate", json={"game_id": "5d", "mode": "quick"}, headers=auth_headers)
    assert r.status_code == 200, r.text
    seq = r.json()["pick"]["digit_sequence"]
    assert len(seq) == 5 and seq.isdigit()


def test_generate_quick_6d(session, auth_headers):
    r = session.post(f"{BASE_URL}/api/generate", json={"game_id": "6d", "mode": "quick"}, headers=auth_headers)
    assert r.status_code == 200, r.text
    seq = r.json()["pick"]["digit_sequence"]
    assert len(seq) == 6 and seq.isdigit()


def test_generate_ai_6d_consumes_credit(session, auth_headers):
    r = session.post(
        f"{BASE_URL}/api/generate",
        json={"game_id": "6d", "mode": "ai", "birthday": "1990-05-12",
              "zodiac": "Taurus", "lucky_numbers": [7, 13]},
        headers=auth_headers,
        timeout=90,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    pick = data["pick"]
    assert pick["game_type"] == "digit"
    seq = pick["digit_sequence"]
    assert isinstance(seq, str) and len(seq) == 6 and seq.isdigit()
    assert pick["reasoning"]
    assert data["user"]["credits"] == 2  # 1 consumed


def test_generate_ai_4d(session, auth_headers):
    r = session.post(
        f"{BASE_URL}/api/generate",
        json={"game_id": "4d", "mode": "ai", "birthday": "1985-01-01"},
        headers=auth_headers,
        timeout=90,
    )
    assert r.status_code == 200, r.text
    seq = r.json()["pick"]["digit_sequence"]
    assert len(seq) == 4 and seq.isdigit()
    # credits decremented to 1
    assert r.json()["user"]["credits"] == 1


def test_generate_ai_exhaust_and_402(session, auth_headers):
    # consume remaining 1 credit
    r = session.post(
        f"{BASE_URL}/api/generate",
        json={"game_id": "6_52", "mode": "ai"},
        headers=auth_headers,
        timeout=90,
    )
    assert r.status_code == 200, r.text
    # next AI call -> 402
    r = session.post(
        f"{BASE_URL}/api/generate",
        json={"game_id": "6_52", "mode": "ai"},
        headers=auth_headers,
        timeout=90,
    )
    assert r.status_code == 402


def test_picks_history_mixed(session, auth_headers):
    r = session.get(f"{BASE_URL}/api/picks", headers=auth_headers)
    assert r.status_code == 200
    picks = r.json()["picks"]
    # We did at minimum: 1 quick 6_58, 1 quick 4d, 1 quick 5d, 1 quick 6d,
    # 1 ai 6d, 1 ai 4d, 1 ai 6_52 = 7
    assert len(picks) >= 6
    # mixed: both digit and pick game types appear
    types = {p.get("game_type") for p in picks}
    assert "digit" in types
    assert "pick" in types
    # desc order
    ts = [p["created_at"] for p in picks]
    assert ts == sorted(ts, reverse=True)


# ---------- Payments ----------
def test_checkout_credits_10(session, auth_headers):
    r = session.post(
        f"{BASE_URL}/api/payments/checkout",
        json={"package_id": "credits_10", "origin_url": "https://example.com"},
        headers=auth_headers,
        timeout=30,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["url"].startswith("https://checkout.stripe.com")
    assert data["session_id"]

    # REGRESSION: status must return 200 even if Stripe hasn't propagated.
    s = session.get(f"{BASE_URL}/api/payments/status/{data['session_id']}",
                    headers=auth_headers, timeout=30)
    assert s.status_code == 200, s.text
    sd = s.json()
    # Either propagated already, OR returns pending fallback (warning field present).
    assert sd["status"] in ("open", "complete", "expired")
    assert sd["payment_status"] in ("pending", "initiated", "unpaid", "paid", "no_payment_required")
    assert sd["transaction"]["credits_granted"] is False


def test_checkout_bad_package(session, auth_headers):
    r = session.post(
        f"{BASE_URL}/api/payments/checkout",
        json={"package_id": "nope", "origin_url": "https://example.com"},
        headers=auth_headers,
    )
    assert r.status_code == 400


def test_payment_status_unknown_session_returns_404(session, auth_headers):
    # Unknown session_id not in our DB -> 404 (not 500)
    r = session.get(
        f"{BASE_URL}/api/payments/status/cs_test_unknown_session_xyz",
        headers=auth_headers, timeout=15,
    )
    assert r.status_code == 404
