"""Importer lookalikes: the US brands that buy from the same factories as the companies you name,
from US customs bills of lading > importer_lookalikes.csv. A prospect list for freight forwarders,
customs brokers, sourcing agents and anyone selling to importers.

Cost: about $0.004 per company profile and $0.002 per lookalike importer.
Usage: python importer_lookalikes.py "Allbirds,Gymshark" 25      (companies, lookalikes per company)
"""

import csv
import sys

from _apify import run

companies = (sys.argv[1] if len(sys.argv) > 1 else "Allbirds").split(",")
per_company = int(sys.argv[2]) if len(sys.argv) > 2 else 25

rows = run(
    "tacps126~us-import-records",
    {
        "companies": [c.strip() for c in companies if c.strip()],
        "includePartners": False,
        "findLookalikes": True,
        "maxLookalikesPerCompany": per_company,
        "maxItems": 1000,
    },
)

profiles = {r.get("name"): r for r in rows if r.get("type") == "profile"}
lookalikes = [r for r in rows if r.get("type") == "lookalike"]
lookalikes.sort(key=lambda r: (r.get("of") or "", -(r.get("sharedSuppliers") or 0)))

with open("importer_lookalikes.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        ["similar_to", "importer", "shared_suppliers", "shipments_12m_from_shared", "suppliers"]
    )
    for r in lookalikes:
        w.writerow(
            [
                r.get("of"),
                r.get("name"),
                r.get("sharedSuppliers"),
                r.get("shipments12mFromShared"),
                "; ".join(r.get("suppliers") or []),
            ]
        )

for name, p in profiles.items():
    print(f"{name}: {p.get('shipments12m')} shipments in 12 months ({p.get('shipmentGrowthPct')}% vs the 12 before)")
print(f"{len(lookalikes)} lookalike importers > importer_lookalikes.csv")
