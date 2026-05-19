from ipaddress import ip_address

def result_key(r: dict) -> tuple:
    """Return a hashable key used to deduplicate result entries.

    Two results are considered duplicates when they share the same source
    and the same set of flags (order-independent).
    """
    return (r["source"], frozenset(r["flags"]))


def valid_ip(ip: str) -> bool:
    """Return True if ip is a valid IPv4 or IPv6 address, False otherwise."""
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False
