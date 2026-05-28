from datetime import datetime
from dotenv import load_dotenv
import requests
import os
 
load_dotenv()

_HEADERS = {
    "Accept": "application/json",
    "Auth-Key": os.getenv("ABUSE_CH_KEY", ""),
}

def extract(url: str, query: dict) -> list[dict]:
    
    payloads = []
    more = True

    if not query.get("limit") or not query.get("query"):
        print("Invalid query: missing 'limit' or 'query' fields")
        return []
    
    print(f"Fetching from {url} with query: {query}")
    response = requests.post(url, json=query, headers=_HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch from {url} (HTTP {response.status_code})")
        return payloads

    json_response = response.json()

    if not json_response.get("query_status") == "ok":
        print(f"API error from {url}: {json_response.get('error', 'Unknown error')}")
        return payloads

    if not json_response.get("data"):
        print(f"No more data from {url}")
        return payloads

    for entry in json_response["data"]:

        if entry.get("ioc_type") != "ip:port":
            continue

        [ ip, port ] = entry.get("ioc", "").split(":")
        flag = entry.get("malware_printable", "unknown").lower()
        firstSeen = datetime.strptime(entry.get("first_seen", ""), "%Y-%m-%d %H:%M:%S %Z")

        payloads.append({
            "ip": ip,
            "flags": [flag],
            "results": [{
                "source": "threatfox",
                # Record when this aggregator ingested the entry, not the scan time
                "datetime": datetime.now().isoformat(),
                "flags": [flag],
                "metadata": {
                    "firstSeen": firstSeen.isoformat(),
                    "port": port,
                    "reference": entry.get("reference", ""),
                    "malware_malpedia": entry.get("malware_malpedia", ""),
                    "id": entry.get("id", ""),
                    "ioc": entry.get("ioc", ""),
                    "threat_type": entry.get("threat_type", ""),
                },
            }],
        })

    return payloads