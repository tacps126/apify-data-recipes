"""Trade-show lead list: exhibitors of any show → exhibitor_leads.csv.

1. Scrapes the exhibitor list of the show behind a link (any Messe Frankfurt,
   Messe Düsseldorf, Swapcard or Corussoft show, or a built-in one).
2. For exhibitors that list a website but no email, finds emails on their
   own website with Website Contact Details.
3. Writes one CSV with booth, contacts and where each email came from.

Cost: about $0.002 per exhibitor, plus about $0.002 per website where
contacts are found (sites with nothing found are free).
Usage: python exhibitor_leads.py <exhibitor-list link or built-in show id> [max per show]
  e.g. python exhibitor_leads.py "https://ish.messefrankfurt.com/frankfurt/en/exhibitor-search.html"
       python exhibitor_leads.py sema-show 200        (ids: see the Actor README)
Use the data within GDPR / CAN-SPAM rules.
"""
import csv
import sys

from _apify import run

url = sys.argv[1] if len(sys.argv) > 1 else "https://ish.messefrankfurt.com/frankfurt/en/exhibitor-search.html"
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50

show = {"startUrls": [{"url": url}]} if url.startswith("http") else {"exhibitionList": [url]}
exhibitors = run("tacps126~exhibition-scraper", {**show, "maxResults": limit})
print(f"{len(exhibitors)} exhibitors from {url}")

# Exhibitors with a website but no email: look the email up on their site.
missing = {
    (e.get("contact") or {}).get("website"): e
    for e in exhibitors
    if not (e.get("contact") or {}).get("email") and (e.get("contact") or {}).get("website")
}
found = {}
if missing:
    for r in run("tacps126~contact-details", {"startUrls": list(missing), "maxPagesPerSite": 5}):
        found[r.get("domain")] = r
    print(f"{len(found)} of {len(missing)} websites without an email gave contacts")


def domain(site):
    host = (site or "").split("//")[-1].split("/")[0].lower()
    return host[4:] if host.startswith("www.") else host


with open("exhibitor_leads.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "booth", "email", "email_source", "phone", "website", "city", "country", "exhibition_url"])
    for e in exhibitors:
        c, a = e.get("contact") or {}, e.get("address") or {}
        email, source = c.get("email"), "exhibitor list" if c.get("email") else ""
        site = found.get(domain(c.get("website")))
        if not email and site and site.get("primaryEmail"):
            email, source = site["primaryEmail"], "company website"
        w.writerow([e.get("name"), e.get("booth"), email, source, c.get("phone") or (site or {}).get("primaryPhone"),
                    c.get("website"), a.get("city"), a.get("country"), e.get("exhibitionUrl")])
print("→ exhibitor_leads.csv")
