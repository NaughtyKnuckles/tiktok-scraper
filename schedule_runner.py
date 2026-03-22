# schedule_runner.py
import schedule
import time
import asyncio
from scraper import scrape_trending_products
from scorer import rank_products
from saver import save_to_csv
from notifier import notify

def run_scraper():
    print("Running scheduled scrape...")
    async def job():
        products = await scrape_trending_products()
        ranked = rank_products(products)
        save_to_csv(ranked)
        notify(ranked)
    asyncio.run(job())

# Run every day at 8:00 AM
schedule.every().day.at("08:00").do(run_scraper)

print("Scheduler running — will scrape every day at 8:00 AM. Keep this window open.")
while True:
    schedule.run_pending()
    time.sleep(60)