import json
from datetime import datetime
import requests
from .extractors import REGISTRY
from .storage import save_payload

# Path to the sources config, relative to wherever the process is run from
SOURCES_FILE = "../sources.json"

def _build_url(source: dict) -> str:
    """Resolve the full URL for today's feed file from a source definition.

    The file_format field supports YYYY, MM, and DD tokens which are replaced
    with today's date values, e.g. "YYYY-MM-DD.csv" → "2026-05-19.csv".
    """
    today = datetime.now()

    # Convert the custom token format to a strftime-ready format string
    filename = (
        source["file_format"]
        .replace("YYYY", today.strftime("%Y"))
        .replace("MM", today.strftime("%m"))
        .replace("DD", today.strftime("%d"))
    )

    return source["url_raw"] + filename


def _process_git_source(source: dict) -> None:
    """Fetch and ingest a single git-hosted feed source.

    Looks up the registered extractor for the source by name, parses the
    response body into payloads, and persists each one via save_payload.
    """
    url = _build_url(source)
    response = requests.get(url)

    # Bail early if the feed is unreachable or returned an error
    if response.status_code != 200:
        print(f"Failed to fetch {source['name']} from {url} (HTTP {response.status_code})")
        return

    extractor = REGISTRY.get(source["name"])

    # Warn and skip if no extractor has been registered for this source name
    if extractor is None:
        print(f"No extractor registered for source: {source['name']}")
        return

    for payload in extractor(response.text):
        save_payload(payload)

def _process_json_source(source: dict) -> None:
    """Fetch and ingest a single JSON feed source.

    Looks up the registered extractor for the source by name, parses the
    response body into payloads, and persists each one via save_payload.
    """
    url = source["url"]
    response = requests.get(url)

    # Bail early if the feed is unreachable or returned an error
    if response.status_code != 200:
        print(f"Failed to fetch {source['name']} from {url} (HTTP {response.status_code})")
        return

    extractor = REGISTRY.get(source["name"])

    # Warn and skip if no extractor has been registered for this source name
    if extractor is None:
        print(f"No extractor registered for source: {source['name']}")
        return

    for payload in extractor(response.text):
        save_payload(payload)

def _process_csv_source(source: dict) -> None:

    url = source["url"]
    response = requests.get(url)

    # Bail early if the feed is unreachable or returned an error
    if response.status_code != 200:
        print(f"Failed to fetch {source['name']} from {url} (HTTP {response.status_code})")
        return

    extractor = REGISTRY.get(source["name"])

    # Warn and skip if no extractor has been registered for this source name
    if extractor is None:
        print(f"No extractor registered for source: {source['name']}")
        return

    for payload in extractor(response.text):
        save_payload(payload)


def main() -> None:
    """Entry point: load sources config and process each configured feed."""
    with open(SOURCES_FILE) as f:
        sources = json.load(f)

    # Only git-hosted sources are supported for now
    for source in sources.get("aggregator", {}).get("git", []):
        _process_git_source(source)

    for source in sources.get("aggregator", {}).get("json", []):
        _process_json_source(source)

    for source in sources.get("aggregator", {}).get("csv", []):
        _process_csv_source(source)


if __name__ == "__main__":
    main()
