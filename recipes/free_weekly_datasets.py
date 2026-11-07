"""Free weekly datasets, no account or token needed: new company registrations,
product recalls and property auctions from the last 7 days > <name>.csv, with an
optional keyword filter.

Cost: free (public Hugging Face datasets, refreshed weekly). For fresh, filtered
or scheduled data, run the Apify tool named in each dataset's card.
Usage: python free_weekly_datasets.py                     (all three)
       python free_weekly_datasets.py product-recalls peanut
"""

import csv
import io
import sys
import urllib.request

DATASETS = ["new-company-registrations", "product-recalls", "bank-property-auctions"]
URL = "https://huggingface.co/datasets/tacps126/{}/resolve/main/data/latest.csv"

names = [sys.argv[1]] if len(sys.argv) > 1 else DATASETS
keyword = sys.argv[2].lower() if len(sys.argv) > 2 else ""

for name in names:
    with urllib.request.urlopen(URL.format(name), timeout=60) as r:
        rows = list(csv.DictReader(io.StringIO(r.read().decode("utf-8"))))
    if keyword:
        rows = [row for row in rows if keyword in " ".join(row.values()).lower()]
    if not rows:
        print(f"{name}: no rows")
        continue
    with open(f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows > {name}.csv")
