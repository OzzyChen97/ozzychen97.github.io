"""Report whether the published Google Scholar snapshot needs refreshing."""

import json
import sys
from datetime import datetime, timedelta, timezone


def snapshot_age(path):
    try:
        with open(path, encoding="utf-8") as snapshot_file:
            snapshot = json.load(snapshot_file)
        if not isinstance(snapshot.get("citedby"), int):
            raise ValueError("Citation count is missing")
        updated = datetime.fromisoformat(snapshot["updated"])
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        age = datetime.now(timezone.utc) - updated
        if age < timedelta(0):
            raise ValueError("Snapshot timestamp is in the future")
        return age
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def main():
    age = snapshot_age(sys.argv[1])
    hours = int(age.total_seconds() // 3600) if age is not None else -1
    print(f"age_hours={hours}")
    print(f"due={'true' if age is None or age >= timedelta(hours=20) else 'false'}")
    print(f"stale={'true' if age is None or age >= timedelta(hours=48) else 'false'}")


if __name__ == "__main__":
    main()
