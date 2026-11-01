"""Closing betting lines and how they settled (who covered, over or under, did the favourite
win) for last week's games > closing_lines.csv. A ready table for backtesting models.

Cost: about $0.003 per game line.
Usage: python closing_lines.py nfl,ncaaf 7      (leagues, days back)
"""

import csv
import sys

from _apify import run

leagues = (sys.argv[1] if len(sys.argv) > 1 else "nfl").split(",")
days = int(sys.argv[2]) if len(sys.argv) > 2 else 7

lines = run(
    "tacps126~sports-data",
    {
        "leagues": [x.strip() for x in leagues],
        "dataType": "odds",
        "daysBack": days,
        "gameStatus": "final",
        "maxItems": 2000,
    },
)

cols = [
    "league", "date", "awayTeam", "homeTeam", "awayScore", "homeScore", "sportsbook",
    "homeSpreadOpen", "homeSpread", "spreadResult", "totalOpen", "total", "totalResult",
    "homeMoneylineOpen", "homeMoneyline", "favorite", "favoriteWon",
]  # fmt: skip
with open("closing_lines.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for line in lines:
        w.writerow({**line, "date": (line.get("date") or "")[:10]})
print(f"{len(lines)} closing lines from the last {days} days > closing_lines.csv")
