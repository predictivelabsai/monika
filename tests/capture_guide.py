"""
Capture User Guide Screenshots

Launches a headless browser, logs in, navigates every module,
and saves screenshots to static/guide/.

Usage:
    # App must be running first: python app.py
    python tests/capture_guide.py

    # Or start app automatically:
    python tests/capture_guide.py --start-app
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
GUIDE_DIR = ROOT / "static" / "guide"
BASE_URL = "http://localhost:5010"
EMAIL = "joe@ashland-hill.com"
PASSWORD = "test1234"


PAGES = [
    ("00_login.png",      None,                         "Login page"),
    ("01_welcome.png",    "__after_login__",             "Welcome screen"),
    ("02_deals.png",      "/module/deals",              "Deal Pipeline"),
    ("03_deal_new.png",   "/module/deal/new",           "New Deal form"),
    ("04_contacts.png",   "/module/contacts",           "Contacts"),
    ("05_sales.png",      "/module/sales",              "Sales & Collections"),
    ("06_estimates.png",  "/module/estimates",           "Sales Estimates"),
    ("07_risk.png",       "/module/risk",               "Risk Scoring"),
    ("08_risk_form.png",  "/module/risk/new",           "Risk Assessment form"),
    ("09_budget.png",     "/module/budget",             "Smart Budget"),
    ("10_schedule.png",   "/module/schedule",           "Scheduling"),
    ("11_audience.png",   "/module/audience",           "Audience Intel"),
    ("12_dataroom.png",   "/module/dataroom",           "Data Room"),
    ("13_checklist.png",  "__checklist_detail__",       "Closing Checklist"),
    ("14_talent.png",     "/module/talent",             "Talent Intel"),
]


async def run():
    from playwright.async_api import async_playwright

    GUIDE_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})

        # --- Login page screenshot ---
        await page.goto(f"{BASE_URL}/login")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=str(GUIDE_DIR / "00_login.png"))
        print("  captured  00_login.png")

        # --- Login ---
        await page.fill('input[name="email"]', EMAIL)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_url(f"{BASE_URL}/")
        await asyncio.sleep(2)

        # --- Welcome screen ---
        await page.screenshot(path=str(GUIDE_DIR / "01_welcome.png"))
        print("  captured  01_welcome.png")

        # --- Module pages ---
        for filename, path, label in PAGES:
            if path is None or path == "__after_login__":
                continue

            if path == "__checklist_detail__":
                # Find the deal with a checklist
                deal_id = await page.evaluate("""
                    async () => {
                        const r = await fetch('/module/dataroom');
                        const html = await r.text();
                        const m = html.match(/hx-get="\\/module\\/dataroom\\/([^"]+)"/);
                        return m ? m[1] : null;
                    }
                """)
                if deal_id:
                    path = f"/module/dataroom/{deal_id}"
                else:
                    print(f"  skipped   {filename} (no checklist found)")
                    continue

            # Navigate via HTMX swap
            await page.evaluate(f"""
                () => {{
                    var c = document.getElementById('center-content');
                    var ch = document.getElementById('center-chat');
                    if (c && ch) {{ ch.style.display = 'none'; c.style.display = 'block'; }}
                    htmx.ajax('GET', '{path}', {{target: '#center-content', swap: 'innerHTML'}});
                    var h = document.getElementById('center-title');
                    if (h) h.textContent = '{label}';
                }}
            """)
            await asyncio.sleep(1.5)
            await page.screenshot(path=str(GUIDE_DIR / filename))
            print(f"  captured  {filename}")

        # --- Chat: help command ---
        # Switch back to chat
        await page.evaluate("""
            () => {
                var c = document.getElementById('center-content');
                var ch = document.getElementById('center-chat');
                if (c) c.style.display = 'none';
                if (ch) ch.style.display = 'block';
                var h = document.getElementById('center-title');
                if (h) h.textContent = 'AI Chat';
            }
        """)
        await asyncio.sleep(1)

        # Type help command
        chat_input = page.locator("#chat-input")
        if await chat_input.count() > 0:
            await chat_input.fill("help")
            await chat_input.press("Enter")
            await asyncio.sleep(3)
            await page.screenshot(path=str(GUIDE_DIR / "15_chat_help.png"))
            print("  captured  15_chat_help.png")

            # Type portfolio command
            await chat_input.fill("portfolio")
            await chat_input.press("Enter")
            await asyncio.sleep(3)
            await page.screenshot(path=str(GUIDE_DIR / "16_chat_portfolio.png"))
            print("  captured  16_chat_portfolio.png")

        await browser.close()


def main():
    start_app = "--start-app" in sys.argv
    app_proc = None

    if start_app:
        print("Starting app...")
        app_proc = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=str(ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(5)

    print(f"\nCapturing User Guide screenshots to {GUIDE_DIR}/\n")

    try:
        asyncio.run(run())
    finally:
        if app_proc:
            app_proc.terminate()
            app_proc.wait()
            print("\nApp stopped.")

    print(f"\nDone — {len(list(GUIDE_DIR.glob('*.png')))} screenshots in static/guide/")


if __name__ == "__main__":
    main()
