"""LottoLuxe Backend - Casino-themed Malaysia Toto Lottery Prediction App."""
import os
import random
import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
import jwt
from dotenv import load_dotenv

import lottery_data as ld

# Load env first
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# Mongo setup
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# JWT
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = os.environ["JWT_ALGORITHM"]
JWT_EXPIRE = int(os.environ["JWT_EXPIRE_MINUTES"])

# Password hashing
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Auth
bearer = HTTPBearer(auto_error=False)

# Emergent LLM
EMERGENT_LLM_KEY = os.environ["EMERGENT_LLM_KEY"]
STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
ADMIN_EMAILS = {e.strip().lower() for e in os.environ.get("ADMIN_EMAILS", "").split(",") if e.strip()}

# ---------- Malaysia Lottery Games Config ----------
# type: "pick" = choose K numbers from 1..max ; type: "digit" = a single N-digit number
TOTO_GAMES = {
    "4d":   {"id": "4d",   "name": "4D",                "type": "digit", "digits": 4, "label": "Classic 4-Digit"},
    "5d":   {"id": "5d",   "name": "5D",                "type": "digit", "digits": 5, "label": "Big 5-Digit"},
    "6d":   {"id": "6d",   "name": "6D",                "type": "digit", "digits": 6, "label": "Mega 6-Digit"},
    "6_58": {"id": "6_58", "name": "6/58 Toto Mega",    "type": "pick",  "max": 58, "picks": 6, "label": "Mega Jackpot"},
    "6_55": {"id": "6_55", "name": "Power Toto 6/55",   "type": "pick",  "max": 55, "picks": 6, "label": "Power Draw"},
    "6_52": {"id": "6_52", "name": "Star Toto 6/52",    "type": "pick",  "max": 52, "picks": 6, "label": "Star Pick"},
    "6_50": {"id": "6_50", "name": "Supreme Toto 6/50", "type": "pick",  "max": 50, "picks": 6, "label": "Supreme Cash"},
}

# Pricing packages (server-side, NEVER from frontend)
PACKAGES = {
    "premium_pick": {"name": "Single Premium AI Pick", "amount": 1.99, "currency": "myr", "type": "one_time", "credits": 1},
    "credits_10": {"name": "10 Premium AI Picks", "amount": 9.99, "currency": "myr", "type": "one_time", "credits": 10},
    "vip_monthly": {"name": "High Roller VIP - Monthly", "amount": 14.99, "currency": "myr", "type": "subscription", "credits": 9999, "days": 30},
}

# ---------- Models ----------
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict

class GenerateRequest(BaseModel):
    game_id: str
    mode: str = "quick"  # quick | ai
    birthday: Optional[str] = None
    zodiac: Optional[str] = None
    lucky_numbers: Optional[List[int]] = None

class CheckoutRequest(BaseModel):
    package_id: str
    origin_url: str

# ---------- Helpers ----------
def now_utc():
    return datetime.now(timezone.utc)

