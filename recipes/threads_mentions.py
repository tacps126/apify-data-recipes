"""New Threads posts that mention your brand or topic, most engaged first > threads_mentions.csv.
Run it daily; with a monitor name only posts not seen before come back.

Cost: about $0.0015 per post.
Usage: python threads_mentions.py "acme,acme coffee" acme-daily
       (search words, optional monitor name for only-new runs)
"""

import csv
import sys

from _apify import run

terms = (sys.argv[1] if len(sys.argv) > 1 else "electric cars").split(",")
monitor = sys.argv[2] if len(sys.argv) > 2 else None

payload = {"searchTerms": [t.strip() for t in terms], "searchRecent": True, "maxItems": 300}
if monitor:
    payload |= {"onlyNew": True, "monitorName": monitor}
posts = [p for p in run("tacps126~threads-scraper", payload) if p.get("type") == "post"]
posts.sort(
    key=lambda p: (p.get("likesCount") or 0) + 3 * (p.get("repliesCount") or 0), reverse=True
)

with open("threads_mentions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["posted", "author", "likes", "replies", "reposts", "text", "url"])
    for p in posts:
        w.writerow(
            [
                (p.get("timestamp") or "")[:16],
                p.get("authorUsername"),
                p.get("likesCount"),
                p.get("repliesCount"),
                p.get("repostsCount"),
                (p.get("text") or "").replace("\n", " "),
                p.get("url"),
            ]
        )
print(f"{len(posts)} posts > threads_mentions.csv")
