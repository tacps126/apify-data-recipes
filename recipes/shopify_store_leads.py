"""A list of websites → the Shopify stores among them with country, currency, product
count, price range and contact details → stores.csv. Non-Shopify sites are skipped free.

Cost: about $0.004 per Shopify store.
Usage: python shopify_store_leads.py sites.txt        (one domain or URL per line)
"""

import csv
import sys

from _apify import run

sites = (
    [line.strip() for line in open(sys.argv[1]) if line.strip()]
    if len(sys.argv) > 1
    else [
        "allbirds.com",
        "gymshark.com",
        "brooklinen.com",
    ]
)

stores = run(
    "tacps126~shopify-store-analyzer",
    {
        "startUrls": sites,
        "includeContacts": True,
        "maxItems": len(sites),
    },
)

with open("stores.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "store",
            "domain",
            "country",
            "currency",
            "products",
            "priceMedian",
            "email",
            "phone",
            "instagram",
        ]
    )
    for s in stores:
        cat = s.get("catalog") or {}
        w.writerow(
            [
                s.get("storeName"),
                s.get("domain"),
                s.get("country"),
                s.get("currency"),
                s.get("productCount"),
                cat.get("priceMedian"),
                s.get("primaryEmail"),
                s.get("primaryPhone"),
                s.get("instagram"),
            ]
        )
print(f"{len(stores)} Shopify stores (of {len(sites)} sites) → stores.csv")
