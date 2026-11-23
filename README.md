# apify-data-recipes

Small, copy-paste recipes for common data jobs: hiring signals, news alerts, review
monitoring, lead enrichment, trade-show leads, new-company leads, Shopify store leads, sanctions
screening, recall alerts, YouTube transcripts, job feeds, research alerts, technology-field comparisons, prediction-market movers,
closing betting lines, daily stock screens, startup funding leads, podcast outreach, property auction deals, local business leads, CVE alerts,
clinical trial sites, new medical practices and importer lookalikes. Each recipe calls a ready-made
[Apify](https://apify.com) Actor and prints or saves clean JSON/CSV.

You need a free Apify account. Put your API token in `APIFY_TOKEN` (Console > 
Settings > API & Integrations). Pricing is per result; every recipe states the cost.

| Recipe | What it does | Actor |
|--------|--------------|-------|
| [free_weekly_datasets.py](recipes/free_weekly_datasets.py) | Free, no token: this week's new companies, product recalls and property auctions > CSV, with a keyword filter | [Company Registry](https://apify.com/tacps126/company-registry), [Recalls Radar](https://apify.com/tacps126/recalls-radar), [Auctions Radar](https://apify.com/tacps126/auctions-radar) |
| [hiring_signals.py](recipes/hiring_signals.py) | Weekly list of target accounts hiring for given roles | [Hiring Signals](https://apify.com/tacps126/hiring-signals) |
| [news_alerts.py](recipes/news_alerts.py) | New Google News articles for a query > CSV, with real publisher URLs | [Google News Scraper](https://apify.com/tacps126/google-news) |
| [contacts_from_websites.py](recipes/contacts_from_websites.py) | Emails, phones and social links from a list of websites | [Website Contact Details](https://apify.com/tacps126/contact-details) |
| [local_business_leads.py](recipes/local_business_leads.py) | Local businesses by category and city (e.g. dentists in Pune) with e-mails from their own websites > CSV | [Website Contact Details](https://apify.com/tacps126/contact-details) |
| [jobs_feed.py](recipes/jobs_feed.py) | One normalized job feed from career pages or company names (13 job-board systems) | [Job Board Harvester](https://apify.com/tacps126/jobs-harvester) |
| [remote_jobs_feed.py](recipes/remote_jobs_feed.py) | Remote jobs open to your countries from company sites and remote-job feeds > CSV | [Remote Jobs Scraper](https://apify.com/tacps126/remote-jobs-scraper) |
| [new_companies.py](recipes/new_companies.py) | Companies registered in the last days (France, Norway, Finland, Estonia, New York, Colorado, Connecticut, Oregon) by industry code > CSV | [Company Registry](https://apify.com/tacps126/company-registry) |
| [shopify_store_leads.py](recipes/shopify_store_leads.py) | The Shopify stores in a list of websites, with country, catalog and contacts > CSV | [Shopify Store Analyzer](https://apify.com/tacps126/shopify-store-analyzer) |
| [shopify_best_deals.py](recipes/shopify_best_deals.py) | The biggest discounts across several Shopify stores, best first > CSV | [Shopify Products Scraper](https://apify.com/tacps126/shopify-products) |
| [exhibitor_leads.py](recipes/exhibitor_leads.py) | Exhibitors of any trade show (paste its exhibitor-list link) > CSV with booth and contacts; missing emails found on each company's website | [Trade Show Exhibitor List Scraper](https://apify.com/tacps126/exhibition-scraper) + [Website Contact Details](https://apify.com/tacps126/contact-details) |
| [research_alerts.py](recipes/research_alerts.py) | New papers, preprints and patents for your topics, merged across OpenAlex, arXiv, PubMed and Europe PMC > CSV (or the most influential, `--influential`) | [Research Radar](https://apify.com/tacps126/research-radar) |
| [compare_fields.py](recipes/compare_fields.py) | Technology fields ranked by opportunity score, with the reasons, industry share and top companies > CSV | [Innovation Radar](https://apify.com/tacps126/innovation-radar) |
| [sanctions_check.py](recipes/sanctions_check.py) | A list of customers or suppliers screened against OFAC, UN, EU, UK, Canada and Swiss sanctions lists > CSV with a verdict per name | [Sanctions Screener](https://apify.com/tacps126/sanctions-screener) |
| [recall_alerts.py](recipes/recall_alerts.py) | Product recalls and safety alerts for your products, brands or ingredients (FDA, CPSC, Canada, UK, EU) > CSV | [Recalls Radar](https://apify.com/tacps126/recalls-radar) |
| [youtube_transcripts.py](recipes/youtube_transcripts.py) | Transcripts of a video, playlist, channel or search > one text file per video | [YouTube Transcripts](https://apify.com/tacps126/youtube-transcripts) |
| [stock_screener.py](recipes/stock_screener.py) | Daily stock screen: verdict, support and resistance, and which ready-made rules (pullback in uptrend, breakout on volume...) are true today with their past hit rate > CSV | [Stock Analyzer](https://apify.com/tacps126/stock-analyzer) |
| [market_movers.py](recipes/market_movers.py) | Kalshi and Polymarket markets that moved most in 24 hours > CSV | [Prediction Markets](https://apify.com/tacps126/prediction-markets) |
| [closing_lines.py](recipes/closing_lines.py) | Last week's closing spread, total and moneyline with cover and over/under results > CSV for backtests | [Sports Data](https://apify.com/tacps126/sports-data) |
| [funding_leads.py](recipes/funding_leads.py) | Companies that just raised money (SEC Form D) in your states, with founders and executives > CSV | [Startup Funding Rounds](https://apify.com/tacps126/startup-funding) |
| [podcast_outreach.py](recipes/podcast_outreach.py) | Active podcasts in your niche with the owner's email, for guest pitches and sponsorships > CSV | [Podcast Scraper](https://apify.com/tacps126/podcasts) |
| [auction_deals.py](recipes/auction_deals.py) | Court, bank and government property auctions near a place, scored against similar lots and your budget > CSV | [Auctions Radar](https://apify.com/tacps126/auctions-radar) |
| [cve_alerts.py](recipes/cve_alerts.py) | New CVEs for your vendors, exploited-in-the-wild and likeliest-to-be-exploited first > CSV | [CVE Vulnerability Feed](https://apify.com/tacps126/cve-feed) |
| [trial_sites.py](recipes/trial_sites.py) | Recruiting clinical trials for a condition, one row per study site in your country, with contacts > CSV | [Clinical Trials Scraper](https://apify.com/tacps126/clinical-trials) |
| [new_practices.py](recipes/new_practices.py) | New US practices of a specialty (recently issued NPIs) with address and phone > CSV | [NPI Registry Scraper](https://apify.com/tacps126/npi-providers) |
| [importer_lookalikes.py](recipes/importer_lookalikes.py) | US brands that buy from the same factories as the importers you name, from customs bills of lading > CSV | [US Import Records](https://apify.com/tacps126/us-import-records) |
| [amazon_best_sellers.py](recipes/amazon_best_sellers.py) | Amazon products for your keywords ranked by "bought in past month", with price, discount and rating > CSV | [Amazon Product Scraper](https://apify.com/tacps126/amazon-products) |
| [facebook_page_contacts.py](recipes/facebook_page_contacts.py) | E-mail, phone, address, website and followers from a list of Facebook Pages > CSV | [Facebook Pages Scraper](https://apify.com/tacps126/facebook-pages) |
| [hotel_rates.py](recipes/hotel_rates.py) | Google Hotels prices for a place and dates, cheapest good hotels first > CSV | [Google Hotels Scraper](https://apify.com/tacps126/google-hotels) |
| [threads_mentions.py](recipes/threads_mentions.py) | New Threads posts mentioning your brand or topic, most engaged first; only-new on daily runs > CSV | [Threads Scraper](https://apify.com/tacps126/threads-scraper) |
| [music_artist_leads.py](recipes/music_artist_leads.py) | Independent SoundCloud and Spotify artists for your genres, best leads first, with listeners, latest release and e-mail > CSV | [Music Artist Scraper](https://apify.com/tacps126/media-profiles) |
| [creator_outreach.py](recipes/creator_outreach.py) | YouTube and Vimeo creators for your niche with real engagement, best leads first, with e-mail and socials > CSV | [Creator Finder](https://apify.com/tacps126/creator-finder) |
| [negative_reviews.sh](recipes/negative_reviews.sh) | 1-2★ Trustpilot reviews of competitors (curl only) | [Trustpilot Reviews](https://apify.com/tacps126/trustpilot-reviews) |

```bash
pip install requests
export APIFY_TOKEN=...
python recipes/news_alerts.py "generative AI"
```

All recipes use the synchronous endpoint
`POST /v2/acts/<actor>/run-sync-get-dataset-items`. It runs the Actor and returns the
results in the same request, up to 5 minutes. For longer runs, start a run and poll it;
see the [Apify API docs](https://docs.apify.com/api/v2).

## n8n, Make, Zapier and Clay

**Ready-made:** importable n8n workflows, Make and Zapier steps, and copy-paste Clay enrichment
inputs are in [integrations/](integrations/README.md).

The same endpoint works from any automation tool. In n8n: add an **HTTP Request** node with
`POST https://api.apify.com/v2/acts/<actor>/run-sync-get-dataset-items`, header
`Authorization: Bearer <token>`, your input as the JSON body and a 330-second timeout. Each result
becomes one n8n item, so you can map fields straight into Sheets, a CRM or a database. Our actors
return normalized fields in one schema; the [exhibitor scraper](https://apify.com/tacps126/exhibition-scraper)
can also add each organiser's original record (`includeRawData`).

Missing a source, or found a problem? Open an issue on the Actor's page in Apify Store.

All rights reserved; see [LICENSE](LICENSE). You may run and adapt these scripts to call the Actors
they name.
