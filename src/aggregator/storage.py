import json
import os
from ipaddress import ip_address
from .utils import valid_ip, result_key

OUTPUT_DIR = "../out/data"

def save_payload(payload: dict) -> None:
    """Persist a payload to disk, merging with any existing data for that IP.

    Payloads are stored under data/ipv4/ or data/ipv6/ in a directory tree
    that mirrors the IP address structure, e.g.:
        data/ipv4/192/168/1/1.json
        data/ipv6/2001/0db8/85a3/0000/0000/8a2e/0370/7334.json

    If a file for the IP already exists, flags and results are merged and
    deduplicated rather than overwritten.
    """
    if not _validate_payload(payload):
        return

    file_path = _ip_to_path(payload["ip"])

    # Ensure all parent directories exist before writing
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing = json.load(f)

        _merge_into(existing, payload)

        with open(file_path, "w") as f:
            json.dump(existing, f, indent=4)
    else:
        # First time seeing this IP — write directly
        with open(file_path, "w") as f:
            json.dump(payload, f, indent=4)


def _validate_payload(payload: dict) -> bool:
    """Return True if payload has the required fields with the correct types."""
    return (
        isinstance(payload.get("ip"), str)
        and isinstance(payload.get("results"), list)
        and isinstance(payload.get("flags"), list)
        and valid_ip(payload["ip"])
    )


def _ip_to_path(ip: str) -> str:
    """Convert an IP address string to its corresponding file path.

    IPv4 octets and IPv6 groups each become a directory level, with the
    final segment used as the filename.
    """
    addr = ip_address(ip)

    # IPv6: use the fully-expanded form so every group is present
    parts = str(addr).split(".") if addr.version == 4 else addr.exploded.split(":")

    return OUTPUT_DIR + "/ipv{}/".format(addr.version) + "/".join(parts[:-1]) + "/{}.json".format(parts[-1])


def _merge_into(existing: dict, new: dict) -> None:
    """Merge new payload data into existing in-place.

    Flags are unioned and sorted. Results are deduplicated by (source, flags)
    key, keeping the first occurrence when duplicates are found.
    """
    # Union the flag sets and re-sort for stable output
    existing["flags"] = sorted(set(existing["flags"]) | set(new["flags"]))

    # Build a dict keyed by result identity so duplicates are dropped
    seen = {}
    for r in existing["results"] + new["results"]:
        seen.setdefault(result_key(r), r)

    existing["results"] = list(seen.values())
