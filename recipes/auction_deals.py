"""Court, bank and government property auctions near a place, scored against similar lots and
your budget > auction_deals.csv. Schedule it weekly with a monitor name to get only new lots and
price cuts.

Cost: about $0.015 per lot.
Usage: python auction_deals.py Milano 25 250000      (place, radius in km, maximum budget in EUR)
"""

import csv
import sys

from _apify import run

place = sys.argv[1] if len(sys.argv) > 1 else "Milano"
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 25
budget = float(sys.argv[3]) if len(sys.argv) > 3 else 250000

lots = run(
    "tacps126~auctions-radar",
    {
        "location": place,
        "radiusKm": radius,
        "budgetMax": budget,
        "assetTypes": ["apartment", "house"],
        "profile": "bargainHunter",
        "maxItems": 100,
    },
)

with open("auction_deals.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "score",
            "verdict",
            "title",
            "city",
            "price",
            "currency",
            "valuation",
            "area_sqm",
            "price_per_sqm",
            "possession",
            "auction_date",
            "distance_km",
            "url",
        ]
    )
    for x in lots:
        w.writerow(
            [
                x.get("score"),
                x.get("headline"),
                x.get("title"),
                x.get("city"),
                x.get("price"),
                x.get("currency"),
                x.get("valuation"),
                x.get("areaSqm"),
                x.get("pricePerSqm"),
                x.get("possession"),
                (x.get("auctionDate") or "")[:10],
                x.get("distanceKm"),
                x.get("url"),
            ]
        )
print(f"{len(lots)} lots, best score first > auction_deals.csv")
