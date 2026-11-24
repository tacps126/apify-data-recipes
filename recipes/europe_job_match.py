"""Jobs from Europe's main job boards, scored against your CV by AI > europe_jobs.csv,
best fit first. Each job gets a 0-100 fit score, the reason and what your profile lacks.

Cost: about $0.001 per job, plus $0.01 per AI-matched job (first 25) and the AI model's
tokens on your Apify account.
Usage: python europe_job_match.py "data engineer" "de,nl" "4 years Python, SQL, Airflow, AWS"
"""

import csv
import sys

from _apify import run

query = sys.argv[1] if len(sys.argv) > 1 else "data engineer"
countries = (sys.argv[2] if len(sys.argv) > 2 else "de,nl").split(",")
profile = sys.argv[3] if len(sys.argv) > 3 else "4 years Python, SQL, Airflow and AWS; wants hybrid"

jobs = run(
    "tacps126~europe-jobs-scraper",
    {
        "query": query,
        "countries": [c.strip().lower() for c in countries if c.strip()],
        "maxItems": 60,
        "aiInsights": True,
        "aiProfile": profile,
        "maxInsights": 25,
    },
    timeout=600,
)

matched = [j for j in jobs if (j.get("insight") or {}).get("fitScore") is not None]
matched.sort(key=lambda j: j["insight"]["fitScore"], reverse=True)

with open("europe_jobs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        ["fitScore", "title", "company", "country", "location", "fitReason", "missing", "url"]
    )
    for j in matched:
        i = j["insight"]
        w.writerow(
            [
                i.get("fitScore"),
                j.get("title"),
                j.get("company"),
                j.get("countryCode"),
                j.get("location"),
                i.get("fitReason"),
                "; ".join(i.get("missingFromProfile") or []),
                j.get("url"),
            ]
        )
print(f"{len(matched)} scored jobs (of {len(jobs)}) > europe_jobs.csv")
