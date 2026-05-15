# Play Console — Day 1 Submission Walkthrough

Three things to do, in order. Allow ~2 hours total for a first-time developer.

---

## STEP 1 — Pay the $25 Google Play developer fee  (15 min)

You only do this once, ever.

1. Go to **https://play.google.com/console/signup**
2. Sign in with the Google account you want to own the app (use a **business account** if you have one — easier to transfer later than a personal Gmail).
3. Pick **"An organization"** account type → enter:
   - **Organization name**: `JH Creative Enterprise`
   - **Email**: `turyoungpotato@gmail.com`
   - **Country**: `Malaysia`
4. Pay the **USD $25** registration fee (one-time, non-refundable, accepts Visa/Mastercard/Amex).
5. Verify your identity — Google will email you to upload a government-issued ID (NRIC / passport).
   - Approval typically takes 1–3 business days.
   - You can start setting up the app while verification is pending.

Once approved, you'll land at the Play Console dashboard at `play.google.com/console`.

---

## STEP 2 — Build the signed `.aab` in Android Studio  (45 min)

You'll do this on your own computer.

### 2.1  Open the project
```bash
cd /path/to/your/huatpick/frontend
yarn install
yarn cap:android         # builds React + opens Android Studio
```
Wait for Android Studio to finish Gradle sync (first time = 5–10 min).

### 2.2  Create your upload keystore  (do this ONCE — keep this file safe forever)
In Android Studio:

1. Menu → **Build → Generate Signed App Bundle / APK…**
2. Pick **Android App Bundle** → Next.
3. Under **Key store path**, click **Create new…**
4. Fill in:
   - **Key store path**: `~/keystores/huatpick-upload.jks`  *(somewhere outside the repo — DO NOT commit this file)*
   - **Password / Confirm**: pick a strong password (write it in 1Password / a vault)
   - **Alias**: `huatpick-upload`
   - **Key password**: same as keystore password (simpler)
   - **Validity**: `25` years
   - **First and Last Name**: `JH Creative Enterprise`
   - **Organizational unit**: `Apps`
   - **Organization**: `JH Creative Enterprise`
   - **City**: your city
   - **State / Country**: your state, `MY`
5. Click **OK**. The `.jks` file is now created.

