# Test Credentials – HuatPick

## Admin Account
- **Email**: `admin@huatpick.com`
- **Password**: `adminpass123`
- Granted admin privileges via `ADMIN_EMAILS` env var in `/app/backend/.env`
- Has access to `/admin` route, `/api/admin/*` endpoints (stats, draws, scrape)

## Regular Test User
- Email: `tester+<timestamp>@huatpick.com`
- Password: `lucky123` (any value ≥ 6 chars)

## Sample API token request
```bash
TOKEN=$(curl -s -X POST $BACKEND_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@huatpick.com","password":"adminpass123"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# Check admin stats:
curl -s "$BACKEND_URL/api/admin/stats" -H "Authorization: Bearer $TOKEN"
```

## Stripe
Test key (already in backend/.env): `STRIPE_API_KEY=sk_test_emergent` (Emergent-managed proxy).
Use Stripe test card `4242 4242 4242 4242` for end-to-end flow.

## Emergent LLM Key
`EMERGENT_LLM_KEY=sk-emergent-aB2C8Ae6684E4C42fC` (backend/.env). Used for AI Lucky Picks via Gemini 2.5 Flash.

## Admin Endpoints
- `GET  /api/admin/stats` — system counters + live hot/cold preview
- `GET  /api/admin/draws` — list of bundled + manual + scraped data pool stats
- `POST /api/admin/draws` `{raw_text, label}` — paste raw text, extracts every 4-digit run
- `POST /api/admin/scrape` — triggers live scrape from www.4dmoon.com