def create_jwt(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": now_utc() + timedelta(minutes=JWT_EXPIRE),
        "iat": now_utc(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALGO])
        user = await db.users.find_one({"id": payload["sub"]}, {"_id": 0, "password_hash": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def serialize_user(u: dict) -> dict:
    return {
        "id": u["id"],
        "email": u["email"],
        "name": u.get("name") or u["email"].split("@")[0],
        "credits": u.get("credits", 3),
        "vip_until": u.get("vip_until"),
        "is_vip": bool(u.get("vip_until") and datetime.fromisoformat(u["vip_until"]) > now_utc()),
        "is_admin": u["email"].lower() in ADMIN_EMAILS,
    }

# ---------- App ----------
app = FastAPI(title="LottoLuxe API")

# Parse allowed origins; wildcard disables credentials per CORS spec.
_origins_raw = os.environ.get("CORS_ORIGINS", "*").strip()
_origins = [o.strip() for o in _origins_raw.split(",") if o.strip()]
_use_wildcard = (len(_origins) == 1 and _origins[0] == "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins if not _use_wildcard else ["*"],
    allow_credentials=not _use_wildcard,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Public ----------
@app.get("/api/")
async def root():
    return {"app": "LottoLuxe", "status": "ok", "time": now_utc().isoformat()}

@app.get("/api/games")
async def list_games():
    return {"games": list(TOTO_GAMES.values())}

@app.get("/api/packages")
async def list_packages():
    return {"packages": [{"id": k, **v} for k, v in PACKAGES.items()]}

# ---------- Auth ----------
@app.post("/api/auth/register", response_model=TokenResponse)
async def register(body: UserRegister):
    existing = await db.users.find_one({"email": body.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "email": body.email.lower(),
        "name": body.name or body.email.split("@")[0],
        "password_hash": pwd_ctx.hash(body.password),
        "credits": 3,  # 3 free AI picks on signup
        "vip_until": None,
        "created_at": now_utc().isoformat(),
    }
    await db.users.insert_one(user_doc)
    token = create_jwt(user_id, body.email.lower())
    return TokenResponse(access_token=token, user=serialize_user(user_doc))

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(body: UserLogin):
    user = await db.users.find_one({"email": body.email.lower()})
    if not user or not pwd_ctx.verify(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_jwt(user["id"], user["email"])
    return TokenResponse(access_token=token, user=serialize_user(user))

@app.get("/api/auth/me")
async def me(user=Depends(get_current_user)):
    return serialize_user(user)

# ---------- Number Generation ----------
def quick_pick(max_n: int, count: int) -> List[int]:
    return sorted(random.sample(range(1, max_n + 1), count))

def quick_digits(n: int) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(n))

# ---------- Live pool cache (refreshed lazily) ----------
_LIVE_POOL_CACHE: Dict[str, object] = {"text": "", "fetched_at": None}

async def get_extra_pool() -> str:
    """Returns concatenated 4-digit strings from MongoDB `draws` + cached
    live-scraped data. Scrapes once if cache is older than 6 hours."""
    parts: List[str] = []
    # Manual / scraped draws saved in Mongo (admin-added)
    cursor = db.draws.find({}, {"_id": 0, "numbers": 1, "raw": 1})
    async for doc in cursor:
        if doc.get("numbers"):
            parts.append("".join(doc["numbers"]))
        elif doc.get("raw"):
            parts.append(doc["raw"])
    # Live scrape cache
    fetched_at = _LIVE_POOL_CACHE.get("fetched_at")
    now = now_utc()
    stale = (fetched_at is None) or ((now - fetched_at).total_seconds() > 6 * 3600)
    if stale:
        try:
            nums = await asyncio.to_thread(ld.scrape_live_4d, 6.0, 200)
            _LIVE_POOL_CACHE["text"] = "".join(nums)
            _LIVE_POOL_CACHE["fetched_at"] = now
            _LIVE_POOL_CACHE["count"] = len(nums)
        except Exception:
            _LIVE_POOL_CACHE["text"] = _LIVE_POOL_CACHE.get("text", "")
    parts.append(str(_LIVE_POOL_CACHE.get("text", "")))
    return "".join(parts)

async def hot_cold_digits_real() -> Dict[str, List[int]]:
    extra = await get_extra_pool()
    return ld.hot_cold_digits(extra_pool=extra, top_k=5)

async def hot_cold_analysis_real(max_n: int) -> Dict[str, List[int]]:
    extra = await get_extra_pool()
    return ld.hot_cold_numbers(max_n, extra_pool=extra, top_k=8)

# Synchronous fallbacks (offline)
def hot_cold_digits() -> Dict[str, List[int]]:
    return ld.hot_cold_digits(top_k=5)

def hot_cold_analysis(max_n: int) -> Dict[str, List[int]]:
    """Real hot/cold derived from bundled Malaysia 4D history (no live extra)."""
    return ld.hot_cold_numbers(max_n, top_k=8)

async def ai_lucky_pick(game: dict, birthday: Optional[str], zodiac: Optional[str], lucky_numbers: Optional[List[int]]) -> Dict:
    """Use Emergent LLM to recommend numbers (pick game) or a digit sequence (4D/5D/6D)."""
    from emergentintegrations.llm.chat import LlmChat, UserMessage

    is_digit = game.get("type") == "digit"

    if is_digit:
        n_digits = game["digits"]
        hc = await hot_cold_digits_real()
        sys_msg = (
            f"You are a Malaysia lottery numerologist for the {game['name']} game. "
            f"Produce ONE lucky {n_digits}-digit number (0-9 each digit, leading zeros allowed). "
            "Blend the player's numerology cues with hot/cold digit frequencies. "
            "Reply with EXACTLY this format on two lines:\n"
            f"DIGITS: <{n_digits} digits, no spaces, no commas>\n"
            "REASONING: <one short sentence under 28 words>"
        )
        user_txt = (
            f"Game: {game['name']} ({n_digits}-digit)\n"
            f"Birthday: {birthday or 'unknown'}\n"
            f"Zodiac: {zodiac or 'unknown'}\n"
            f"User lucky numbers: {lucky_numbers or 'none'}\n"
            f"Hot digits (frequent): {hc['hot']}\n"
            f"Cold digits (rare, due): {hc['cold']}\n"
        )
    else:
        max_n = game["max"]
        hc = await hot_cold_analysis_real(max_n)
        sys_msg = (
            "You are a Malaysia lottery numerologist. You will produce one set of "
            f"{game['picks']} unique lucky lottery numbers from 1 to {max_n} for a player. "
            "Combine numerology of their personal inputs with hot/cold frequency cues. "
            "Reply with EXACTLY this format on two lines:\n"
            "NUMBERS: n1,n2,n3,n4,n5,n6\n"
            "REASONING: <one short sentence under 28 words>"
        )
        user_txt = (
            f"Game: {game['name']}\n"
            f"Birthday: {birthday or 'unknown'}\n"
            f"Zodiac: {zodiac or 'unknown'}\n"
            f"User lucky numbers (consider but do not blindly include): {lucky_numbers or 'none'}\n"
            f"Hot numbers (frequent): {hc['hot']}\n"
            f"Cold numbers (rare, due): {hc['cold']}\n"
            f"Choose {game['picks']} numbers between 1 and {max_n}."
        )

    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"luckypick-{uuid.uuid4()}",
        system_message=sys_msg,
    ).with_model("gemini", "gemini-2.5-flash")

    try:
        resp_text = await chat.send_message(UserMessage(text=user_txt))
    except Exception:
        if is_digit:
            seq = quick_digits(game["digits"])
            return {"numbers": [], "digit_sequence": seq,
                    "reasoning": "Cosmic alignment with hot & cold cycle (offline mode).",
                    "hot": hc["hot"], "cold": hc["cold"]}
        numbers = sorted(random.sample(hc["hot"] + hc["cold"], game["picks"]))
        return {"numbers": numbers, "reasoning": "Cosmic alignment with hot & cold cycle (offline mode).",
                "hot": hc["hot"], "cold": hc["cold"]}

    reasoning = ""
    digit_seq = ""
    numbers: List[int] = []
    for line in resp_text.splitlines():
        line = line.strip()
        upper = line.upper()
        if upper.startswith("DIGITS") and is_digit:
            try:
                part = line.split(":", 1)[1]
                only_digits = "".join(ch for ch in part if ch.isdigit())
                if len(only_digits) >= game["digits"]:
                    digit_seq = only_digits[: game["digits"]]
            except Exception:
                pass
        elif upper.startswith("NUMBERS") and not is_digit:
            try:
                part = line.split(":", 1)[1]
                nums = [int(x.strip()) for x in part.replace(" ", "").split(",") if x.strip().isdigit()]
                numbers = [n for n in nums if 1 <= n <= game["max"]]
            except Exception:
                pass
        elif upper.startswith("REASONING"):
            try:
                reasoning = line.split(":", 1)[1].strip()
            except Exception:
                pass
        elif line.upper().startswith("REASONING"):
            try:
                reasoning = line.split(":", 1)[1].strip()
            except Exception:
                pass

    if game.get("type") == "digit":
        if not digit_seq:
            digit_seq = quick_digits(game["digits"])
        if not reasoning:
            reasoning = "Numerology mapped onto the digit frequency rhythm."
        return {"numbers": [], "digit_sequence": digit_seq, "reasoning": reasoning,
                "hot": hc["hot"], "cold": hc["cold"]}

    # dedupe & ensure count for pick games
    max_n = game["max"]
    numbers = list(dict.fromkeys(numbers))
    while len(numbers) < game["picks"]:
        cand = random.randint(1, max_n)
        if cand not in numbers:
            numbers.append(cand)
    numbers = sorted(numbers[: game["picks"]])

    if not reasoning:
        reasoning = "Numerology aligned with hot/cold rhythm of recent draws."

    return {"numbers": numbers, "reasoning": reasoning, "hot": hc["hot"], "cold": hc["cold"]}

@app.post("/api/generate")
async def generate(body: GenerateRequest, user=Depends(get_current_user)):
    game = TOTO_GAMES.get(body.game_id)
    if not game:
        raise HTTPException(status_code=400, detail="Unknown game")

    mode = body.mode.lower()
    if mode not in ("quick", "ai"):
        raise HTTPException(status_code=400, detail="mode must be 'quick' or 'ai'")

    is_vip = bool(user.get("vip_until") and datetime.fromisoformat(user["vip_until"]) > now_utc())

    if mode == "ai":
        if not is_vip and user.get("credits", 0) < 1:
            raise HTTPException(status_code=402, detail="Insufficient credits. Buy AI Picks or upgrade to VIP.")
        result = await ai_lucky_pick(game, body.birthday, body.zodiac, body.lucky_numbers)
        if not is_vip:
            await db.users.update_one({"id": user["id"]}, {"$inc": {"credits": -1}})
    else:
        if game.get("type") == "digit":
            result = {"numbers": [], "digit_sequence": quick_digits(game["digits"]),
                      "reasoning": "Quick Pick - randomized digits.", "hot": [], "cold": []}
        else:
            nums = quick_pick(game["max"], game["picks"])
            result = {"numbers": nums, "reasoning": "Quick Pick - randomized lucky draw.", "hot": [], "cold": []}

    pick_doc = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "game_id": game["id"],
        "game_name": game["name"],
        "game_type": game.get("type", "pick"),
        "mode": mode,
        "numbers": result.get("numbers", []),
        "digit_sequence": result.get("digit_sequence"),
        "reasoning": result["reasoning"],
        "hot": result.get("hot", []),
        "cold": result.get("cold", []),
        "created_at": now_utc().isoformat(),
    }
    await db.picks.insert_one(pick_doc)
    pick_doc.pop("_id", None)

    # refreshed user
    fresh = await db.users.find_one({"id": user["id"]}, {"_id": 0, "password_hash": 0})
    return {"pick": pick_doc, "user": serialize_user(fresh)}

@app.get("/api/picks")
async def my_picks(user=Depends(get_current_user)):
    cursor = db.picks.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).limit(100)
    items = await cursor.to_list(length=100)
    return {"picks": items}

# ---------- Stripe ----------
@app.post("/api/payments/checkout")
async def create_checkout(body: CheckoutRequest, request: Request, user=Depends(get_current_user)):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest

    pkg = PACKAGES.get(body.package_id)
    if not pkg:
        raise HTTPException(status_code=400, detail="Invalid package")

    origin = body.origin_url.rstrip("/")
    success_url = f"{origin}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{origin}/vip"

    host_url = str(request.base_url)
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)

    metadata = {
        "user_id": user["id"],
        "user_email": user["email"],
        "package_id": body.package_id,
        "package_name": pkg["name"],
        "package_type": pkg["type"],
    }

    req = CheckoutSessionRequest(
        amount=float(pkg["amount"]),
        currency=pkg["currency"],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
    )
    session = await stripe_checkout.create_checkout_session(req)

    # Record transaction as initiated
    txn = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "user_email": user["email"],
        "session_id": session.session_id,
        "package_id": body.package_id,
        "amount": float(pkg["amount"]),
        "currency": pkg["currency"],
        "payment_status": "initiated",
        "status": "open",
        "credits_granted": False,
        "metadata": metadata,
        "created_at": now_utc().isoformat(),
    }
    await db.payment_transactions.insert_one(txn)

    return {"url": session.url, "session_id": session.session_id}

