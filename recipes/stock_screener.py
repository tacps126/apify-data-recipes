"""Daily stock screener: a verdict per ticker (bullish to bearish, with confidence), support and
resistance, and which ready-made rules are true today, with how often each worked on that stock
before > screener.csv. Add --only to keep just the tickers where a rule is true now.

Rules to pick from: golden-cross, death-cross, oversold-bounce, overbought-fade,
pullback-in-uptrend, short-term-dip, breakout-on-volume, breakdown-on-volume,
macd-bullish-cross, macd-bearish-cross, bollinger-reentry, supertrend-turns-up,
supertrend-turns-down, strong-uptrend, stretched-below-mean, stretched-above-mean.

Cost: about $0.002 per ticker returned.
Usage:
  python stock_screener.py "AAPL,MSFT,NVDA,SAP.DE" "pullback-in-uptrend,breakout-on-volume" [--only]
"""

import csv
import sys

from _apify import run

args = [a for a in sys.argv[1:] if a != "--only"]
tickers = (args[0] if args else "AAPL,MSFT,NVDA,AMZN,GOOGL").split(",")
presets = (args[1] if len(args) > 1 else "pullback-in-uptrend,breakout-on-volume").split(",")

rows = run(
    "tacps126~stock-analyzer",
    {
        "tickers": [t.strip() for t in tickers],
        "rulePresets": [p.strip() for p in presets],
        "onlyMatching": "--only" in sys.argv,
    },
)

with open("screener.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "ticker",
            "price",
            "verdict",
            "confidence",
            "support",
            "resistance",
            "rules_true_now",
            "rule_hit_rate_5d",
            "base_rate_5d",
            "answer",
        ]
    )
    for r in rows:
        true_now = r.get("rulesTrueNow") or []
        hit, base = [], []
        for name in true_now:
            o = ((r.get("rules") or {}).get(name) or {}).get("outcomes", {}).get("bars5", {})
            hit.append(f"{name}: {o.get('hitRate')}%")
            base.append(str(o.get("baseRate")))
        w.writerow(
            [
                r.get("symbol"),
                r.get("price"),
                r.get("verdict"),
                r.get("confidence"),
                r.get("support"),
                r.get("resistance"),
                "; ".join(true_now),
                "; ".join(hit),
                "; ".join(base),
                r.get("answer"),
            ]
        )
print(f"{len(rows)} ticker(s) > screener.csv")
