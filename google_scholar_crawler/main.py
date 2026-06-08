from scholarly import scholarly
import json
from datetime import datetime
import os
import sys

def main():
    # Fetch author profile from Google Scholar
    author_id = os.environ.get('GOOGLE_SCHOLAR_ID')
    if not author_id:
        print("Error: GOOGLE_SCHOLAR_ID environment variable is not set.")
        print("Please add it in your repo Settings > Secrets and variables > Actions.")
        sys.exit(1)

    print(f"Fetching data for Google Scholar ID: {author_id}")

    try:
        author = scholarly.search_author_id(author_id)
        scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    except Exception as e:
        print(f"Error fetching Google Scholar data: {e}")
        print("This may be due to rate limiting or network issues. Try running the workflow again.")
        sys.exit(1)

    name = author['name']
    author['updated'] = str(datetime.now())

    # Convert publications list to dict keyed by author_pub_id
    author['publications'] = {
        v['author_pub_id']: v for v in author['publications']
    }

    print(f"Author: {name}")
    print(f"Total citations: {author.get('citedby', 'N/A')}")
    print(f"Publications: {len(author['publications'])}")

    for pub_id, pub in author['publications'].items():
        title = pub.get('bib', {}).get('title', 'Untitled')
        citations = pub.get('num_citations', 0)
        print(f"  - {title} (citations: {citations})")

    # Write full data
    os.makedirs('results', exist_ok=True)
    with open('results/gs_data.json', 'w') as outfile:
        json.dump(author, outfile, ensure_ascii=False, indent=2)

    # Write shields.io compatible data
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author.get('citedby', 0)}",
    }
    with open('results/gs_data_shieldsio.json', 'w') as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)

    print("Data written to results/")

if __name__ == '__main__':
    main()