async def _grant_package(session_id: str):
    """Idempotently grant credits/VIP based on a paid session."""
    txn = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
    if not txn:
        return None
    if txn.get("credits_granted"):
        return txn

    pkg = PACKAGES.get(txn["package_id"])
    if not pkg:
        return txn

    update: Dict = {"$set": {"credits_granted": True, "granted_at": now_utc().isoformat()}}
    user_update: Dict = {}
    if pkg["type"] == "one_time":
        user_update = {"$inc": {"credits": int(pkg["credits"])}}
    elif pkg["type"] == "subscription":
        # extend VIP
        user = await db.users.find_one({"id": txn["user_id"]}, {"_id": 0})
        base = now_utc()
        if user and user.get("vip_until"):
            existing = datetime.fromisoformat(user["vip_until"])
            if existing > base:
                base = existing
        new_until = (base + timedelta(days=int(pkg["days"]))).isoformat()
        user_update = {"$set": {"vip_until": new_until}}

    if user_update:
        await db.users.update_one({"id": txn["user_id"]}, user_update)
    await db.payment_transactions.update_one({"session_id": session_id}, update)
    return await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})

@app.get("/api/payments/status/{session_id}")
async def payment_status(session_id: str, request: Request, user=Depends(get_current_user)):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout

    txn = await db.payment_transactions.find_one({"session_id": session_id, "user_id": user["id"]}, {"_id": 0})
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    host_url = str(request.base_url)
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    try:
        status_resp = await stripe_checkout.get_checkout_status(session_id)
    except Exception as e:
        # Stripe may not yet have propagated the session; return pending so the
        # frontend polling can retry without failing the UX.
        fresh_user = await db.users.find_one({"id": user["id"]}, {"_id": 0, "password_hash": 0})
        return {
            "session_id": session_id,
            "status": "open",
            "payment_status": "pending",
            "amount_total": None,
            "currency": txn.get("currency"),
            "transaction": txn,
            "user": serialize_user(fresh_user),
            "warning": "stripe_status_unavailable",
        }

    await db.payment_transactions.update_one(
        {"session_id": session_id},
        {"$set": {"status": status_resp.status, "payment_status": status_resp.payment_status}},
    )

    if status_resp.payment_status == "paid":
        await _grant_package(session_id)

    fresh_user = await db.users.find_one({"id": user["id"]}, {"_id": 0, "password_hash": 0})
    fresh_txn = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})

    return {
        "session_id": session_id,
        "status": status_resp.status,
        "payment_status": status_resp.payment_status,
        "amount_total": status_resp.amount_total,
        "currency": status_resp.currency,
        "transaction": fresh_txn,
        "user": serialize_user(fresh_user),
    }

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout

    body_bytes = await request.body()
    sig = request.headers.get("Stripe-Signature")
    host_url = str(request.base_url)
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    try:
        resp = await stripe_checkout.handle_webhook(body_bytes, sig)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    if resp.payment_status == "paid" and resp.session_id:
        await _grant_package(resp.session_id)

    return {"received": True}


