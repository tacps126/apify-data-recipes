"""New vulnerabilities in the software you run: CVSS, severity, CISA known-exploited status and
the EPSS exploit likelihood > cves.csv. Schedule it daily for a patch-triage list.

Cost: about $0.003 per CVE.
Usage: python cve_alerts.py "microsoft,fortinet,citrix" 2 7      (vendors, days back, min CVSS)
"""

import csv
import sys

from _apify import run

vendors = (sys.argv[1] if len(sys.argv) > 1 else "microsoft").split(",")
days = int(sys.argv[2]) if len(sys.argv) > 2 else 2
min_cvss = float(sys.argv[3]) if len(sys.argv) > 3 else 7

cves = run(
    "tacps126~cve-feed",
    {
        "vendors": [v.strip() for v in vendors],
        "withinDays": days,
        "minCvss": min_cvss,
        "maxItems": 500,
    },
)
# Exploited in the wild first, then the likeliest to be exploited.
cves.sort(key=lambda c: (not c.get("knownExploited"), -(c.get("epss") or 0)))

with open("cves.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "cve",
            "published",
            "cvss",
            "severity",
            "known_exploited",
            "epss",
            "vendors",
            "products",
            "url",
        ]
    )
    for c in cves:
        w.writerow(
            [
                c.get("cveId"),
                (c.get("published") or "")[:10],
                c.get("cvssScore"),
                c.get("severity"),
                c.get("knownExploited"),
                c.get("epss"),
                ", ".join(c.get("vendors") or []),
                ", ".join(c.get("products") or []),
                c.get("url"),
            ]
        )
print(f"{len(cves)} CVEs (CVSS >= {min_cvss}) in the last {days} days > cves.csv")
