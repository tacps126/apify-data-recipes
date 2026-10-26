"""Screen a list of customers or suppliers against official sanctions lists (OFAC, UN, EU,
UK, Canada, Switzerland) → screening.csv with a verdict per name. A screening aid, not legal advice.

Cost: about $0.003 per name.
Usage: python sanctions_check.py names.txt        (one person or company per line)
"""

import csv
import sys

from _apify import run

names = (
    [line.strip() for line in open(sys.argv[1]) if line.strip()]
    if len(sys.argv) > 1
    else ["Rosneft", "Acme Trading LLC"]
)

results = run(
    "tacps126~sanctions-screener",
    {"mode": "screen", "names": names, "maxItems": len(names)},
)

with open("screening.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "verdict", "score", "matchedName", "list", "programs", "url"])
    for r in results:
        best = (r.get("matches") or [{}])[0]
        w.writerow(
            [
                r.get("query"),
                r.get("status"),
                r.get("topScore"),
                best.get("matchedName"),
                best.get("list"),
                ", ".join(best.get("programs") or []),
                best.get("url"),
            ]
        )
flagged = sum(r.get("status") != "no-match" for r in results)
print(f"{len(results)} names screened, {flagged} to review → screening.csv")