# ---------- Admin (lottery draws + scraping) ----------
class AdminDrawBody(BaseModel):
    raw_text: str = Field(..., description="Free-form text; every 4-digit run is extracted")
    label: Optional[str] = "manual"

def require_admin(user=Depends(get_current_user)):
    if user["email"].lower() not in ADMIN_EMAILS:
        raise HTTPException(status_code=403, detail="Admin only")
    return user

@app.get("/api/admin/draws")
async def list_draws(user=Depends(require_admin)):
    cursor = db.draws.find({}, {"_id": 0}).sort("created_at", -1).limit(200)
    items = await cursor.to_list(length=200)
    bundled_count = sum(
        len(e.get("top_3", [])) + len(e.get("special", [])) + len(e.get("consolation", []))
        for e in ld.HISTORICAL_RESULTS.values()
    )
    return {
        "bundled_count": bundled_count,
        "bundled_draws": len(ld.HISTORICAL_RESULTS),
        "manual_draws": len(items),
        "draws": items,
        "live_cache_count": _LIVE_POOL_CACHE.get("count", 0),
        "live_cache_fetched_at": (
            _LIVE_POOL_CACHE["fetched_at"].isoformat()
            if _LIVE_POOL_CACHE.get("fetched_at") else None
        ),
    }

@app.post("/api/admin/draws")
async def add_draws(body: AdminDrawBody, user=Depends(require_admin)):
    import re as _re
    nums = _re.findall(r"\b\d{4}\b", body.raw_text or "")
    if not nums:
        raise HTTPException(status_code=400, detail="No 4-digit numbers found in input")
    doc = {
        "id": str(uuid.uuid4()),
        "label": body.label or "manual",
        "numbers": nums,
        "count": len(nums),
        "source": "admin_paste",
        "created_at": now_utc().isoformat(),
        "created_by": user["email"],
    }
    await db.draws.insert_one(doc)
    doc.pop("_id", None)
    return {"added": len(nums), "draw": doc}

