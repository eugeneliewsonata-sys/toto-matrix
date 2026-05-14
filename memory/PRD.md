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

## What's Been Implemented (May 14, 2026)
- ✅ Auth: register / login / JWT / `/auth/me` (3 free AI credits on signup)
- ✅ Games endpoint with 7 variants (4D, 5D, 6D + 6/58, 6/55, 6/52, 6/50)
- ✅ Quick Pick generation (random, free, unlimited)
- ✅ AI Lucky Pick via Gemini 2.5 Flash with numerology reasoning
- ✅ Hot / Cold number analysis surfaced on AI picks
- ✅ Credit consumption + VIP override (unlimited for VIP)
- ✅ Pick history (sorted desc)
- ✅ Stripe checkout (one-time + subscription packages)
- ✅ Payment status polling endpoint (graceful pending state on Stripe propagation delay)
- ✅ Stripe webhook for idempotent grant
- ✅ Swiss-minimalist red/white UI with bold typography (Manrope)
- ✅ 4D/5D/6D rendered with big bold digits and thin dividers (per design req)
- ✅ Toto picks rendered as solid red circles with white numbers
- ✅ Mobile shell with sticky bottom nav, sticky action buttons (banking-app pattern)
- ✅ Form validation: AI predict button disabled until at least one input provided
- ✅ data-testid attributes across all interactive elements
- ✅ Backend: 21/21 pytest tests pass, AI generation produces valid in-range results

## Prioritized Backlog
**P0 / Next polish**
- Push notifications for upcoming draw reminders
- Add real Malaysia draw history scraper (currently `hot_cold_analysis` uses deterministic sample)

**P1**
- Internationalization (English + 中文 Bahasa Malaysia)
- Share pick to WhatsApp deep-link (the existing Streamlit app had this)
- Save/star favourite picks

**P2**
- Capacitor wrapper for Google Play / App Store submission
- Lottery jackpot tracker (live data feed)
- Friend referral credits

## Known Limitations
- Hot/cold numbers are simulated (deterministic random) until a real Malaysia draw history feed is wired in
- Bcrypt password hashing version pinned to 4.0.1 to avoid passlib 1.7.4 incompatibility
- PWA installable but not yet wrapped for native app stores
