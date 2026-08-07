from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


def _load_credentials() -> tuple[str, str]:
    """Load Adzuna credentials from the repository .env file."""
    repo_root = Path(__file__).resolve().parents[3]
    load_dotenv(repo_root / ".env")

    app_id = os.getenv("APP_ID")
    app_key = os.getenv("APP_KEY")
    if not app_id or not app_key:
        raise RuntimeError("Missing APP_ID or APP_KEY in .env")
    return app_id, app_key


def fetch_adzuna_sample(country: str, query: str, results_per_page: int = 5) -> dict[str, Any]:
    """Fetch a small sample of jobs from the Adzuna API."""
    app_id, app_key = _load_credentials()

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": query,
        "content-type": "application/json",
    }

    response = httpx.get(url, params=params, timeout=20.0)
    response.raise_for_status()
    return response.json()


def print_summary(payload: dict[str, Any], query: str, country: str, results_per_page: int) -> None:
    """Print a concise summary of the API response and a few job samples."""
    results = payload.get("results", [])
    print(f"Country: {country}")
    print(f"Query: {query}")
    print(f"Results returned: {len(results)}")
    print(f"Total available results: {payload.get('count', 'n/a')}")
    print("Top-level keys:")
    for key in sorted(payload.keys()):
        print(f"- {key}")

    print("\nSample jobs:")
    for index, job in enumerate(results[:results_per_page], start=1):
        location = job.get("location", {})
        print(f"\n[{index}] {job.get('title', 'N/A')}")
        print(f"  Company: {job.get('company', {}).get('display_name', 'N/A')}")
        print(f"  Location: {location.get('display_name', 'N/A')}")
        print(f"  Salary min/max: {job.get('salary_min', 'N/A')} / {job.get('salary_max', 'N/A')}")
        print(f"  Contract: {job.get('contract_type', 'N/A')} | {job.get('contract_time', 'N/A')}")
        print(f"  Created: {job.get('created', 'N/A')}")
        print(f"  Redirect URL: {job.get('redirect_url', 'N/A')}")
        print(f"  Category: {job.get('category', {}).get('label', 'N/A')}")
        print(f"  Description preview: {job.get('description', 'N/A')[:220]}")

    print("\nFirst result keys:")
    if results:
        for key in sorted(results[0].keys()):
            print(f"- {key}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a sample of jobs from Adzuna")
    parser.add_argument("--country", default="gb", help="Adzuna country code (default: gb)")
    parser.add_argument("--query", default="data engineer", help="Search query")
    parser.add_argument("--results-per-page", type=int, default=3, help="Number of results to fetch")
    args = parser.parse_args()

    payload = fetch_adzuna_sample(args.country, args.query, args.results_per_page)
    print_summary(payload, args.query, args.country, args.results_per_page)

    if args.results_per_page:
        print("\nRaw JSON preview:")
        print(json.dumps(payload, indent=2)[:4000])


if __name__ == "__main__":
    main()
