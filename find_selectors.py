# find_selectors.py
from bs4 import BeautifulSoup
from collections import Counter
import re

with open("debug.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find all unique class names that appear on divs/li elements
# Product cards are almost always repeated divs with the same class
all_classes = []
for tag in soup.find_all(["div", "li", "article"]):
    for cls in tag.get("class", []):
        all_classes.append(cls)

# Count how often each class appears — product cards repeat many times
counts = Counter(all_classes)

print("=== CLASSES THAT APPEAR 5–50 TIMES (likely product cards) ===")
for cls, count in sorted(counts.items(), key=lambda x: -x[1]):
    if 5 <= count <= 50:
        print(f"  .{cls}  →  appears {count} times")

print("\n=== CLASSES CONTAINING 'product' or 'card' or 'item' ===")
for cls, count in sorted(counts.items(), key=lambda x: -x[1]):
    if any(kw in cls.lower() for kw in ["product", "card", "item", "trending"]):
        print(f"  .{cls}  →  appears {count} times")

print("\n=== ALL DATA-E2E ATTRIBUTES ON PAGE ===")
for tag in soup.find_all(attrs={"data-e2e": True}):
    print(f"  [{tag.name}] data-e2e='{tag['data-e2e']}'")