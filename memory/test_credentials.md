# Test Credentials – HuatPick

Auth uses email + password. There is no admin / superuser. Tests should create fresh accounts.

## Sample test user (created on demand)
- Email: `tester+<timestamp>@huatpick.com`
- Password: `lucky123` (any value ≥ 6 chars)

## Sample API token request
```bash
TOKEN=$(curl -s -X POST $BACKEND_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"tester+demo@huatpick.com","password":"lucky123","name":"Demo"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
```

## Stripe
Test key (already in backend/.env): `STRIPE_API_KEY=sk_test_emergent` (Emergent-managed proxy).
Use Stripe test card `4242 4242 4242 4242` for end-to-end flow.

## Emergent LLM Key
`EMERGENT_LLM_KEY=sk-emergent-aB2C8Ae6684E4C42fC` (backend/.env). Used for AI Lucky Picks via Gemini 2.5 Flash.
