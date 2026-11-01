"""Companies that just raised money (SEC Form D), with the founders and executives named in
each filing > funding.csv. Good for selling to newly funded startups.

Cost: about $0.005 per filing.
Usage: python funding_leads.py CA,NY 7 1000000      (states, days back, minimum raised in $)
"""

import csv
import sys

from _apify import run

states = (sys.argv[1] if len(sys.argv) > 1 else "CA").split(",")
days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
min_raised = float(sys.argv[3]) if len(sys.argv) > 3 else 0

filings = run(
    "tacps126~startup-funding",
    {
        "states": [s.strip().upper() for s in states],
        "postedWithinDays": days,
        "minAmountRaised": min_raised or None,
        "maxItems": 500,
    },
)

with open("funding.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "filed",
            "company",
            "industry",
            "raised",
            "offering",
            "investors",
            "city",
            "phone",
            "people",
            "url",
        ]
    )
    for r in filings:
        people = "; ".join(
            f"{p.get('name')} ({', '.join(p.get('roles') or [])})" for p in r.get("people") or []
        )
        w.writerow(
            [
                r.get("filed"),
                r.get("company"),
                r.get("industry"),
                r.get("totalAmountSold"),
                r.get("totalOfferingAmount"),
                r.get("investors"),
                r.get("city"),
                r.get("phone"),
                people,
                r.get("filingUrl"),
            ]
        )
print(f"{len(filings)} new raises in the last {days} days > funding.csv")
