"""Report whether the published Google Scholar snapshot needs refreshing.

Prints GitHub Actions output lines:

* ``age_hours`` - age of the published snapshot, or -1 if it is missing/invalid
* ``due``       - true when a refresh should be attempted (>= 20 hours old)
* ``stale``     - true when a failed refresh deserves a warning (>= 48 hours old)
* ``expired``   - true when a failed refresh should fail the job (>= 7 days old)
"""

import json
import sys
from datetime import datetime, timedelta, timezone

DUE_AFTER = timedelta(hours=20)
STALE_AFTER = timedelta(hours=48)
EXPIRED_AFTER = timedelta(days=7)


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


def flag(age, threshold):
    return "true" if age is None or age >= threshold else "false"


def main():
    age = snapshot_age(sys.argv[1])
    hours = int(age.total_seconds() // 3600) if age is not None else -1
    print(f"age_hours={hours}")
    print(f"due={flag(age, DUE_AFTER)}")
    print(f"stale={flag(age, STALE_AFTER)}")
    print(f"expired={flag(age, EXPIRED_AFTER)}")


if __name__ == "__main__":
    main()
