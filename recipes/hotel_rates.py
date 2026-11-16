"""Hotel prices for a place and your dates from Google Hotels, cheapest good hotels first, with
the deal versus the usual price > hotel_rates.csv. Rate checks and trip planning.

Cost: about $0.002 per hotel.
Usage: python hotel_rates.py "Lisbon" 2027-03-10 2027-03-12 4
       (place, check-in, check-out, lowest hotel class)
"""

import csv
import sys

from _apify import run

place = sys.argv[1] if len(sys.argv) > 1 else "Lisbon"
check_in = sys.argv[2] if len(sys.argv) > 2 else None
check_out = sys.argv[3] if len(sys.argv) > 3 else None
min_stars = int(sys.argv[4]) if len(sys.argv) > 4 else 4

payload = {"locations": [place], "minStars": min_stars, "moreResults": True, "maxItems": 200}
if check_in and check_out:
    payload |= {"checkIn": check_in, "checkOut": check_out}
hotels = [
    h for h in run("tacps126~google-hotels", payload) if (h.get("price") or {}).get("nightly")
]
hotels.sort(key=lambda h: (h["price"]["nightly"], -(h.get("rating") or 0)))

with open("hotel_rates.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "name",
            "stars",
            "rating",
            "reviews",
            "nightly",
            "nightly_with_taxes",
            "total_with_taxes",
            "currency",
            "deal",
            "website",
            "google_url",
        ]
    )
    for h in hotels:
        p = h["price"]
        w.writerow(
            [
                h.get("name"),
                h.get("stars"),
                h.get("rating"),
                h.get("reviewsCount"),
                p.get("nightly"),
                p.get("nightlyWithTaxes"),
                p.get("totalWithTaxes"),
                p.get("currency"),
                h.get("deal"),
                h.get("website"),
                h.get("googleUrl"),
            ]
        )
print(f"{len(hotels)} hotels in {place}, cheapest first > hotel_rates.csv")
