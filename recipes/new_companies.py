"""Companies registered in the last N days in official registers → companies.csv.
A daily lead list for anyone selling to new businesses (banking, accounting, insurance, web).

Cost: about $0.0025 per company.
Usage: python new_companies.py US-NY 1          (country or US state, days back)
       python new_companies.py FR 7 56.10       (optional industry code prefix: restaurants)
"""

import csv
import sys

from _apify import run

country = sys.argv[1] if len(sys.argv) > 1 else "US-NY"
days = int(sys.argv[2]) if len(sys.argv) > 2 else 1
codes = sys.argv[3:]

companies = run(
    "tacps126~company-registry",
    {
        "mode": "new",
        "countries": [country],
        "registeredWithinDays": days,
        "industryCodes": codes,
        "maxItems": 500,
    },
)

with open("companies.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["registeredOn", "name", "legalForm", "industry", "city", "region", "email", "url"])
    for c in companies:
        a = c.get("address") or {}
        w.writerow(
            [
                c.get("registeredOn"),
                c.get("name"),
                c.get("legalForm"),
                c.get("industry"),
                a.get("city"),
                a.get("region"),
                c.get("email"),
                c.get("url"),
            ]
        )
print(f"{len(companies)} new companies in {country} (last {days} days) → companies.csv")
