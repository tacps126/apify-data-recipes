"""Reddit posts from people ready to buy (asking for a tool, leaving a competitor,
comparing options, complaining) → leads.csv, newest first.

Cost: about $0.002 per lead plus $0.0001 per post read (a run like this: a few cents).
Usage: python reddit_leads.py "CRM" "HubSpot,Pipedrive"
"""
import csv
import sys

from _apify import run

categories = [c.strip() for c in (sys.argv[1] if len(sys.argv) > 1 else "CRM").split(",") if c.strip()]
competitors = [c.strip() for c in (sys.argv[2] if len(sys.argv) > 2 else "HubSpot").split(",") if c.strip()]

leads = run("tacps126~reddit-lead-finder", {
    "keywords": categories,        # what you sell, as buyers say it
    "competitors": competitors,    # products whose users you want
    "time": "month",
    "maxItems": 100,
    "maxPostsPerSource": 50,
})
leads.sort(key=lambda x: x.get("publishedAt") or "", reverse=True)

with open("leads.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["publishedAt", "intent", "phrase", "subreddit", "title", "url"])
    for x in leads:
        w.writerow([x.get("publishedAt"), x.get("intent"), x.get("intentPhrase"),
                    x.get("subreddit"), x.get("title") or x.get("postTitle"), x.get("url")])
print(f"{len(leads)} leads → leads.csv")
