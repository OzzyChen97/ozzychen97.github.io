import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


DATASET_ID = os.environ.get("HF_DATASET_ID", "OzzyChen97/TC-SSA")
API_URL = (
    "https://huggingface.co/api/datasets/"
    f"{quote(DATASET_ID, safe='/')}?expand=downloads&expand=downloadsAllTime"
)


def fetch_dataset_stats():
    request = Request(API_URL, headers={"User-Agent": "ozzychen97.github.io-stats/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)

    total_downloads = payload.get("downloadsAllTime")
    if not isinstance(total_downloads, int) or total_downloads < 0:
        raise ValueError("Hugging Face API did not return a valid downloadsAllTime value")

    downloads_last_30_days = payload.get("downloads")
    if not isinstance(downloads_last_30_days, int) or downloads_last_30_days < 0:
        downloads_last_30_days = None

    return {
        "dataset": payload.get("id", DATASET_ID),
        "total_downloads": total_downloads,
        "downloads_last_30_days": downloads_last_30_days,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    try:
        stats = fetch_dataset_stats()
    except Exception as error:
        print(f"Error fetching Hugging Face dataset stats: {error}", file=sys.stderr)
        sys.exit(1)

    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    with (results_dir / "hf_data.json").open("w", encoding="utf-8") as output:
        json.dump(stats, output, ensure_ascii=False, indent=2)
        output.write("\n")

    shield_data = {
        "schemaVersion": 1,
        "label": "total downloads",
        "message": str(stats["total_downloads"]),
    }
    with (results_dir / "hf_data_shieldsio.json").open("w", encoding="utf-8") as output:
        json.dump(shield_data, output, ensure_ascii=False)
        output.write("\n")

    print(f"Dataset: {stats['dataset']}")
    print(f"Total downloads: {stats['total_downloads']}")
    print(f"Downloads in the last 30 days: {stats['downloads_last_30_days']}")


if __name__ == "__main__":
    main()
