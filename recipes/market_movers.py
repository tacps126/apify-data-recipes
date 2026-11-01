"""Prediction markets that moved the most in the last 24 hours on Kalshi and Polymarket, with
probability, change and volume → movers.csv. Run it hourly or daily for a news-signal feed.

Cost: about $0.003 per market.
Usage: python market_movers.py "politics,economics" 10000      (categories, minimum 24h volume)
"""

import csv
import sys

from _apify import run

categories = (sys.argv[1] if len(sys.argv) > 1 else "politics,economics").split(",")
min_volume = float(sys.argv[2]) if len(sys.argv) > 2 else 10000

markets = run(
    "tacps126~prediction-markets",
    {
        "platforms": ["kalshi", "polymarket"],
        "categories": [c.strip() for c in categories],
        "minVolume24h": min_volume,
        "sortBy": "move24h",
        "maxItems": 100,
    },
)

with open("movers.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        ["platform", "event", "outcome", "probability", "change_24h", "volume_24h", "closes", "url"]
    )
    for m in markets:
        w.writerow(
            [
                m.get("platform"),
                m.get("eventTitle") or m.get("question"),
                m.get("outcome"),
                m.get("probability"),
                m.get("change24h"),
                m.get("volume24h"),
                (m.get("closeTime") or "")[:10],
                m.get("url"),
            ]
        )
print(f"{len(markets)} markets, biggest 24h moves first → movers.csv")
