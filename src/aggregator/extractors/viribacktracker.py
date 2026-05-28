import csv
from datetime import datetime

def extract(body: str) -> list[dict]:
    
    payloads = []

    content = body.splitlines()[1:]  # Skip the header row
    reader = csv.reader(content)

    for object in reader:

        firstSeen = datetime.strptime(object[3], "%d-%m-%Y")

        payloads.append({
            "ip": object[2],
            "flags": [object[0].lower()],
            "results": [{
                "source": "viribacktracker",
                # Record when this aggregator ingested the entry, not the scan time
                "datetime": datetime.now().isoformat(),
                "flags": [object[0].lower()],
                "metadata": {
                    "firstSeen": firstSeen.isoformat(),
                    "login": object[1],
                },
            }],
        })

    return payloads
