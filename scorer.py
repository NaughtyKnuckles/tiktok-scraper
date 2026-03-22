# scorer.py
import re

def parse_percent(text):
    match = re.search(r"(\d+\.?\d*)%", str(text))
    return float(match.group(1)) if match else 0

def parse_number(text):
    text = str(text).strip().replace(",", "")
    if "K" in text:
        return float(re.sub(r"[^\d.]", "", text.replace("K", ""))) * 1000
    if "M" in text:
        return float(re.sub(r"[^\d.]", "", text.replace("M", ""))) * 1_000_000
    try:
        return float(re.sub(r"[^\d.]", "", text))
    except:
        return 0

def score_product(product):
    ctr = parse_percent(product.get("ctr", "0"))     # click-through rate
    cvr = parse_percent(product.get("cvr", "0"))     # conversion rate
    popularity = parse_number(product.get("popularity", "0"))

    # Higher CTR = more people click = better content opportunity
    ctr_score = min(ctr / 10, 1.0) * 40

    # Higher CVR = more people buy = better commission potential
    cvr_score = min(cvr / 15, 1.0) * 40

    # Popularity gives a tiebreaker
    pop_score = min(popularity / 5000, 1.0) * 20

    return round(ctr_score + cvr_score + pop_score, 1)

def rank_products(products):
    for p in products:
        p["score"] = score_product(p)
    return sorted(products, key=lambda x: x["score"], reverse=True)