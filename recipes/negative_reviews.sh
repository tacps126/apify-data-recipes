#!/usr/bin/env bash
# 1–2★ English Trustpilot reviews for the companies given → reviews.json
# Cost: about $0.0005 per review. Usage: ./negative_reviews.sh hubspot.com salesforce.com
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN}"
companies=$(printf '"%s",' "${@:-hubspot.com}"); companies="[${companies%,}]"
curl -sS -X POST \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d "{\"companies\": $companies, \"starRatings\": [\"1\",\"2\"], \"language\": \"en\", \"maxReviews\": 200}" \
  "https://api.apify.com/v2/acts/tacps126~trustpilot-reviews/run-sync-get-dataset-items" > reviews.json
echo "saved $(python3 -c 'import json;print(len(json.load(open("reviews.json"))))') reviews → reviews.json"
