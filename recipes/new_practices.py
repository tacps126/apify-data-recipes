"""New US practices: providers of a specialty whose NPI was issued recently, with address and
phone > new_practices.csv. A fresh lead list for anyone selling to dentists, clinics or therapists.

Cost: about $0.003 per provider.
Usage: python new_practices.py "Dentist" TX,FL 30      (specialty, states, days back)
"""

import csv
import sys

from _apify import run

specialty = sys.argv[1] if len(sys.argv) > 1 else "Dentist"
states = (sys.argv[2] if len(sys.argv) > 2 else "TX").split(",")
days = int(sys.argv[3]) if len(sys.argv) > 3 else 30

providers = run(
    "tacps126~npi-providers",
    {
        "specialties": [specialty],
        "states": [s.strip().upper() for s in states],
        "enumeratedWithinDays": days,
        "withPhoneOnly": True,
        "maxItems": 1000,
    },
)

with open("new_practices.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        ["npi", "name", "type", "specialty", "street", "city", "state", "zip", "phone", "since"]
    )
    for p in providers:
        w.writerow(
            [
                p.get("npi"),
                p.get("name"),
                p.get("type"),
                p.get("specialty"),
                p.get("street"),
                p.get("city"),
                p.get("state"),
                p.get("zip"),
                p.get("phone"),
                p.get("enumerationDate"),
            ]
        )
print(f"{len(providers)} new {specialty} NPIs in the last {days} days > new_practices.csv")
