#!/usr/bin/env python3
"""Fetch the concert schedule from Google Sheets API v4 and write concerts.json.

Requires the sheet to be shared as 'Anyone with the link can view' and a
Google Sheets API key stored in the SHEETS_API_KEY environment variable.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

SHEET_ID = "1E2w7kju5AWI8PF-Xs3PpVoBV6vawBXW9xu40Ym5STZs"
RANGE    = "Sheet1!A:G"

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


def fetch_rows(api_key):
    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"
        f"/values/{urllib.parse.quote(RANGE)}?key={urllib.parse.quote(api_key)}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "sync-concerts/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("values", [])


def convert(rows):
    if not rows:
        return []

    headers = [h.strip() for h in rows[0]]

    # Map expected column names to their index (tolerates extra/missing columns)
    col = {h: i for i, h in enumerate(headers)}

    def get(row, name):
        i = col.get(name)
        return row[i].strip() if i is not None and i < len(row) else ""

    concerts = []
    concert_id = 1
    for row in rows[1:]:
        date_str = get(row, "Dato")
        if not date_str:
            continue

        title   = get(row, "Koncert navn")
        venue   = get(row, "Sted(kirkens navn fx)")
        address = get(row, "Adresse")
        time_val = get(row, "Tid")
        price    = get(row, "Pris")
        desc     = get(row, "Beskrivelse af koncerten")

        # Use venue name as title when title cell is empty
        if not title:
            title = venue

        concerts.append({
            "id": concert_id,
            **parse_date(date_str),
            "time":        time_val,
            "title":       title,
            "venue":       venue,
            "address":     address,
            "price":       price,
            "description": desc,
            "soldOut":     False,
        })
        concert_id += 1

    return concerts


def main():
    api_key = os.environ.get("SHEETS_API_KEY", "").strip()
    if not api_key:
        print("ERROR: SHEETS_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    try:
        rows = fetch_rows(api_key)
    except Exception as exc:
        print(f"ERROR: could not fetch sheet — {exc}", file=sys.stderr)
        sys.exit(1)

    concerts = convert(rows)
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
