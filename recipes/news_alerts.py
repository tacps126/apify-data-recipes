"""Google News articles for a query → news.csv, with the publisher's real URL.

Cost: about $0.002 per article.
Usage: python news_alerts.py "generative AI" [timeframe: 1h|1d|7d]
"""
import csv
import sys

from _apify import run

query = sys.argv[1] if len(sys.argv) > 1 else "artificial intelligence"
timeframe = sys.argv[2] if len(sys.argv) > 2 else "1d"
articles = run("tacps126~google-news", {"queries": [query], "timeframe": timeframe, "maxItems": 100})

with open("news.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["publishedAt", "publisher", "title", "url"])
    for a in articles:
        w.writerow([a.get("publishedAt"), a.get("publisher"), a.get("title"), a.get("url")])
print(f"{len(articles)} articles → news.csv")