@app.post("/api/admin/scrape")
async def trigger_scrape(user=Depends(require_admin)):
    nums = await asyncio.to_thread(ld.scrape_live_4d, 8.0, 300)
    _LIVE_POOL_CACHE["text"] = "".join(nums)
    _LIVE_POOL_CACHE["fetched_at"] = now_utc()
    _LIVE_POOL_CACHE["count"] = len(nums)
    if nums:
        await db.draws.insert_one({
            "id": str(uuid.uuid4()),
            "label": "scrape_4dmoon",
            "numbers": nums,
            "count": len(nums),
            "source": "live_scrape",
            "created_at": now_utc().isoformat(),
            "created_by": user["email"],
        })
    return {"fetched": len(nums), "sample": nums[:10]}

@app.get("/api/admin/stats")
async def admin_stats(user=Depends(require_admin)):
    extra = await get_extra_pool()
    digits = await hot_cold_digits_real()
    toto658 = await hot_cold_analysis_real(58)
    total_users = await db.users.count_documents({})
    total_picks = await db.picks.count_documents({})
    total_txns = await db.payment_transactions.count_documents({})
    paid_txns = await db.payment_transactions.count_documents({"payment_status": "paid"})
    return {
        "users": total_users,
        "picks": total_picks,
        "txns": total_txns,
        "paid_txns": paid_txns,
        "digit_hot_cold": digits,
        "toto_6_58_hot_cold": toto658,
        "extra_pool_size": len(extra),
    }


