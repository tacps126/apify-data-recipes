"""Which target accounts are hiring for the roles you sell to?

Cost: about $0.01 per company with a matching role; companies with none are free.
Usage: python hiring_signals.py
"""
from _apify import run

ACCOUNTS = [
    "https://boards.greenhouse.io/stripe",
    "https://jobs.lever.co/spotify",
    "https://jobs.ashbyhq.com/ramp",
]

rows = run("tacps126~hiring-signals", {
    "companies": ACCOUNTS,
    "roleKeywords": ["data", "analytics", "machine learning"],
    "postedWithinDays": 30,
})
for c in sorted(rows, key=lambda c: -c["matchingRoles"]):
    print(f'{c["company"]:<20} {c["matchingRoles"]:>3} matching roles ({c["newMatchingRoles"]} new)')
    for r in c["roles"][:3]:
        print(f'    - {r["title"]} ({r.get("location", "")})')