> ⚠️ **If you lose this keystore file or password, you can NEVER update the app on Play Store again** (you'd have to publish a brand-new listing under a new package name). Back it up to encrypted cloud storage right now.

### 2.3  Generate the release bundle

1. Build menu → Generate Signed App Bundle → pick the keystore you just made.
2. Build variants: select `release` only.
3. Destination folder: stays default.
4. Click **Create**.

After ~3 minutes you'll see:
```
android/app/release/app-release.aab
```
This is the file you upload to Play Store. Typical size: 5–15 MB.

### 2.4  Test it on a real device first
```bash
# generate a debug APK for sideloading
cd /path/to/huatpick/frontend/android
./gradlew assembleRelease
adb install app/build/outputs/apk/release/app-release.apk
```
(Or use the `bundletool` to produce an APK from the AAB — but the easiest sanity check is just **Build → Run** on a real phone connected via USB.)

---

## STEP 3 — Fill the Data Safety form  (20 min)

In Play Console → your app → **App content → Data Safety → Manage**.
Below are **every answer you need**. Paste/click exactly these.

### Section 1: Data collection and security

| Question | Answer |
|---|---|
| Does your app collect or share any of the required user data types? | **Yes** |
| Is all of the user data collected by your app encrypted in transit? | **Yes** |
| Do you provide a way for users to request that their data be deleted? | **Yes** (via email to turyoungpotato@gmail.com — Privacy Policy explains this) |

### Section 2: Data types — what HuatPick collects

You'll see a checklist of data categories. Mark these as **Collected**:

| Category | Item | Purpose | Optional/Required | Shared? |
|---|---|---|---|---|
| **Personal info** | Email address | Account management, Communications | Required | No |
| **Personal info** | Name | Account management | Optional | No |
| **Personal info** | User IDs | Account management, App functionality | Required | No |
| **Financial info** | User payment info | App functionality, Purchase history | Required | **Yes — Stripe** (Service Providers) |
| **App activity** | App interactions | Analytics, App functionality | Required | No |
| **App info & performance** | Crash logs | App functionality | Required | No |
| **Device or other IDs** | Device or other IDs | Analytics, Fraud prevention | Required | No |

Everything else (Location, Personal financials, Photos, Health, Messages, Audio, Files, Calendar, Contacts, Web history, etc.) → **Not collected**.

### Section 3: Security practices

| Question | Answer |
|---|---|
| Is data encrypted in transit? | **Yes** (HTTPS/TLS for all `/api/*` calls) |
| Can users request that their data be deleted? | **Yes** (email request → deleted within 30 days, see Privacy Policy §4) |
| Independent security review? | **No** (small app, not yet audited — that's fine) |
| Committed to Google Play Families Policy? | **No** (HuatPick is 18+, not for families) |

### Section 4: Save and submit

Click **Save** at the end of each step, then **Submit** at the very end. The form turns green ✓.

---

## STEP 4 — Other required Play Console sections  (30 min)

While you're in Play Console, you also need to fill these:

### 4.1  Privacy Policy URL
Setup → App content → **Privacy Policy** → URL:
```
https://<your-deployed-emergent-url>/privacy
```

### 4.2  App access
Do you have any sign-in restrictions? → **All functionality is available without special access**
*(Don't tick "restricted access" — your sign-up is open to anyone with email.)*

### 4.3  Ads
Does your app contain ads? → **No, my app does not contain ads** ✓

### 4.4  Content rating questionnaire (IARC)
Setup → App content → **Content ratings** → Start questionnaire.

Category to pick: **Reference, News, or Educational** *(not Casino/Gambling — we don't take real bets)*.

Answers:
| Question | Answer |
|---|---|
| Does this app contain violence? | No |
| Does this app contain sexual content? | No |
| Does this app contain profanity? | No |
| Does this app feature gambling? | **No, simulated gambling without real prizes** |
| Does this app allow users to interact? | No |
| Does this app share location? | No |
| Does this app allow users to purchase digital content? | **Yes** (VIP subscription + credit packs) |

Resulting rating should be **Teen** in IARC, **PEGI 12+** in Europe — but you can manually set **Mature 17+** to match the 18+ requirement in your Terms.

### 4.5  Target audience
Setup → App content → **Target audience and content** → select **18 and over** only.

### 4.6  News app declaration
Not a news app → leave blank.

### 4.7  Store listing
Main store listing → fill in:
- **App name**: `HuatPick: Lottery AI Picks`
- **Short description**: paste from `/app/STORE_LISTING.md` §4
- **Full description**: paste from `/app/STORE_LISTING.md` §4
- **App icon**: upload `/app/frontend/assets/icon-512.png`
- **Feature graphic**: upload `/app/frontend/assets/feature-graphic.png`
- **Phone screenshots**: at least 2 (more is better — see screenshot capture instructions below)

### 4.8  Capture phone screenshots
Easiest way:

1. Open the deployed app in **Chrome**.
2. Open **DevTools** (F12) → click **Toggle device toolbar** (Ctrl+Shift+M).
3. Pick **"Pixel 8 Pro"** (1080×2400) or **"iPhone 14 Pro Max"** (1290×2796).
4. Navigate to each screen → DevTools `⋮` menu → **"Capture full-size screenshot"**.
5. Recommended screens (5 total):
   - **Home** (with hero "Generate lucky numbers in 2 seconds")
   - **Generate / 4D** (mid-spin animation — pause animations or capture at right moment)
   - **Result modal** (showing the bold lucky digits + AI reasoning)
   - **History**
   - **VIP page** (shows the three tiers + checkout button)

Save them as PNG, name them `01_home.png`, `02_generate.png` etc., and upload in the same order.

---

## STEP 5 — Upload the `.aab` and submit  (15 min)

1. Play Console → your app → **Production → Create new release**.
2. Click **Upload** → drag your `app-release.aab` from `android/app/release/`.
3. **Release name**: `1.0 (1)` (auto-filled).
4. **Release notes** (paste from `STORE_LISTING.md` §4 "What's new" section).
5. Click **Next → Save**.
6. Click **Review release** → fix any policy warnings → **Start rollout to Production**.

**Recommended: do Internal Testing first** instead of Production:
- Same upload flow but pick **Internal testing** track.
- Add up to 100 internal tester emails (yourself + friends).
- **No review needed** — they can install via opt-in link within minutes.
- Once stable, promote the same `.aab` to Production with one click.

---

## STEP 6 — Wait for review  (1–7 days for first submission)

First submissions are manually reviewed and can take up to **7 days** (sometimes 14). Subsequent updates usually approve within hours.

Common rejection reasons (all already handled in this repo):
- ❌ Missing Privacy Policy URL → ✅ done
- ❌ Inappropriate age rating → ✅ marked 18+
- ❌ Missing Data Safety form → ✅ template above
- ❌ Using lottery brand logos (Magnum, Sports Toto) in screenshots → don't use them
- ❌ Implying guaranteed winnings → ✅ Terms §3 says no guarantee

---

## Done. What I need from you to help further:

When you've started the Play Console setup, share back:
1. ✅ The deployed app URL (after you click Deploy in Emergent) — so I can put it into `Privacy/Terms` and the screenshot capture works
2. Any **policy warnings** Play Console flags during submission — I can adjust the app code if anything trips a check
3. The **package name** if you ended up choosing something other than `com.huatpick.app` — I'll update the Capacitor config

I cannot help with:
- Paying the $25 (your credit card)
- Generating the keystore (must be on your machine, must stay private)
- Filling the form (your Play Console login)

But every answer is now sitting above, ready to copy-paste.
