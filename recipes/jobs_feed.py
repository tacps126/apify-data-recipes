"""One normalized job feed from several companies → jobs.csv. Give career-page links
(the company's own careers page or its job board) or just company names.

Cost: about $0.001 per job.
Usage: python jobs_feed.py
"""

import csv

from _apify import run

jobs = run(
    "tacps126~jobs-harvester",
    {
        "careerPageUrls": [
            "https://boards.greenhouse.io/stripe",
            "https://jobs.lever.co/spotify",
            "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite",
            "https://www.figma.com/careers",  # company site: its job board is found for you
        ],
        "companyNames": ["Datadog", "Ramp"],  # or just names
        "countries": ["US"],
        "titleIncludes": ["engineer"],
        "postedWithinDays": 14,
        "maxItems": 300,
    },
)

with open("jobs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["company", "title", "location", "postedAtIso", "url"])
    for j in jobs:
        loc = j.get("location")
        w.writerow(
            [
                j.get("company"),
                j.get("title"),
                loc if isinstance(loc, str) else (loc or {}).get("text"),
                j.get("postedAtIso"),
                j.get("url"),
            ]
        )
print(f"{len(jobs)} jobs → jobs.csv")
