import csv
from datetime import datetime

def extract(body: str) -> list[dict]:
    """Parse a CriminalIP C2 daily feed CSV and return a list of payloads.

    The feed is a CSV with columns: IP, flag, port, score, country, scanTime.
    The header row (where IP == "IP") is skipped automatically.

    Each returned payload conforms to the standard shape:
        {
            "ip": str,
            "flags": [str],
            "results": [{ "source", "datetime", "flags", "metadata" }]
        }
    """
    payloads = []

    content = body.splitlines()[1:]  # Skip the header row
    reader = csv.reader(content)

    for row in reader:
        ip, flag, port, score, country, scan_time = row

        payloads.append({
            "ip": ip,
            "flags": [flag.lower()],
            "results": [{
                "source": "criminalip",
                # Record when this aggregator ingested the entry, not the scan time
                "datetime": datetime.now().isoformat(),
                "flags": [flag.lower()],
                "metadata": {
                    "port": port,
                    "score": score,
                    "country": country,
                    "scanTime": scan_time,  # original scan timestamp from the feed
                },
            }],
        })

    return payloads
