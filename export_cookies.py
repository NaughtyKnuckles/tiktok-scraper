# export_cookies.py
# Run this ONCE on your local PC to export your TikTok login cookies
import asyncio
import json
from playwright.async_api import async_playwright

async def export():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./browser-session",
            channel="chrome",
            headless=False,
        )
        page = await context.new_page()
        await page.goto("https://ads.tiktok.com/business/creativecenter/top-products/pc/en")
        await asyncio.sleep(5)

        # Save all cookies to a file
        cookies = await context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)

        print(f"Exported {len(cookies)} cookies to cookies.json")
        await context.close()

asyncio.run(export())