# apify-data-recipes

Small, copy-paste recipes for common data jobs: hiring signals, news alerts, review
monitoring, lead enrichment, trade-show leads, Reddit buying-intent leads, Shopify store leads,
job feeds, research alerts and technology-field comparisons. Each recipe calls a ready-made
[Apify](https://apify.com) Actor and prints or saves clean JSON/CSV.

You need a free Apify account. Put your API token in `APIFY_TOKEN` (Console →
Settings → API & Integrations). Pricing is per result; every recipe states the cost.

| Recipe | What it does | Actor |
|--------|--------------|-------|
| [hiring_signals.py](recipes/hiring_signals.py) | Weekly list of target accounts hiring for given roles | [Hiring Signals](https://apify.com/tacps126/hiring-signals) |
| [news_alerts.py](recipes/news_alerts.py) | New Google News articles for a query → CSV, with real publisher URLs | [Google News Scraper](https://apify.com/tacps126/google-news) |
| [contacts_from_websites.py](recipes/contacts_from_websites.py) | Emails, phones and social links from a list of websites | [Website Contact Details](https://apify.com/tacps126/contact-details) |
| [jobs_feed.py](recipes/jobs_feed.py) | One normalized job feed from career pages or company names (13 job-board systems) | [Job Board Harvester](https://apify.com/tacps126/jobs-harvester) |
| [remote_jobs_feed.py](recipes/remote_jobs_feed.py) | Remote jobs open to your countries from company sites and remote-job feeds → CSV | [Remote Jobs Scraper](https://apify.com/tacps126/remote-jobs-scraper) |
| [reddit_leads.py](recipes/reddit_leads.py) | Reddit posts asking for a tool like yours or an alternative to a competitor, tagged by intent → CSV | [Reddit Lead Finder](https://apify.com/tacps126/reddit-lead-finder) |
| [shopify_store_leads.py](recipes/shopify_store_leads.py) | The Shopify stores in a list of websites, with country, catalog and contacts → CSV | [Shopify Store Analyzer](https://apify.com/tacps126/shopify-store-analyzer) |
| [exhibitor_leads.py](recipes/exhibitor_leads.py) | Exhibitors of any trade show (paste its exhibitor-list link) → CSV with booth and contacts; missing emails found on each company's website | [Trade Show Exhibitor List Scraper](https://apify.com/tacps126/exhibition-scraper) + [Website Contact Details](https://apify.com/tacps126/contact-details) |
| [research_alerts.py](recipes/research_alerts.py) | New papers, preprints and patents for your topics, merged across OpenAlex, arXiv, PubMed and Europe PMC → CSV (or the most influential, `--influential`) | [Research Radar](https://apify.com/tacps126/research-radar) |
| [compare_fields.py](recipes/compare_fields.py) | Technology fields ranked by opportunity score, with the reasons, industry share and top companies → CSV | [Innovation Radar](https://apify.com/tacps126/innovation-radar) |
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

## n8n, Make and Zapier

The same endpoint works from any automation tool. In n8n: add an **HTTP Request** node with
`POST https://api.apify.com/v2/acts/<actor>/run-sync-get-dataset-items`, header
`Authorization: Bearer <token>`, your input as the JSON body and a 330-second timeout. Each result
becomes one n8n item, so you can map fields straight into Sheets, a CRM or a database. Our actors
return normalized fields in one schema; the [exhibitor scraper](https://apify.com/tacps126/exhibition-scraper)
can also add each organiser's original record (`includeRawData`).

Issues and requests are welcome. If a source you need is missing, open an issue.
