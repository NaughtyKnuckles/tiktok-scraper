# main.py
import asyncio
from scraper import scrape_trending_products
from scorer import rank_products
from saver import save_to_csv
from notifier import notify          # add this

async def run():
    print("=== TikTok Affiliate Product Scraper ===\n")

    products = await scrape_trending_products()
    if not products:
        print("No products scraped.")
        return

    ranked = rank_products(products)

    print("\n--- TOP 15 PRODUCTS TODAY ---")
    for i, p in enumerate(ranked[:15], 1):
        print(f"{i:>2}. [Score {p['score']:>5}/100] {p['name'][:45]:<45} | CTR: {p['ctr']:>6} | CVR: {p['cvr']:>6} | Pop: {p['popularity']}")

    save_to_csv(ranked)
    notify(ranked)                   # add this

asyncio.run(run())