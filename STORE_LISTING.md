# Play Store / App Store Listing — Ready-to-Paste Content

All assets are at `/app/frontend/assets/` and `/app/frontend/icons/`.
Native projects already include every required size — no manual upload of icons needed.

---

## 1. App identity

| Field | Value |
|---|---|
| **App name** | HuatPick |
| **Short name** | HuatPick |
| **Developer / Publisher** | JH Creative Enterprise |
| **Support email** | turyoungpotato@gmail.com |
| **Category** | Entertainment (primary) / Lifestyle (secondary) |
| **Content rating** | 18+ (Mature 17+ on App Store; Adults Only or Mature on Play) |
| **Age rating questionnaire** | "Simulated gambling: No" — we suggest numbers, we don't take bets |

## 2. Assets bundled in this repo

| File | Dimensions | Use |
|---|---|---|
| `/app/frontend/assets/icon.png` | 1024×1024 | Master app icon (Play & App Store) |
| `/app/frontend/assets/icon-512.png` | 512×512 | Play Store high-res icon upload |
| `/app/frontend/assets/icon-192.png` | 192×192 | Backup |
| `/app/frontend/assets/feature-graphic.png` | 1024×500 | Play Store feature graphic |
| `/app/frontend/android/app/src/main/res/mipmap-*/ic_launcher*` | all densities | Built into APK / AAB |
| `/app/frontend/ios/App/App/Assets.xcassets/AppIcon.appiconset/` | all sizes | Built into iOS app |

## 3. Required URLs

| Field | URL |
|---|---|
| **Privacy Policy URL** | `https://<your-deployed-url>/privacy` |
| **Terms of Service URL** | `https://<your-deployed-url>/terms` |
| **Marketing website** (optional) | `https://<your-deployed-url>` |
| **Support URL** | `mailto:turyoungpotato@gmail.com` |

> Replace `<your-deployed-url>` with the URL you publish from Emergent's deployment.

---

## 4. Store listing copy (English)

### App title (30 chars max)
```
HuatPick: Lottery AI Picks
```
*28 characters*

### Short description (80 chars max for Play Store)
```
Lucky numbers, picked smart. AI lucky picks for Malaysia 4D, 5D, 6D & Toto.
```
*75 characters*

### Full description (4000 chars max — Play Store)
```
HuatPick is the smartest lucky-number generator for Malaysia lottery players.

▸ COVERS EVERY POPULAR GAME
• 4D — classic four-digit
• 5D — five-digit
• 6D — six-digit
• Sports Toto 6/58, 6/55, 6/52 & 6/50

▸ TWO WAYS TO PICK
• Quick Pick — instant, free, unbiased randomness (unlimited)
• AI Lucky Pick — combines your numerology (birthday, zodiac, lucky numbers) with real hot/cold draw frequencies

▸ POWERED BY REAL DATA
We continuously analyze hundreds of past Malaysia 4D draws and recent Sports Toto results to surface the hot and cold numbers — so every AI pick is rooted in actual frequency data, not pure superstition.

▸ BEAUTIFULLY MINIMAL
Swiss-minimalist red & white design. No noise, no clutter — just bold lucky numbers, big and bright.

▸ YOUR FORTUNE LEDGER
Every pick is saved to your personal history. Track what you tried, what worked, and revisit your favourites any time.

▸ VIP HIGH-ROLLER MEMBERSHIP
Upgrade for unlimited AI lucky picks, personalized numerology, priority generation, and an ad-free experience.

▸ PRIVACY-FIRST
We never see your card details — payments are handled by Stripe. We don't sell ads, we don't track you across the web.

▸ FOR ENTERTAINMENT ONLY
HuatPick is an entertainment app. It does not sell lottery tickets and does not guarantee winnings. Lottery draws are random — past frequencies have no predictive power over future results. Please play responsibly. You must be 18 or older to use HuatPick.

GET LUCKY: download HuatPick today and let the numbers find you.

—
Made with care in Malaysia by JH Creative Enterprise.
Support: turyoungpotato@gmail.com
```

### Keywords / Tags (Play Store)
```
malaysia lottery, 4d, toto, lucky numbers, AI, prediction, lottery picker,
malaysia 4d, sports toto, magnum, 5d 6d, lottery analysis, hot numbers, cold numbers
```

### App Store keywords (100 chars, comma-separated)
```
lottery,4d,toto,malaysia,lucky,numbers,ai,prediction,5d,6d,magnum,hotcold,picker
```

### What's new (release notes, 500 chars)
```
First public release of HuatPick!
• Generate lucky numbers for Malaysia 4D, 5D, 6D, and Sports Toto 6/58, 6/55, 6/52, 6/50
• AI Lucky Picks powered by Gemini and real Malaysia draw history
• Hot/cold number analysis from live Sports Toto scraping
• Beautiful Swiss-minimalist red & white design
• Unlimited Quick Picks (free)
• VIP membership for unlimited AI picks
```

---

## 5. Screenshots (you'll capture these from the running app)

The Play Store wants **at least 2** phone screenshots, ideally 4–8.
App Store wants **at least 3** per device family (iPhone 6.7", 6.5", 5.5").

Recommended screens to capture (in this order):

1. **Home** — show the hero "Generate lucky numbers in 2 seconds." card + game list
2. **Generate / 4D / Spinning** — the spinning digit row mid-animation (most "alive")
3. **Result modal** — big bold lucky numbers with the AI reasoning text underneath
4. **History** — the ledger of past picks
5. **VIP** — the three-tier upgrade page

### How to capture clean screenshots (using your phone in dev mode)
```bash
# Connect Android phone via USB with debugging enabled
adb exec-out screencap -p > screen-home.png

# OR use Chrome DevTools' device-emulation screenshot
# Open https://<your-deployed-url> in Chrome → DevTools → Device toolbar →
# pick "iPhone 14 Pro Max" → ⋮ menu → "Capture full size screenshot"
```

Recommended frame size for Play Store: **1080 × 1920** or **1440 × 2560**.
Recommended for App Store iPhone 6.7": **1290 × 2796**.

---

## 6. Submission checklist

### Play Store (Google)
- [ ] $25 one-time Google Play Developer fee paid
- [ ] App created in Play Console; package name `com.huatpick.app` (or your choice)
- [ ] App content section: privacy policy URL, target audience (18+), ads (No), data safety form filled (we collect email + payment + usage)
- [ ] Store listing: title, short + full descriptions, screenshots (≥2), feature graphic, hi-res icon (512×512)
- [ ] Release: signed AAB uploaded to Production track (or Internal Testing first — recommended)
- [ ] Review & roll out

### App Store (Apple)
- [ ] $99 annual Apple Developer Program fee paid
- [ ] App ID `com.huatpick.app` created on developer.apple.com
- [ ] App created in App Store Connect; primary language English
- [ ] App Privacy section: same data points as Play Store
- [ ] Listing: name, subtitle, promotional text, description, keywords, support URL, screenshots per device family
- [ ] Archive in Xcode → Upload → wait for processing → Submit for Review

---

## 7. After submission

- **Play Store review** typically takes 1–3 days. First-time accounts can take up to 14 days.
- **App Store review** typically 24–48 hours. Common rejection reasons for lottery-style apps: missing 18+ rating, unclear refund policy, or no privacy-policy URL — all already handled in this repo. Make sure your screenshots **do not show actual lottery brand logos** (Magnum, Sports Toto, etc.) without permission, or Apple may reject.

Need any of these copy lines translated to Bahasa Malaysia or 中文? Just ask.
