# HuatPick — Signed Android `.aab` Build (Copy-Paste Edition)

**Goal:** Produce `app-release.aab` and upload it to Google Play Console → Internal Testing.

**You will do this on your LOCAL machine** (Mac / Windows / Linux with Android Studio). This container cannot produce signed bundles.

---

## Prerequisites (one-time)
- [x] Android Studio Hedgehog (2023.1.1) or newer — [download](https://developer.android.com/studio)
- [x] JDK 17 (Android Studio installs this automatically as a bundled JBR)
- [x] Node 18 + Yarn 1.22
- [x] The full `/app` repo cloned to your local machine

Verify:
```bash
java -version       # should report 17.x
node -v             # should report v18 or v20
yarn -v             # should report 1.22.x
```

---

## Step 1 — Generate your upload keystore (do this ONCE, keep forever)

> ⚠️ **CRITICAL**: This `.jks` file is your **only** way to publish updates to Play Store under this app. If you lose it, you lose the listing. Back it up to a password manager / encrypted cloud drive.

From the repo root on your local machine:

```bash
cd frontend/android

# Replace YOUR_NAME and YOUR_COMPANY with real values. You'll be asked for two passwords —
# pick strong unique ones and store them in 1Password / Bitwarden.
keytool -genkey -v \
  -keystore huatpick-release.jks \
  -alias huatpick \
  -keyalg RSA -keysize 2048 -validity 36500 \
  -dname "CN=YOUR_NAME, O=JH Creative Enterprise, C=MY"
```

The tool will ask:
1. **Keystore password** (twice) — save this
2. **Key password** — press ENTER to reuse the keystore password, OR type a different one (save it too)

A file `huatpick-release.jks` now exists in `frontend/android/`. **Back it up immediately.**

---

## Step 2 — Wire the keystore into Gradle

```bash
# still in frontend/android/
cp key.properties.template key.properties
```

Open `key.properties` in any editor and fill in the four values:

```properties
storeFile=huatpick-release.jks
storePassword=<paste keystore password>
keyAlias=huatpick
keyPassword=<paste key password (or same as keystore password)>
```

Save. The Gradle script in `app/build.gradle` already picks this up automatically.

> Both `key.properties` and `*.jks` are git-ignored — they will never leak into your repo.

---

## Step 3 — Make sure the web build points at your PRODUCTION backend

Edit `frontend/.env`:

```env
REACT_APP_BACKEND_URL=https://<your-deployed-emergent-domain>
```

> This is baked into the bundle at build time. Use your **deployed** URL, NOT the preview URL — Google will reject the app if API calls fail in production.

---

## Step 4 — Build the React bundle + sync into Android

```bash
cd frontend
yarn install            # only if you haven't already
yarn build              # produces frontend/build/
npx cap sync android    # copies build/ into android/app/src/main/assets/public
```

---

## Step 5 — Build the signed `.aab`

Two equivalent options. Pick one:

### Option A — Command line (fastest, recommended)
```bash
cd frontend/android
./gradlew bundleRelease
```

Wait 2-5 minutes (first run downloads Gradle ~200 MB). On success:

```
BUILD SUCCESSFUL
```

Your file is at:
```
frontend/android/app/build/outputs/bundle/release/app-release.aab
```

### Option B — Android Studio GUI
1. Open `frontend/android/` in Android Studio (`File → Open`, pick the folder).
2. Wait for Gradle sync to finish.
3. `Build → Generate Signed Bundle / APK… → Android App Bundle → Next`
4. Pick the existing `huatpick-release.jks` (it auto-fills from `key.properties`).
5. Pick `release` build variant → `Finish`.
6. File appears at the same path as Option A.

---

## Step 6 — Upload to Play Console

1. Go to [Play Console](https://play.google.com/console) → your app → **Testing → Internal testing → Create new release**.
2. Drag `app-release.aab` into the upload box.
3. Fill in **Release name** (e.g. `1.0.0`) and **Release notes** (copy from `/app/STORE_LISTING.md`).
4. Click **Save → Review release → Start rollout to Internal testing**.
5. Add your own Gmail to the internal testers list → install via the opt-in URL Play Console shows you.

🎉 You now have HuatPick installed from the Play Store on your test device.

---

## When you ship an update later

Bump version numbers in `frontend/android/app/build.gradle`:

```gradle
versionCode 2          // integer, must increase every upload
versionName "1.0.1"    // user-facing string
```

Then repeat Steps 4 → 5 → 6. Same keystore, same `key.properties` — no need to regenerate anything.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `keytool: command not found` | JDK not on PATH. Run `/Applications/Android\ Studio.app/Contents/jbr/Contents/Home/bin/keytool` (macOS) or `"C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe"` (Windows). |
| Gradle: `SDK location not found` | Open `android/` once in Android Studio — it will create `local.properties` with your SDK path automatically. |
| `Cannot recover key` during signing | `keyPassword` in `key.properties` is wrong. Try setting it equal to `storePassword`. |
| Play Console: "Your AAB is signed with the wrong key" | You already uploaded a different `.jks` before. Either find the original `.jks` from your backups, OR enable Play App Signing key reset (Play Console → Setup → App integrity → Request upload key reset). |
| App installs but shows blank white screen | `REACT_APP_BACKEND_URL` in `frontend/.env` was wrong at build time. Fix the URL → re-run Step 4 → Step 5. |

---

## What's already set up for you

| Item | Status |
|---|---|
| Capacitor Android project | ✅ `/app/frontend/android/` |
| `applicationId` (Play Store bundle ID) | ✅ `com.huatpick.app` |
| App icon (all densities) | ✅ Generated via `@capacitor/assets` |
| Splash screen | ✅ White background, `splash` resource |
| `versionCode 1 / versionName "1.0"` | ✅ Ready for first release |
| Gradle signing config | ✅ Reads `key.properties` automatically (this PR) |
| `.gitignore` for keystore + properties | ✅ This PR |
| Privacy Policy URL | ✅ `/privacy` (publicly accessible) |
| Account deletion URL | ✅ `/delete-account` (publicly accessible) — **paste into Play Console Data Safety** |
| Terms URL | ✅ `/terms` |

**You only need to do Steps 1–6 above. Everything else is wired.**
