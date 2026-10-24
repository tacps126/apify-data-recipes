"""New papers, preprints and patents for your topics → research.csv (merged across sources).

Run it daily or weekly with only_new on: each run returns only what earlier runs didn't.
Cost: about $0.003 per result.
Usage:
  python research_alerts.py "solid state battery" "sulfide electrolyte" [--days 7] [--influential]
"""

import argparse
import csv

from _apify import run

p = argparse.ArgumentParser()
p.add_argument("queries", nargs="+")
p.add_argument("--days", type=int, default=7, help="only results published in the last N days")
p.add_argument(
    "--influential", action="store_true", help="most influential first instead of newest"
)
a = p.parse_args()

items = run(
    "tacps126~research-radar",
    {
        "queries": a.queries,
        "postedWithinDays": a.days,
        "sortBy": "impact" if a.influential else "newest",
        "maxItems": 200,
        "onlyNew": not a.influential,
    },
)

with open("research.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "publishedAt",
            "type",
            "title",
            "venue",
            "citations",
            "impact",
            "rank",
            "foundIn",
            "url",
            "pdfUrl",
        ]
    )
    for r in items:
        w.writerow(
            [
                r.get("publishedAt"),
                r.get("type"),
                r.get("title"),
                r.get("venue"),
                r.get("citations"),
                r.get("fieldNormalizedImpact"),
                r.get("citationRank"),
                ",".join(r.get("foundIn", [])),
                r.get("url"),
                r.get("pdfUrl"),
            ]
        )
print(f"{len(items)} results → research.csv")
