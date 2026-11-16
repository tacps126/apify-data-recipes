"""Contact details from a list of Facebook Pages (local businesses, brands, venues): category,
e-mail, phone, address, website, followers and rating > facebook_pages.csv.

Cost: about $0.003 per page.
Usage: python facebook_page_contacts.py pages.txt
       (one page name or link per line, e.g. katzsdeli or https://www.facebook.com/nasa)
"""

import csv
import sys
from pathlib import Path

from _apify import run

src = sys.argv[1] if len(sys.argv) > 1 else None
pages = (
    [line.strip() for line in Path(src).read_text().splitlines() if line.strip()]
    if src
    else ["katzsdeli"]
)

rows = run("tacps126~facebook-pages", {"pages": pages, "maxItems": len(pages)})

with open("facebook_pages.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "name",
            "categories",
            "email",
            "phone",
            "address",
            "website",
            "followers",
            "recommend_%",
            "reviews",
            "url",
        ]
    )
    for p in rows:
        w.writerow(
            [
                p.get("name"),
                ", ".join(p.get("categories") or []),
                p.get("email"),
                p.get("phone"),
                p.get("address"),
                (p.get("websites") or [""])[0],
                p.get("followers"),
                p.get("recommendPercent"),
                p.get("reviewsCount"),
                p.get("url"),
            ]
        )
with_email = sum(1 for p in rows if p.get("email"))
print(f"{len(rows)} pages, {with_email} with an e-mail > facebook_pages.csv")
