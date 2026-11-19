"""Independent artists on SoundCloud and Spotify for your genres, best leads first: followers,
monthly listeners, latest release, city, e-mail and social links > music_artists.csv.

Cost: about $0.0025 per artist.
Usage: python music_artist_leads.py "lofi hip hop" "indie folk berlin"
"""

import csv
import sys

from _apify import run

queries = sys.argv[1:] or ["lofi hip hop"]

rows = run(
    "tacps126~media-profiles",
    {
        "searchTerms": queries,
        "platforms": ["soundcloud", "spotify"],
        "artistType": "independent",
        "itemsPerProfile": 0,
        "profilesPerSearch": 50,
        "maxItems": 200,
    },
)
artists = sorted(
    (r for r in rows if r.get("type") == "profile"),
    key=lambda r: r.get("leadScore") or 0,
    reverse=True,
)

with open("music_artists.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "name",
            "platform",
            "lead_score",
            "followers",
            "monthly_listeners",
            "latest_release",
            "city",
            "country",
            "email",
            "instagram",
            "url",
        ]
    )
    for a in artists:
        socials = a.get("socials") or {}
        w.writerow(
            [
                a.get("name"),
                a.get("platform"),
                a.get("leadScore"),
                a.get("followers"),
                a.get("monthlyListeners"),
                (a.get("latestRelease") or {}).get("date"),
                a.get("city"),
                a.get("country"),
                (a.get("emails") or [""])[0],
                socials.get("instagram"),
                a.get("url"),
            ]
        )
with_email = sum(1 for a in artists if a.get("emails"))
print(f"{len(artists)} artists, {with_email} with an e-mail > music_artists.csv")
