# Use our data tools in n8n, Make, Zapier and Clay

Every tool runs on [Apify](https://apify.com/tacps126). You need a free Apify account and its
API token (Apify Console > **Settings > API & Integrations**). New here?
[Create a free account](https://console.apify.com/sign-up): the free plan includes monthly
usage, enough to try any tool on real data.

| Tool | Best for | Ready-made |
|------|----------|-----------|
| [n8n](https://n8n.io/) | Scheduled pipelines, self-hosting | 6 importable workflows below |
| [Make](https://www.make.com/) | Visual scenarios, no code | Step-by-step below |
| Zapier | Simple "when X, do Y" | Step-by-step below |
| [Clay](https://clay.com?via=bec1a7) | Enriching a lead table row by row | Copy-paste inputs below |

---

## n8n

**Import a ready workflow:** download a file below, then in n8n: *Workflows > Add workflow > ⋯ > 
Import from file*.

| Workflow | What it does |
|----------|--------------|
| [exhibitors-to-google-sheets.json](n8n/exhibitors-to-google-sheets.json) | A trade show's exhibitor list (company, booth, email, phone, website, city, country) into a Google Sheet |
| [weekly-hiring-signals-to-google-sheets.json](n8n/weekly-hiring-signals-to-google-sheets.json) | Every Monday: which of your target accounts opened roles you sell to, scored per company |
| [weekly-auction-deals-to-google-sheets.json](n8n/weekly-auction-deals-to-google-sheets.json) | Every Monday: new and changed court, bank and government auction lots near your place, scored against similar lots and your budget |
| [daily-new-companies-to-google-sheets.json](n8n/daily-new-companies-to-google-sheets.json) | Every morning: companies registered since the last run in the official registers you pick |
| [weekly-sanctions-screening-to-google-sheets.json](n8n/weekly-sanctions-screening-to-google-sheets.json) | Every Monday: your customers and suppliers screened against six official sanctions lists, one verdict per name |
| [weekly-channel-transcripts-to-google-sheets.json](n8n/weekly-channel-transcripts-to-google-sheets.json) | Every Friday: transcripts of a YouTube channel's new videos, one row per video |

After import:
1. Open the **HTTP Request** node > *Credential* > *Create new* > **Header Auth**. Name `Authorization`,
   value `Bearer <your Apify token>`.
2. Change the JSON body to your show, accounts, place, names, channel or keywords.
3. Open the **Google Sheets** node, connect Google and paste your sheet's URL.
4. Click *Execute workflow* (or *Activate* for the weekly one).

**Any other tool, by hand:** HTTP Request node, `POST`
`https://api.apify.com/v2/acts/tacps126~<tool-name>/run-sync-get-dataset-items`, same Header Auth,
JSON body = the tool's input, *Options > Timeout* `330000`. Each result becomes one n8n item. The
endpoint waits up to 5 minutes; for big jobs start the run with `/runs` and read its dataset later.

You can also install Apify's own n8n node (`@apify/n8n-nodes-apify`): *Run an Actor* with
`tacps126/<tool-name>`, then *Get dataset items*.

---

## Make

1. Create a scenario and add the **Apify** app > **Run an Actor**.
2. Connect with your Apify API token.
3. *Actor*: type `tacps126/<tool-name>` (e.g. `tacps126/exhibition-scraper`). Turn on **Run synchronously**.
4. *Input JSON*: paste the tool's input, for example
   `{"exhibitionList": ["automechanika-dubai"], "maxResults": 200}`.
5. Add **Apify > Get Dataset Items** with *Dataset ID* = the run's `defaultDatasetId`.
6. Add Google Sheets *Add a Row*, HubSpot *Create a Contact*, Airtable or Slack and map the fields.

For a schedule, set the scenario's clock (e.g. every Monday 07:00). For alerts, use the tool's
*only new* setting so each run returns only what's new.

---

## Zapier

1. Create a Zap. **Trigger**: Schedule by Zapier (e.g. every week), or any app event.
2. **Action**: **Apify > Run Actor**. Connect with your Apify API token, *Actor* `tacps126/<tool-name>`,
   *Input* the tool's JSON, *Wait for finish*: yes.
3. **Action**: **Apify > Fetch Dataset Items** from that run.
4. **Action**: Google Sheets *Create Spreadsheet Row(s)*, HubSpot, Slack, Gmail...

To react to runs you schedule in Apify instead: trigger **Apify > Finished Actor Run**, then
*Fetch Dataset Items*.

---

## Clay

Clay can run our tools as an enrichment on every row of a table.

1. In Clay: *Settings > Connections > Add connection > Apify*, paste your Apify API token.
2. In your table: *Add enrichment* > **Run Apify Actor** > pick the Apify account.
3. *Actor*: `tacps126/<tool-name>`. *Input*: one of the bodies below. Where it says
   `/Website` or `/Company Name`, type `/` and pick that column. Don't put quotes around the column.
4. Map the output fields to new columns. Optional: *Run settings > only run if* the column isn't empty.

| Enrich a row with | Tool | Input |
|-------------------|------|-------|
| Emails, phones, LinkedIn from the company website | `contact-details` | `{"startUrls": [/Website], "maxPagesPerSite": 5}` |
| Is the company hiring for roles you sell to? | `hiring-signals` | `{"companies": [/Careers URL], "roleKeywords": ["security", "data"]}` |
| Sanctions check of the company or person | `sanctions-screener` | `{"names": [/Company Name], "minScore": 85}` |
| Official registry record (status, legal form, officers) | `company-registry` | `{"mode": "search", "names": [/Company Name], "countries": ["FR"]}` |

**Build a new lead table from a source** (one run > many rows): *Add data > Import from Apify > 
Actor run*, then pick a run of, for example, `tacps126/exhibition-scraper` (a show's exhibitors) or
`tacps126/company-registry` (newly registered companies). Then enrich those rows as above.

Useful outputs per tool:
- `contact-details`: `primaryEmail`, `primaryPhone`, `linkedin`, `contactPageUrl`
- `hiring-signals`: `signalScore`, `matchingRoles`, `newMatchingRoles`, `newestRolePostedAt`
- `sanctions-screener`: `status`, `topScore`, `matchCount`, `list`
- `company-registry`: `status`, `legalForm`, `industry`, `address.city`, `url`
- `exhibition-scraper`: `name`, `booth`, `contact.email`, `contact.phone`, `contact.website`, `address.country`

---

Found a tool useful? A short review on its Apify page helps other people find it.
