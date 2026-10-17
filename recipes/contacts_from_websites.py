"""Emails, phones and social links from a list of websites → contacts.csv.

Cost: about $0.002 per website where contacts are found; nothing found = free.
Usage: python contacts_from_websites.py sites.txt   (one domain or URL per line)
Use the data within GDPR / CAN-SPAM rules.
"""
import csv
import sys

from _apify import run

sites = [l.strip() for l in open(sys.argv[1]) if l.strip()] if len(sys.argv) > 1 else ["apify.com", "mailchimp.com"]
rows = run("tacps126~contact-details", {"startUrls": sites, "maxPagesPerSite": 5})

with open("contacts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["domain", "emails", "phones", "linkedin", "twitter", "instagram", "facebook"])
    for r in rows:
        w.writerow([r.get("domain"), "; ".join(r.get("emails") or []), "; ".join(r.get("phones") or []),
                    r.get("linkedin"), r.get("twitter"), r.get("instagram"), r.get("facebook")])
print(f"{len(rows)} websites → contacts.csv")
