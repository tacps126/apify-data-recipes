"""Several Shopify stores > the biggest discounts across all of them, best first > deals.csv.

Cost: about $0.0004 per product returned (only the top results are billed).
Usage: python shopify_best_deals.py stores.txt 50      (one domain per line, how many deals)
"""

import csv
import sys

from _apify import run

stores = (
    [line.strip() for line in open(sys.argv[1]) if line.strip()]
    if len(sys.argv) > 1
    else ["allbirds.com", "gymshark.com", "colourpop.com"]
)
top = int(sys.argv[2]) if len(sys.argv) > 2 else 50

products = run(
    "tacps126~shopify-products",
    {
        "startUrls": stores,
        "onlyOnSale": True,
        "onlyAvailable": True,
        "sortBy": "discountHigh",
        "maxItems": top,
    },
)

with open("deals.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["store", "title", "price", "compareAtPrice", "discountPercent", "currency", "url"])
    for p in products:
        w.writerow(
            [
                p.get("store"),
                p.get("title"),
                p.get("price"),
                p.get("compareAtPrice"),
                p.get("discountPercent"),
                p.get("currency"),
                p.get("url"),
            ]
        )
print(f"{len(products)} deals across {len(stores)} stores > deals.csv")
