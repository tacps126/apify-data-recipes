"""Rank technology fields by opportunity: momentum, lab-to-market gap, industry and top companies.

Cost: about $0.03 per field.
Usage: python compare_fields.py "sodium-ion battery" "solid state battery" "lithium-sulfur battery"
"""
import csv
import sys

from _apify import run

fields = sys.argv[1:] or ["sodium-ion battery", "solid state battery"]
records = run("tacps126~innovation-radar", {"mode": "landscape", "fields": fields, "topWorks": 5})
records.sort(key=lambda r: r.get("rank") or 0)

with open("fields.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", "field", "opportunity", "momentum", "labToMarketGap", "stage", "industryShare", "topCompanies", "why"])
    for r in records:
        s, ind = r.get("scores", {}), r.get("industry", {})
        companies = [c if isinstance(c, str) else c.get("name", "") for c in r.get("topCompanies", [])[:5]]
        w.writerow([
            r.get("rank"), r.get("field"), s.get("opportunity"), s.get("momentum"), s.get("labToMarketGap"),
            r.get("growth", {}).get("stage"), ind.get("recentShare"), "; ".join(companies), " | ".join(s.get("why", [])),
        ])
        print(f"{r.get('rank') or '-'}. {r.get('field')}: {s.get('opportunity')}/100 — {'; '.join(s.get('why', [])[:2])}")
print("→ fields.csv")
