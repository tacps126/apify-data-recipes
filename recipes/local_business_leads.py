"""Local businesses by category and city, with their contacts > local_leads.csv.

Cost: about $0.00125 per business, plus $0.00175 when contacts are found on its website.
Usage: python local_business_leads.py "Pune" IN dentist orthodontist
Use the data within GDPR / CAN-SPAM rules.
"""

import csv
import sys

from _apify import run

city = sys.argv[1] if len(sys.argv) > 1 else "Austin"
country = sys.argv[2] if len(sys.argv) > 2 else "US"
categories = sys.argv[3:] or ["plumber"]
rows = run(
    "tacps126~contact-details",
    {
        "city": city,
        "countryCode": country,
        "categories": categories,
        "radiusKm": 10,
        "requireEmail": True,
        "maxItems": 200,
    },
)

with open("local_leads.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "category", "email", "email_on_own_site", "phone", "website", "address", "postcode"])
    for r in rows:
        w.writerow(
            [
                r.get("name"),
                r.get("category"),
                r.get("primaryEmail"),
                r.get("emailFoundOnWebsite"),
                r.get("primaryPhone"),
                r.get("website"),
                r.get("address"),
                r.get("postcode"),
            ]
        )
print(f"{len(rows)} businesses in {city} > local_leads.csv")
