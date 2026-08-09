import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://lutheranworld.org/member-churches/search"
OUTPUT_FILE = "lwf_churches.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


# ISO-style country codes used by the LWF Drupal search.
# The script can be expanded if the site adds countries.
COUNTRIES = [
    "AF", "AL", "AR", "AT", "AU", "BE", "BO", "BR", "BW", "CA",
    "CD", "CF", "CG", "CH", "CL", "CN", "CO", "CR", "CZ", "DE",
    "DK", "DO", "EC", "EE", "EG", "ER", "ES", "ET", "FI", "FR",
    "GB", "GH", "GR", "GT", "HN", "HU", "ID", "IE", "IN", "IS",
    "IT", "JP", "KE", "KH", "KR", "LT", "LU", "LV", "MG", "ML",
    "MM", "MW", "MX", "MZ", "NA", "NG", "NI", "NL", "NO", "NP",
    "NZ", "PE", "PG", "PH", "PL", "PR", "PT", "PY", "RO", "RU",
    "SE", "SG", "SK", "SL", "SN", "SO", "SS", "SV", "SZ", "TG",
    "TH", "TJ", "TN", "TR", "TZ", "TW", "UA", "UG", "US", "UY",
    "VE", "VN", "ZA", "ZM", "ZW", "JO", "PS"
]


def make_id(name):
    """
    Convert a church name into the style used by your dataset.
    """
    name = name.lower()

    # Remove punctuation
    name = re.sub(r"[^a-z0-9]+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    return name


def parse_number(text):
    """
    Convert strings such as:
        12000000
        610503.
        1,200,000
    into integers.
    """
    match = re.search(r"\d[\d,\.]*", text)

    if not match:
        return None

    value = match.group(0)

    # LWF sometimes renders decimal fields as "12000000."
    value = value.replace(",", "").rstrip(".")

    try:
        return int(value)
    except ValueError:
        return None


def extract_churches(html):
    soup = BeautifulSoup(html, "html.parser")

    churches = []

    # Each church is represented by an article of this type.
    articles = soup.select(
        "article.node--type-churches"
    )

    for article in articles:
        title = article.select_one(
            ".field--name-title"
        )

        if not title:
            continue

        name = title.get_text(" ", strip=True)

        # Look specifically for the "Number of Members" field.
        members = None

        for item in article.select(
            ".field--name-field-ph-keym-amount"
        ):
            unit = item.select_one(
                ".ino-pt-keym-unit"
            )

            if not unit:
                continue

            unit_text = unit.get_text(
                " ", strip=True
            ).lower()

            if "number of members" in unit_text:
                amount = item.select_one(
                    ".ino-pt-keym-amount"
                )

                if amount:
                    members = parse_number(
                        amount.get_text(" ", strip=True)
                    )

                break

        # Ignore entries without a membership number.
        if members is None:
            print(
                f"WARNING: No membership count found: {name}"
            )
            continue

        church = {
            "id": make_id(name),
            "name": name,
            "tradition": "Lutheran",
            "members": members
        }

        churches.append(church)

    return churches


def main():
    session = requests.Session()
    session.headers.update(HEADERS)

    all_churches = []
    seen_ids = set()

    for country in COUNTRIES:
        print(f"Checking {country}...")

        try:
            response = session.get(
                BASE_URL,
                params={
                    "field_n_country": country
                },
                timeout=30
            )

            response.raise_for_status()

        except requests.RequestException as e:
            print(
                f"ERROR retrieving {country}: {e}"
            )
            continue

        churches = extract_churches(
            response.text
        )

        for church in churches:

            # Prevent duplicates caused by a church
            # appearing in multiple search results.
            if church["id"] in seen_ids:
                continue

            seen_ids.add(church["id"])
            all_churches.append(church)

            print(
                f"  + {church['name']} "
                f"({church['members']:,})"
            )

        # Be polite to the server.
        time.sleep(0.5)

    # Sort alphabetically.
    all_churches.sort(
        key=lambda church: church["name"].lower()
    )

    output = {
        "churches": all_churches
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print(
        f"Found {len(all_churches)} churches."
    )
    print(
        f"Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()