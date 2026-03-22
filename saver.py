# saver.py
import csv, os
from datetime import datetime

def save_to_csv(products, folder="results"):
    os.makedirs(folder, exist_ok=True)
    if not products:
        print("No products to save.")
        return

    filename = f"{folder}/products_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    fields = ["name", "category", "popularity", "popularity_change", "ctr", "cvr", "cpa", "score", "page", "scraped_at"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(products)

    print(f"Saved {len(products)} products → {filename}")
    return filename