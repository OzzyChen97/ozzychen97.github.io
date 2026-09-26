"""Fetch Google Scholar citation data for the homepage.

Google blocks most datacenter networks, including GitHub-hosted runners, so the
profile page is requested through several routes in turn:

1. ``direct``    - scholar.google.com itself (works from residential networks).
2. ``translate`` - the Google Translate web proxy, which sometimes works where
                   direct requests are blocked.
3. ``wayback``   - the Internet Archive's "Save Page Now" service. archive.org
                   crawls the profile from its own network and returns the
                   captured HTML, so this route does not depend on the caller's
                   IP address.

The first route that returns a parsable profile wins. Routes can be selected
with ``GOOGLE_SCHOLAR_ROUTES`` (comma separated, e.g. ``wayback``).

Exit codes:

* 0  - citation data written to ``results/``
* 75 - every route was temporarily unavailable (rate limit, CAPTCHA, timeout);
       the workflow keeps the previously published snapshot
* 1  - configuration or parsing error that needs attention
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


PROFILE_URL = "https://scholar.google.com/citations"
TRANSLATED_PROFILE_URL = "https://scholar-google-com.translate.goog/citations"
WAYBACK_SAVE_URL = "https://web.archive.org/save/"
WAYBACK_TIMESTAMP_RE = re.compile(r"/web/(\d{14})[a-z_]*/")
ALL_ROUTES = ("direct", "translate", "wayback")
WAYBACK_ATTEMPTS = 2
WAYBACK_RETRY_DELAY_SECONDS = 20
# Save Page Now may hand back a recent capture instead of crawling again.
# Anything older than this is not a fresh reading and must not be published
# with a new "updated" timestamp.
WAYBACK_MAX_CAPTURE_AGE = timedelta(hours=36)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 Chrome/120 Safari/537.36"
)
EXIT_TEMPORARILY_UNAVAILABLE = 75


class ScholarTemporarilyUnavailable(Exception):
    """A route was blocked, rate limited, or timed out."""


class ScholarPageUnparsable(Exception):
    """A route returned HTML without the expected profile data."""


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


def get_routes():
    configured = os.environ.get("GOOGLE_SCHOLAR_ROUTES", "")
    routes = [route.strip().lower() for route in configured.split(",")]
    routes = [route for route in routes if route]
    if not routes:
        routes = list(ALL_ROUTES)
        if os.environ.get("GOOGLE_SCHOLAR_TRANSLATE_ONLY") == "true":
            routes.remove("direct")

    unknown = [route for route in routes if route not in ALL_ROUTES]
    if unknown:
        raise ValueError(
            "Unknown GOOGLE_SCHOLAR_ROUTES entries: "
            + ", ".join(unknown)
            + ". Valid routes: "
            + ", ".join(ALL_ROUTES)
        )
    return routes


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
        {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def profile_params(author_id):
    return {
        "hl": "en",
        "user": author_id,
        "view_op": "list_works",
        "pagesize": 100,
    }


def parse_number(text):
    match = re.search(r"\d[\d,]*", text or "")
    return int(match.group(0).replace(",", "")) if match else 0


def parse_metrics(soup):
    table = soup.select_one("#gsc_rsb_st")
    if table is None:
        raise ScholarPageUnparsable("Google Scholar metrics table was not found.")

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
        raise ScholarPageUnparsable("Google Scholar citation total was not found.")
    return metrics


def parse_publications(soup):
    publications = {}
    rows = soup.select("#gsc_a_b tr.gsc_a_tr")
    if not rows:
        raise ScholarPageUnparsable("Google Scholar publication rows were not found.")

    for index, row in enumerate(rows):
        title_el = row.select_one(".gsc_a_at")
        if title_el is None:
            continue

        # Links may be rewritten by a proxy (Wayback prefixes the original URL);
        # the query string still carries citation_for_view either way.
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
        raise ScholarPageUnparsable("Google Scholar publications could not be parsed.")
    return publications


def parse_author(html, author_id):
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
    }


def has_captcha(html):
    if "unusual traffic" in html:
        return True
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one("#gs_captcha_ccl, #recaptcha, #captcha-form") is not None


def raise_if_blocked(response, route):
    if response.status_code in (403, 429) or response.status_code >= 500:
        raise ScholarTemporarilyUnavailable(
            f"{route}: HTTP {response.status_code} from {urlparse(response.url).netloc}"
        )
    if has_captcha(response.text):
        raise ScholarTemporarilyUnavailable(f"{route}: Google Scholar returned a CAPTCHA page")
    response.raise_for_status()


def fetch_direct(session, author_id):
    response = session.get(
        PROFILE_URL, params=profile_params(author_id), timeout=(5, 20)
    )
    raise_if_blocked(response, "direct")
    return response.text


def fetch_translate(session, author_id):
    params = {
        **profile_params(author_id),
        "_citation_snapshot": str(int(time.time())),
        "_x_tr_sl": "auto",
        "_x_tr_tl": "en",
        "_x_tr_hl": "en",
    }
    response = session.get(TRANSLATED_PROFILE_URL, params=params, timeout=(5, 30))
    raise_if_blocked(response, "translate")
    return response.text


def wayback_capture_time(url):
    """Return the capture time encoded in a Wayback replay URL, or None."""
    match = WAYBACK_TIMESTAMP_RE.search(url)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y%m%d%H%M%S").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None


def fetch_wayback(session, author_id):
    """Ask archive.org to capture the profile now and return the captured HTML."""
    # Save Page Now reuses a recent capture of the same URL instead of crawling
    # again. A per-day parameter (ignored by Google Scholar) makes the first
    # run of each UTC day crawl a fresh copy while later runs reuse it.
    params = {
        **profile_params(author_id),
        "_snapshot": datetime.now(timezone.utc).strftime("%Y%m%d"),
    }
    target = f"{PROFILE_URL}?{urlencode(params)}"
    last_error = None
    for attempt in range(1, WAYBACK_ATTEMPTS + 1):
        try:
            response = session.get(
                WAYBACK_SAVE_URL + target, timeout=(10, 120), allow_redirects=True
            )
        except (requests.ConnectionError, requests.Timeout) as error:
            last_error = ScholarTemporarilyUnavailable(f"wayback: {error}")
        else:
            if response.status_code == 429 or response.status_code >= 500:
                last_error = ScholarTemporarilyUnavailable(
                    f"wayback: HTTP {response.status_code} from archive.org"
                )
            elif not response.ok:
                # Other 4xx responses (for example an excluded URL) will not
                # change on retry.
                raise ScholarTemporarilyUnavailable(
                    f"wayback: HTTP {response.status_code} from archive.org"
                )
            elif has_captcha(response.text):
                raise ScholarTemporarilyUnavailable(
                    "wayback: archive.org captured a CAPTCHA page from Google Scholar"
                )
            else:
                captured_at = wayback_capture_time(response.url)
                if captured_at is None:
                    raise ScholarTemporarilyUnavailable(
                        f"wayback: unexpected final URL {response.url}"
                    )
                age = datetime.now(timezone.utc) - captured_at
                print(
                    f"Wayback capture time: {captured_at.isoformat()} "
                    f"({int(age.total_seconds() // 60)} minutes ago)"
                )
                if age > WAYBACK_MAX_CAPTURE_AGE:
                    raise ScholarTemporarilyUnavailable(
                        "wayback: archive.org returned a capture from "
                        f"{captured_at.isoformat()}, older than "
                        f"{WAYBACK_MAX_CAPTURE_AGE}"
                    )
                return response.text

        if attempt < WAYBACK_ATTEMPTS:
            print(
                f"  attempt {attempt}/{WAYBACK_ATTEMPTS} failed ({last_error}); "
                f"retrying in {WAYBACK_RETRY_DELAY_SECONDS}s",
                file=sys.stderr,
            )
            time.sleep(WAYBACK_RETRY_DELAY_SECONDS)
    raise last_error


FETCHERS = {
    "direct": fetch_direct,
    "translate": fetch_translate,
    "wayback": fetch_wayback,
}


def fetch_author(author_id, routes):
    session = make_session()
    temporary_errors = []
    hard_errors = []

    for route in routes:
        print(f"Trying route: {route}")
        try:
            html = FETCHERS[route](session, author_id)
            author = parse_author(html, author_id)
        except (
            ScholarTemporarilyUnavailable,
            requests.ConnectionError,
            requests.Timeout,
            requests.exceptions.RetryError,
        ) as error:
            print(f"  unavailable: {error}", file=sys.stderr)
            temporary_errors.append(f"{route}: {error}")
            continue
        except (requests.RequestException, ScholarPageUnparsable) as error:
            print(f"  failed: {error}", file=sys.stderr)
            hard_errors.append(f"{route}: {error}")
            continue

        print(f"  succeeded via {route}")
        author["source_route"] = route
        return author

    summary = "; ".join(temporary_errors + hard_errors)
    if temporary_errors:
        raise ScholarTemporarilyUnavailable(summary)
    raise ScholarPageUnparsable(summary)


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

    try:
        routes = get_routes()
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Fetching Google Scholar profile for: {author_id}")
    print(f"Routes: {', '.join(routes)}")
    try:
        author = fetch_author(author_id, routes)
    except ScholarTemporarilyUnavailable as error:
        print(f"Google Scholar is temporarily unavailable: {error}", file=sys.stderr)
        print("The previous citation snapshot will be kept.", file=sys.stderr)
        return EXIT_TEMPORARILY_UNAVAILABLE
    except ScholarPageUnparsable as error:
        print(f"Error parsing Google Scholar data: {error}", file=sys.stderr)
        print("The previous citation snapshot will be kept.", file=sys.stderr)
        return 1

    author["updated"] = datetime.now(timezone.utc).isoformat()
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
