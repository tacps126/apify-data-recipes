"""Tiny helper: run an Apify Actor and return its results (one HTTP request)."""

import os
import sys

import requests


def run(actor: str, payload: dict, timeout: int = 300) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN (Apify Console → Settings → API & Integrations).")
    r = requests.post(
        f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=timeout + 30,
    )
    r.raise_for_status()
    return r.json()
