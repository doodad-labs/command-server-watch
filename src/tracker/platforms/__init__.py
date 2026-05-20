from .shodan import shodan
from .censys import censys

# Maps source name (as defined in sources.json) to its extractor function.
# Each extractor must accept a raw response body (str) and return a list of payloads.
# To add a new source: import its extract function and add it here.
REGISTRY: dict[str, callable] = {
    "shodan": shodan,
    "censys": censys,
}
