# apify-data-recipes

Small, copy-paste recipes for common data jobs: hiring signals, news alerts, review
monitoring, lead enrichment and job feeds. Each recipe calls a ready-made
[Apify](https://apify.com) Actor and prints or saves clean JSON/CSV.

You need a free Apify account. Put your API token in `APIFY_TOKEN` (Console →
Settings → API & Integrations). Pricing is per result; every recipe states the cost.

| Recipe | What it does | Actor |
|--------|--------------|-------|
| [hiring_signals.py](recipes/hiring_signals.py) | Weekly list of target accounts hiring for given roles | [Hiring Signals](https://apify.com/tacps126/hiring-signals) |
| [news_alerts.py](recipes/news_alerts.py) | New Google News articles for a query → CSV, with real publisher URLs | [Google News Scraper](https://apify.com/tacps126/google-news) |
| [contacts_from_websites.py](recipes/contacts_from_websites.py) | Emails, phones and social links from a list of websites | [Website Contact Details](https://apify.com/tacps126/contact-details) |
| [jobs_feed.py](recipes/jobs_feed.py) | One normalized job feed from Greenhouse, Lever, Ashby and Workday pages | [Job Board Harvester](https://apify.com/tacps126/jobs-harvester) |
| [negative_reviews.sh](recipes/negative_reviews.sh) | 1–2★ Trustpilot reviews of competitors (curl only) | [Trustpilot Reviews](https://apify.com/tacps126/trustpilot-reviews) |

```bash
pip install requests
export APIFY_TOKEN=...
python recipes/news_alerts.py "generative AI"
```

All recipes use the synchronous endpoint
`POST /v2/acts/<actor>/run-sync-get-dataset-items`. It runs the Actor and returns the
results in the same request, up to 5 minutes. For longer runs, start a run and poll it;
see the [Apify API docs](https://docs.apify.com/api/v2).

Issues and requests are welcome. If a source you need is missing, open an issue.