@app.on_event("startup")
async def _seed():
    """Schedule live scrape as fire-and-forget so app start is not blocked."""
    async def _bg():
        try:
            nums = await asyncio.to_thread(ld.scrape_live_4d, 8.0, 200)
            _LIVE_POOL_CACHE["text"] = "".join(nums)
            _LIVE_POOL_CACHE["fetched_at"] = now_utc()
            _LIVE_POOL_CACHE["count"] = len(nums)
            print(f"[startup] 4dmoon scrape ok: {len(nums)} numbers")
        except Exception as e:
            print(f"[startup] 4dmoon scrape failed: {e}")

        # Sports Toto scrape (optional, best-effort)
        try:
            for game_id, max_n in [("6_58", 58), ("6_55", 55), ("6_52", 52), ("6_50", 50)]:
                draws = await asyncio.to_thread(ld.scrape_sportstoto, game_id, max_n, 60, 8.0)
                if draws:
                    # Store latest draws (replace cache row per game)
                    await db.toto_draws.delete_many({"game_id": game_id, "source": "scrape"})
                    await db.toto_draws.insert_one({
                        "id": str(uuid.uuid4()),
                        "game_id": game_id,
                        "draws": draws,
                        "count": len(draws),
                        "source": "scrape",
                        "created_at": now_utc().isoformat(),
                    })
                    print(f"[startup] sports-toto {game_id}: {len(draws)} draws cached")
        except Exception as e:
            print(f"[startup] sports-toto scrape failed: {e}")

    asyncio.create_task(_bg())


@app.on_event("shutdown")
async def shutdown():
    client.close()
