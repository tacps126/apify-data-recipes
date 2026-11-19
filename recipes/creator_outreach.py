"""YouTube and Vimeo creators for your niche with real engagement, best leads first: subscribers,
average views, engagement rate, last post, e-mail and other social accounts > creators.csv.

Cost: about $0.005 per creator (profile plus its 3 latest videos).
Usage: python creator_outreach.py "home barista" "budget travel"
"""

import csv
import sys

from _apify import run

queries = sys.argv[1:] or ["home barista"]

rows = run(
    "tacps126~creator-finder",
    {
        "searchTerms": queries,
        "platforms": ["youtube", "vimeo"],
        "minFollowers": 1000,
        "minEngagementRate": 1,
        "itemsPerProfile": 3,
        "profilesPerSearch": 40,
        "maxItems": 400,
    },
)
creators = sorted(
    (r for r in rows if r.get("type") == "profile"),
    key=lambda r: r.get("leadScore") or 0,
    reverse=True,
)

with open("creators.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "name",
            "platform",
            "lead_score",
            "followers",
            "avg_views",
            "engagement_%",
            "last_post",
            "country",
            "email",
            "instagram",
            "tiktok",
            "url",
        ]
    )
    for c in creators:
        socials = c.get("socials") or {}
        w.writerow(
            [
                c.get("name"),
                c.get("platform"),
                c.get("leadScore"),
                c.get("followers"),
                c.get("avgViews"),
                c.get("engagementRate"),
                (c.get("latestRelease") or {}).get("date"),
                c.get("country"),
                (c.get("emails") or [""])[0],
                socials.get("instagram"),
                socials.get("tiktok"),
                c.get("url"),
            ]
        )
with_email = sum(1 for c in creators if c.get("emails"))
print(f"{len(creators)} creators, {with_email} with an e-mail > creators.csv")
