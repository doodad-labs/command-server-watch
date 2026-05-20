import json
from datetime import datetime

def extract(body: str) -> list[dict]:
    
    payloads = []

    reader = json.loads(body)
    for object in reader:

        payloads.append({
            "ip": object["ip_address"],
            "flags": [object["malware"].lower()],
            "results": [{
                "source": "feodotracker",
                # Record when this aggregator ingested the entry, not the scan time
                "datetime": datetime.now().isoformat(),
                "flags": [object["malware"].lower()],
                "metadata": {
                    "country": object["country"],
                    "firstSeen": object["first_seen"],
                    "lastOnline": object["last_online"],
                    "hostname": object["hostname"],
                    "port": object["port"],
                },
            }],
        })

    return payloads
