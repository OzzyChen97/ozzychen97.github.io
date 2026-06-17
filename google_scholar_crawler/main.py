from scholarly import scholarly
import json
from datetime import datetime
import os
import re
import sys

def get_author_id():
    author_id = os.environ.get('GOOGLE_SCHOLAR_ID')
    if author_id:
        return author_id

    config_path = os.path.join(os.path.dirname(__file__), '..', '_config.yml')
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = config_file.read()
    except OSError:
        return None

    match = re.search(r'googlescholar\s*:\s*"?[^"\n]*[?&]user=([^"&\s]+)', config)
    if match:
        return match.group(1)

    return None

def main():
    script_dir = os.path.dirname(__file__)

    # Fetch author profile from Google Scholar
    author_id = get_author_id()
    if not author_id:
        print("Error: Google Scholar ID was not found.")
        print("Set GOOGLE_SCHOLAR_ID in repo secrets or add author.googlescholar to _config.yml.")
        sys.exit(1)

    print(f"Fetching data for Google Scholar ID: {author_id}")

    try:
        author = scholarly.search_author_id(author_id)
        scholarly.fill(author, sections=['basics', 'indices', 'counts'])
    except Exception as e:
        print(f"Error fetching Google Scholar data: {e}")
        print("This may be due to rate limiting or network issues. Try running the workflow again.")
        sys.exit(1)

    name = author['name']
    author['updated'] = str(datetime.now())

    try:
        scholarly.fill(author, sections=['publications'])
        author['publications'] = {
            v['author_pub_id']: v for v in author.get('publications', [])
        }
    except Exception as e:
        print(f"Warning: could not fetch publication-level citation data: {e}")
        print("Continuing with total citation data only.")
        author['publications'] = {}

    print(f"Author: {name}")
    print(f"Total citations: {author.get('citedby', 'N/A')}")
    print(f"Publications: {len(author['publications'])}")

    for pub_id, pub in author['publications'].items():
        title = pub.get('bib', {}).get('title', 'Untitled')
        citations = pub.get('num_citations', 0)
        print(f"  - {title} (citations: {citations})")

    # Write full data
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, 'gs_data.json'), 'w') as outfile:
        json.dump(author, outfile, ensure_ascii=False, indent=2)

    # Write shields.io compatible data
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author.get('citedby', 0)}",
    }
    with open(os.path.join(results_dir, 'gs_data_shieldsio.json'), 'w') as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)

    print("Data written to results/")

if __name__ == '__main__':
    main()
