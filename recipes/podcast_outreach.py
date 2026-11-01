"""Active podcasts in your niche with the owner's contact email, for guest pitches and
sponsorships > podcasts.csv.

Cost: about $0.004 per podcast.
Usage: python podcast_outreach.py "b2b saas,startup marketing" 30 us
       (searches, active within days, store country)
"""

import csv
import sys

from _apify import run

searches = (sys.argv[1] if len(sys.argv) > 1 else "b2b saas").split(",")
active_days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
country = sys.argv[3] if len(sys.argv) > 3 else "us"

shows = run(
    "tacps126~podcasts",
    {
        "searchTerms": [s.strip() for s in searches],
        "country": country,
        "activeWithinDays": active_days,
        "withEmailOnly": True,
        "maxPerSource": 100,
        "maxItems": 300,
    },
)

with open("podcasts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "title",
            "owner",
            "email",
            "website",
            "genre",
            "episodes",
            "days_between",
            "last_episode",
            "apple_url",
        ]
    )
    for p in shows:
        w.writerow(
            [
                p.get("title"),
                p.get("ownerName"),
                p.get("ownerEmail"),
                p.get("website"),
                p.get("genre"),
                p.get("episodeCount"),
                p.get("averageDaysBetweenEpisodes"),
                (p.get("lastEpisodeDate") or "")[:10],
                p.get("appleUrl"),
            ]
        )
print(f"{len(shows)} active podcasts with an owner email > podcasts.csv")
