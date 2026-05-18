"""Capture 5 polished Play Store-ready screenshots from the live HuatPick app.

Output: /app/frontend/assets/screenshots/01_home.png ... 05_vip.png
Dimensions: 1080x1920 (Play Store recommended portrait phone screenshot)
"""
import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright

OUT_DIR = Path("/app/frontend/assets/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE = "https://mobile-app-builder-349.emergent.host"
EMAIL = f"shot{int(time.time())}@huatpick.com"
PASSWORD = "lucky123"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1080, "height": 1920},
            device_scale_factor=1,
            user_agent="Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            is_mobile=True,
            has_touch=True,
        )
        page = await ctx.new_page()

        # Register a fresh user
        await page.goto(f"{BASE}/auth", wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2500)
        await page.click('[data-testid="tab-register"]')
        await page.wait_for_timeout(400)
        await page.fill('[data-testid="register-name-input"]', "Aisha")
        await page.fill('[data-testid="login-email-input"]', EMAIL)
        await page.fill('[data-testid="login-password-input"]', PASSWORD)
        await page.click('[data-testid="login-submit-button"]')
        await page.wait_for_timeout(3500)

        # 1) HOME
        await page.goto(f"{BASE}/", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(OUT_DIR / "01_home.png"), full_page=False)
        print("✓ 01_home.png")

        # 2) GENERATE 4D mid-spin (capture the spinning digits — best "alive" shot)
        await page.goto(f"{BASE}/generate/4d", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        # Click spin & capture right when digits start moving
        await page.click('[data-testid="spin-button"]')
        await page.wait_for_timeout(500)  # mid-spin
        await page.screenshot(path=str(OUT_DIR / "02_generate_spinning.png"), full_page=False)
        print("✓ 02_generate_spinning.png")

        # 3) RESULT modal with lucky numbers
        await page.wait_for_timeout(2500)  # wait for result modal
        await page.screenshot(path=str(OUT_DIR / "03_result.png"), full_page=False)
        print("✓ 03_result.png")

        # 4) HISTORY
        try:
            await page.click('[data-testid="close-result"]')
        except Exception:
            pass
        await page.wait_for_timeout(500)
        # generate one more so history has 2+ entries
        await page.goto(f"{BASE}/generate/6_58", wait_until="networkidle")
        await page.wait_for_timeout(1200)
        await page.click('[data-testid="spin-button"]')
        await page.wait_for_timeout(2500)
        try:
            await page.click('[data-testid="close-result"]')
        except Exception:
            pass
        await page.wait_for_timeout(500)
        await page.click('[data-testid="nav-history"]')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(OUT_DIR / "04_history.png"), full_page=False)
        print("✓ 04_history.png")

        # 5) VIP
        await page.click('[data-testid="nav-vip"]')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(OUT_DIR / "05_vip.png"), full_page=False)
        print("✓ 05_vip.png")

        await browser.close()
        print(f"\nAll screenshots saved to {OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
