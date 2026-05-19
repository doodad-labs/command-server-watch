from .criminalip import extract as criminalip_extract

# Maps source name (as defined in sources.json) to its extractor function.
# Each extractor must accept a raw response body (str) and return a list of payloads.
# To add a new source: import its extract function and add it here.
REGISTRY: dict[str, callable] = {
    "criminalip": criminalip_extract,
}
