"""Remote jobs open to your countries, from company career sites and the Remote OK,
Jobicy, Working Nomads and Himalayas feeds → remote_jobs.csv. Schedule it daily with
"onlyNew": true to get only new postings.

Cost: about $0.002 per job.
Usage: python remote_jobs_feed.py "engineer,developer" "US,CA"
"""

import csv
import sys

from _apify import run

titles = (sys.argv[1] if len(sys.argv) > 1 else "engineer").split(",")
countries = (sys.argv[2] if len(sys.argv) > 2 else "US").split(",")

jobs = run(
    "tacps126~remote-jobs-scraper",
    {
        "titleIncludes": [t.strip() for t in titles if t.strip()],
        "countries": [c.strip() for c in countries if c.strip()],
        "postedWithinDays": 14,
        "maxItems": 200,
    },
)

with open("remote_jobs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        ["company", "title", "country", "seniority", "salaryMin", "salaryMax", "currency", "url"]
    )
    for j in jobs:
        s = j.get("salary") or {}
        w.writerow(
            [
                j.get("company"),
                j.get("title"),
                j.get("countryCode"),
                j.get("seniority"),
                s.get("annualMin"),
                s.get("annualMax"),
                s.get("currency"),
                j.get("url"),
            ]
        )
print(f"{len(jobs)} remote jobs → remote_jobs.csv")
