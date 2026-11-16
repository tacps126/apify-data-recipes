"""What sells on Amazon for your keywords: products ranked by "bought in past month", with price,
discount and rating > amazon_products.csv. Product research and competitor checks.

Cost: about $0.001 per product.
Usage: python amazon_best_sellers.py "standing desk,desk lamp" us 4
       (searches, marketplace: us uk de fr it es ca in jp au mx br nl ae, lowest star rating)
"""

import csv
import re
import sys

from _apify import run

searches = (sys.argv[1] if len(sys.argv) > 1 else "standing desk").split(",")
marketplace = sys.argv[2] if len(sys.argv) > 2 else "us"
min_rating = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0


def bought(text):
    """'10K+ bought in past month' > 10000 (0 when Amazon shows nothing)."""
    m = re.search(r"([\d.]+)\s*([KkMm]?)\+?", text or "")
    if not m:
        return 0
    return int(float(m.group(1)) * {"k": 1_000, "m": 1_000_000}.get(m.group(2).lower(), 1))


items = run(
    "tacps126~amazon-products",
    {
        "searchTerms": [s.strip() for s in searches],
        "marketplace": marketplace,
        "maxPagesPerSearch": 3,
        "skipSponsored": True,
        "minRating": min_rating,
        "maxItems": 300,
    },
)
items.sort(
    key=lambda p: (bought(p.get("boughtPastMonth")), p.get("ratingsCount") or 0), reverse=True
)

with open("amazon_products.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "search",
            "title",
            "asin",
            "price",
            "list_price",
            "discount_%",
            "rating",
            "ratings",
            "bought_past_month",
            "url",
        ]
    )
    for p in items:
        price, list_price = p.get("price"), p.get("listPrice")
        off = (
            round(100 * (1 - price / list_price))
            if price and list_price and list_price > price
            else ""
        )
        w.writerow(
            [
                p.get("searchTerm"),
                p.get("title"),
                p.get("asin"),
                price,
                list_price,
                off,
                p.get("rating"),
                p.get("ratingsCount"),
                p.get("boughtPastMonth"),
                p.get("url"),
            ]
        )
print(f"{len(items)} products, best sellers first > amazon_products.csv")
