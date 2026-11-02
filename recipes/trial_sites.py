"""Recruiting clinical trials for a condition, one row per study site in your country, with the
sponsor and the study's central contact > trial_sites.csv. For site networks, CROs and patients.

Cost: about $0.003 per study.
Usage: python trial_sites.py "obesity" "United States" PHASE2,PHASE3
"""

import csv
import sys

from _apify import run

condition = sys.argv[1] if len(sys.argv) > 1 else "obesity"
country = sys.argv[2] if len(sys.argv) > 2 else "United States"
phases = sys.argv[3].split(",") if len(sys.argv) > 3 else []

studies = run(
    "tacps126~clinical-trials",
    {
        "condition": condition,
        "location": country,
        "statuses": ["RECRUITING", "NOT_YET_RECRUITING"],
        "phases": phases or None,
        "maxLocationsPerStudy": 200,
        "maxItems": 200,
    },
)

rows = 0
with open("trial_sites.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "nct_id",
            "title",
            "phases",
            "sponsor",
            "site",
            "city",
            "state",
            "contact",
            "email",
            "phone",
            "url",
        ]
    )
    for s in studies:
        contact = (s.get("centralContacts") or [{}])[0]
        for loc in s.get("locations") or []:
            if loc.get("country") != country:
                continue
            rows += 1
            w.writerow(
                [
                    s.get("nctId"),
                    s.get("title"),
                    ", ".join(s.get("phases") or []),
                    s.get("sponsor"),
                    loc.get("facility"),
                    loc.get("city"),
                    loc.get("state"),
                    contact.get("name"),
                    contact.get("email"),
                    contact.get("phone"),
                    s.get("url"),
                ]
            )
print(f"{len(studies)} recruiting studies, {rows} sites in {country} > trial_sites.csv")
