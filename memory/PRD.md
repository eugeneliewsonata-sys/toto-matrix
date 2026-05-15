# HuatPick — Malaysia Lottery AI Mobile App

## Original Problem Statement
> "Build a mobile app: build me an app for this — about number prediction for lottery, platform work for android and ios, key features: generate lucky numbers, 3rd party payment via stripe, design like casino design"

Refinements from clarifications:
- Malaysia Toto lottery (Toto 6/58, 6/55, 6/52, 6/50) + Malaysia digit lotteries (4D, 5D, 6D)
- Two generation modes: Quick Pick (random, free) and AI Lucky Picks (Gemini-powered numerology, paid)
- Stripe (subscription + one-time premium picks)
- Email + password JWT auth
- Final design direction (overrode initial casino theme): **Swiss-minimalist red & white**, banking-app feel, Manrope typography, lots of whitespace, single red accent

## Architecture
- **Backend**: FastAPI + MongoDB + JWT + Emergent LLM key (Gemini 2.5 Flash) + Stripe checkout via emergentintegrations
- **Frontend**: React 18 + React Router 6 + Tailwind 3 + Framer Motion + Sonner toasts, mobile-shell max-w-md
- **Mobile delivery**: Mobile-first responsive PWA (works on Android / iOS Safari). Wrappable later with Capacitor for App Store / Play Store.

## Personas
1. **Casual Player** — wants a free Quick Pick once a day, casual entertainment
2. **Believer** — wants personalized AI picks using birthday/zodiac/lucky numbers, willing to buy credits
3. **High Roller** — wants unlimited AI picks via VIP subscription

## Core Requirements (static)
- Generate lucky numbers for 7 Malaysia lottery variants
- Personalized AI predictions
- Stripe payments (one-time + subscription)
- History ledger
- Clean mobile-first UI

## What's Been Implemented (May 15, 2026)
- ✅ Auth: register / login / JWT / `/auth/me` (3 free AI credits on signup)
- ✅ Games endpoint with 7 variants (4D, 5D, 6D + 6/58, 6/55, 6/52, 6/50)
- ✅ Quick Pick generation (random, free, unlimited)
- ✅ AI Lucky Pick via Gemini 2.5 Flash with numerology reasoning
- ✅ **REAL Malaysia 4D draw history bundled** (25 draws, 575 numbers, 2300 digit observations from Feb–Mar 2026)
- ✅ **REAL hot/cold analysis** — derived from actual draw frequencies (digit 9 hottest @ 247 hits, 7 coldest @ 207 hits; Toto 6/58: 44/55 hot, 16/21 cold)
- ✅ **Live scraping** from www.4dmoon.com on startup + on-demand via admin endpoint
- ✅ **Admin Console** (gated by `ADMIN_EMAILS` env var): stats dashboard, data library counts, run-live-scrape button, paste-text-to-inject draws, hot/cold preview
- ✅ Credit consumption + VIP override (unlimited for VIP)
- ✅ Pick history (sorted desc, mixed digit + pick games)
- ✅ Stripe checkout (one-time + subscription packages)
- ✅ Stripe webhook + payment status polling (graceful pending on propagation delay)
- ✅ Swiss-minimalist red/white UI with Manrope typography
- ✅ 4D/5D/6D rendered with big bold digits and thin dividers
- ✅ Toto picks rendered as solid red circles with white numbers
- ✅ Mobile shell + sticky bottom nav + sticky action buttons (no overlap)
- ✅ Form validation: AI predict button disabled until at least one input provided
- ✅ data-testid attributes across all interactive elements
- ✅ Backend: 33/33 pytest tests pass (auth, games, generate quick & AI, payments, admin)
- ✅ Frontend: all flows verified by Playwright agent

## Prioritized Backlog
**P0 / Next polish**
- Push notifications for upcoming draw reminders
- Disable Inject button when raw_text is empty (small UX gap noted by tester)

**P1**
- Internationalization (English + 中文 + Bahasa Malaysia)
- Share pick to WhatsApp deep-link (the existing Streamlit app had this)
- Save/star favourite picks
- Scrape Sports Toto official results for true Toto 6/58 etc. frequencies (currently derived from 2-digit windows of 4D pool)

**P2**
- Capacitor wrapper for Google Play / App Store submission
- Lottery jackpot tracker (live data feed)
- Friend referral credits
- Tighten CORS: pin `allow_origins` to actual frontend URL (currently `*` with credentials)

## Known Limitations
- Toto hot/cold derived from 2-digit windows of 4D data (real but a proxy) until Sports Toto scraper is added
- Bcrypt password hashing version pinned to 4.0.1 to avoid passlib 1.7.4 incompatibility
- PWA installable but not yet wrapped for native app stores
- Live scrape from 4dmoon.com may fail in restricted networks — fallback is bundled history
