# scraper.py
import asyncio
import os
import json
from playwright.async_api import async_playwright
from datetime import datetime

PRODUCTS_URL = "https://ads.tiktok.com/business/creativecenter/top-products/pc/en"

async def scrape_trending_products():
    products = []

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./browser-session",
            headless=True,                        # no screen on GitHub servers
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",                   # required on Linux servers
                "--disable-dev-shm-usage",        # prevents memory crashes
                "--disable-gpu",
            ]
        )
        page = await context.new_page()

        # Load saved cookies if they exist (we'll set this up next)
        if os.path.exists("cookies.json"):
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print("Loaded saved cookies")

        print("Navigating to Top Products...")
        await page.goto(PRODUCTS_URL, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(6)

        if "login" in page.url:
            print("ERROR: Not logged in — cookies may have expired.")
            await context.close()
            return []

        # Close tutorial popup if it appears
        try:
            skip_btn = page.locator("text=Skip")
            if await skip_btn.count() > 0:
                await skip_btn.click()
                await asyncio.sleep(2)
        except:
            pass

        print(f"On page: {page.url}")

        all_products = []
        page_num = 1

        while True:
            print(f"\nScraping page {page_num} of 22...")
            await asyncio.sleep(3)

            await page.wait_for_selector("tr", timeout=15000)
            rows = await page.query_selector_all("tr")

            page_products = []
            for row in rows:
                try:
                    cells = await row.query_selector_all("td")
                    if len(cells) < 4:
                        continue

                    product_cell    = cells[0]
                    popularity_cell = cells[1]
                    change_cell     = cells[2]
                    ctr_cell        = cells[3]
                    cvr_cell        = cells[4] if len(cells) > 4 else None
                    cpa_cell        = cells[5] if len(cells) > 5 else None

                    product_text = await product_cell.inner_text()
                    lines    = [l.strip() for l in product_text.strip().split("\n") if l.strip()]
                    name     = lines[0] if lines else "Unknown"
                    category = lines[1] if len(lines) > 1 else ""

                    popularity = (await popularity_cell.inner_text()).strip()
                    change     = (await change_cell.inner_text()).strip()
                    ctr        = (await ctr_cell.inner_text()).strip()
                    cvr        = (await cvr_cell.inner_text()).strip() if cvr_cell else ""
                    cpa        = (await cpa_cell.inner_text()).strip() if cpa_cell else ""

                    product = {
                        "name": name,
                        "category": category,
                        "popularity": popularity,
                        "popularity_change": change,
                        "ctr": ctr,
                        "cvr": cvr,
                        "cpa": cpa,
                        "page": page_num,
                        "scraped_at": datetime.now().isoformat(),
                    }
                    page_products.append(product)
                    print(f"  {name[:50]} | CTR: {ctr} | CVR: {cvr}")

                except Exception as e:
                    continue

            all_products.extend(page_products)
            print(f"  Page {page_num} done — {len(page_products)} products")

            try:
                next_btn = page.locator("li[title='Next Page']")
                count = await next_btn.count()

                if count == 0:
                    print(f"\nNo more pages. Done after {page_num} page(s).")
                    break

                is_disabled = await next_btn.get_attribute("aria-disabled")
                if is_disabled == "true":
                    print(f"\nReached last page. Done after {page_num} page(s).")
                    break

                if page_num >= 22:
                    print("\nReached page 22 cap.")
                    break

                await next_btn.click()
                page_num += 1
                await asyncio.sleep(3)

            except Exception as e:
                print(f"Stopping at page {page_num}: {e}")
                break

        await context.close()
        return all_products


if __name__ == "__main__":
    results = asyncio.run(scrape_trending_products())
    print(f"\nTotal products scraped: {len(results)}")