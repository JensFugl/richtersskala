#!/usr/bin/env python3
"""Fetch the concert schedule from Google Sheets (published CSV) and write concerts.json."""

import csv
import json
import sys
import urllib.request
from datetime import datetime

SHEET_ID = "1E2w7kju5AWI8PF-Xs3PpVoBV6vawBXW9xu40Ym5STZs"
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    "/pub?gid=0&single=true&output=csv"
)

# Danish month names: number → (full, abbreviated)
DANISH_MONTHS = {
    1:  ("januar",    "jan"),
    2:  ("februar",   "feb"),
    3:  ("marts",     "mar"),
    4:  ("april",     "apr"),
    5:  ("maj",       "maj"),
    6:  ("juni",      "jun"),
    7:  ("juli",      "jul"),
    8:  ("august",    "aug"),
    9:  ("september", "sep"),
    10: ("oktober",   "okt"),
    11: ("november",  "nov"),
    12: ("december",  "dec"),
}


def parse_date(date_str):
    """Convert DD-MM-YYYY to the Danish display fields the frontend expects."""
    dt = datetime.strptime(date_str.strip(), "%d-%m-%Y")
    full_month, abbr_month = DANISH_MONTHS[dt.month]
    return {
        "date": f"{dt.day}. {full_month} {dt.year}",
        "day": str(dt.day),
        "month": f"{abbr_month} {dt.year}",
    }


def fetch_csv():
    req = urllib.request.Request(CSV_URL, headers={"User-Agent": "sync-concerts/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8-sig")


def convert(content):
    reader = csv.DictReader(content.splitlines())
    concerts = []
    for i, row in enumerate(reader, start=1):
        title   = row.get("Koncert navn", "").strip()
        venue   = row.get("Sted(kirkens navn fx)", "").strip()
        address = row.get("Adresse", "").strip()
        date_str = row.get("Dato", "").strip()
        time_val = row.get("Tid", "").strip()
        price    = row.get("Pris", "").strip()
        desc     = row.get("Beskrivelse af koncerten", "").strip()

        if not date_str:
            continue

        # Use venue name as title when title cell is empty
        if not title:
            title = venue

        concerts.append({
            "id": i,
            **parse_date(date_str),
            "time":        time_val,
            "title":       title,
            "venue":       venue,
            "address":     address,
            "price":       price,
            "description": desc,
            "soldOut":     False,
        })
    return concerts


def main():
    try:
        content = fetch_csv()
    except Exception as exc:
        print(f"ERROR: could not fetch sheet — {exc}", file=sys.stderr)
        sys.exit(1)

    concerts = convert(content)
    if not concerts:
        print("ERROR: no concerts parsed from sheet", file=sys.stderr)
        sys.exit(1)

    out_path = "concerts.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(concerts, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(concerts)} concert(s) to {out_path}")


if __name__ == "__main__":
    main()
