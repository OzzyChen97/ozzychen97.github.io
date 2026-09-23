import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


PROFILE_URL = "https://scholar.google.com/citations"
TRANSLATED_PROFILE_URL = "https://scholar-google-com.translate.goog/citations"


def get_author_id():
    author_id = os.environ.get("GOOGLE_SCHOLAR_ID")
    if author_id:
        return author_id

    config_path = os.path.join(os.path.dirname(__file__), "..", "_config.yml")
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = config_file.read()
    except OSError:
        return None

    match = re.search(
        r'googlescholar\s*:\s*"?[^"\n]*[?&]user=([^"&\s]+)', config
    )
    return match.group(1) if match else None


def make_session():
    retry = Retry(
        total=1,
        connect=1,
        read=1,
        status=1,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def parse_number(text):
    match = re.search(r"\d[\d,]*", text or "")
    return int(match.group(0).replace(",", "")) if match else 0


def parse_metrics(soup):
    table = soup.select_one("#gsc_rsb_st")
    if table is None:
        raise ValueError("Google Scholar metrics table was not found.")

    metrics = {}
    for row in table.select("tbody tr"):
        cells = row.select("td")
        if len(cells) < 2:
            continue
        label = cells[0].get_text(" ", strip=True)
        metrics[label] = [
            parse_number(cell.get_text(" ", strip=True)) for cell in cells[1:]
        ]

    if "Citations" not in metrics or not metrics["Citations"]:
        raise ValueError("Google Scholar citation total was not found.")
    return metrics


def parse_publications(soup):
    publications = {}
    rows = soup.select("#gsc_a_b tr.gsc_a_tr")
    if not rows:
        raise ValueError("Google Scholar publication rows were not found.")

    for index, row in enumerate(rows):
        title_el = row.select_one(".gsc_a_at")
        if title_el is None:
            continue

        href = title_el.get("href", "")
        query = parse_qs(urlparse(href).query)
        pub_id = query.get("citation_for_view", [f"publication-{index}"])[0]
        gray_lines = row.select(".gsc_a_t .gs_gray")
        authors = gray_lines[0].get_text(" ", strip=True) if gray_lines else ""
        citation = gray_lines[1].get_text("", strip=True) if len(gray_lines) > 1 else ""
        year_el = row.select_one(".gsc_a_y span")
        count_el = row.select_one(".gsc_a_ac")

        publications[pub_id] = {
            "container_type": "Publication",
            "source": "AUTHOR_PUBLICATION_ENTRY",
            "bib": {
                "title": title_el.get_text(" ", strip=True),
                "author": authors,
                "pub_year": year_el.get_text(" ", strip=True) if year_el else "",
                "citation": citation,
            },
            "filled": False,
            "author_pub_id": pub_id,
            "num_citations": parse_number(
                count_el.get_text(" ", strip=True) if count_el else ""
            ),
        }

    if not publications:
        raise ValueError("Google Scholar publications could not be parsed.")
    return publications


def has_captcha(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one("#gs_captcha_ccl, #recaptcha, #captcha-form") is not None


def fetch_profile_html(author_id):
    session = make_session()
    params = {
        "hl": "en",
        "user": author_id,
        "view_op": "list_works",
        "pagesize": 100,
    }
    response = session.get(
        PROFILE_URL,
        params=params,
        timeout=(5, 20),
    )
    if response.ok and not has_captcha(response.text):
        return response.text

    if response.status_code not in (403, 429) and not has_captcha(response.text):
        response.raise_for_status()

    print(
        "Direct Google Scholar access was blocked; retrying through Google Translate.",
        file=sys.stderr,
    )
    proxy_response = session.get(
        TRANSLATED_PROFILE_URL,
        params={
            **params,
            "_citation_snapshot": str(int(time.time())),
            "_x_tr_sl": "auto",
            "_x_tr_tl": "en",
            "_x_tr_hl": "en",
        },
        timeout=(5, 30),
    )
    proxy_response.raise_for_status()
    if has_captcha(proxy_response.text):
        raise RuntimeError(
            "Google Scholar returned a CAPTCHA page through Google Translate."
        )
    return proxy_response.text


def fetch_author(author_id):
    html = fetch_profile_html(author_id)

    soup = BeautifulSoup(html, "html.parser")

    metrics = parse_metrics(soup)
    publications = parse_publications(soup)
    name_el = soup.select_one("#gsc_prf_in")
    affiliation_el = soup.select_one("#gsc_prf_i .gsc_prf_il")

    def metric(name, column=0):
        values = metrics.get(name, [])
        return values[column] if len(values) > column else 0

    return {
        "container_type": "Author",
        "source": "AUTHOR_PROFILE_PAGE",
        "scholar_id": author_id,
        "name": name_el.get_text(" ", strip=True) if name_el else "",
        "affiliation": (
            affiliation_el.get_text(" ", strip=True) if affiliation_el else ""
        ),
        "citedby": metric("Citations"),
        "citedby5y": metric("Citations", 1),
        "hindex": metric("h-index"),
        "hindex5y": metric("h-index", 1),
        "i10index": metric("i10-index"),
        "i10index5y": metric("i10-index", 1),
        "publications": publications,
        "updated": datetime.now(timezone.utc).isoformat(),
    }


def write_results(author):
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)

    with open(
        os.path.join(results_dir, "gs_data.json"), "w", encoding="utf-8"
    ) as outfile:
        json.dump(author, outfile, ensure_ascii=False, indent=2)

    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author["citedby"]),
    }
    with open(
        os.path.join(results_dir, "gs_data_shieldsio.json"),
        "w",
        encoding="utf-8",
    ) as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)


def main():
    author_id = get_author_id()
    if not author_id:
        print("Error: Google Scholar ID was not found.", file=sys.stderr)
        print(
            "Set GOOGLE_SCHOLAR_ID in repo secrets or add author.googlescholar to _config.yml.",
            file=sys.stderr,
        )
        return 1

    print(f"Fetching Google Scholar profile for: {author_id}")
    try:
        author = fetch_author(author_id)
    except (requests.RequestException, RuntimeError, ValueError) as error:
        print(f"Error fetching Google Scholar data: {error}", file=sys.stderr)
        print("The previous citation snapshot will be kept.", file=sys.stderr)
        return 1

    write_results(author)
    print(f"Author: {author['name']}")
    print(f"Total citations: {author['citedby']}")
    print(f"Publications: {len(author['publications'])}")
    for publication in author["publications"].values():
        print(
            f"  - {publication['bib']['title']} "
            f"(citations: {publication['num_citations']})"
        )
    print("Data written to results/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
