import csv
from datetime import datetime

def extract(body: str) -> list[dict]:
    
    payloads = []

    content = body.splitlines()[1:]  # Skip the header row
    reader = csv.reader(content)

    for row in reader:
        flag, login, ip, firstSeenStr = row
        firstSeen = datetime.strptime(firstSeenStr, "%d-%m-%Y")

        payloads.append({
            "ip": ip,
            "flags": [flag.lower()],
            "results": [{
                "source": "viribacktracker",
                # Record when this aggregator ingested the entry, not the scan time
                "datetime": datetime.now().isoformat(),
                "flags": [flag.lower()],
                "metadata": {
                    "firstSeen": firstSeen.isoformat(),
                    "login": login,
                },
            }],
        })

    return payloads
