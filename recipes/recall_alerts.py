"""Product recalls and safety alerts for your keywords (products, brands, ingredients) from
FDA, CPSC, Health Canada, UK FSA/OPSS and the EU Safety Gate → recalls.csv.

Cost: about $0.002 per recall.
Usage: python recall_alerts.py "peanut,lithium battery" 30      (keywords, days back)
"""

import csv
import sys

from _apify import run

keywords = (sys.argv[1] if len(sys.argv) > 1 else "peanut").split(",")
days = int(sys.argv[2]) if len(sys.argv) > 2 else 30

recalls = run(
    "tacps126~recalls-radar",
    {"keywords": [k.strip() for k in keywords], "postedWithinDays": days, "maxItems": 200},
)

with open("recalls.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "publisher", "category", "title", "company", "hazard", "url"])
    for r in recalls:
        w.writerow(
            [
                r.get("date"),
                r.get("country"),
                r.get("category"),
                r.get("title"),
                r.get("company"),
                r.get("hazard"),
                r.get("url"),
            ]
        )
print(f"{len(recalls)} recalls in the last {days} days → recalls.csv")
