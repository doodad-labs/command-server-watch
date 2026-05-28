from .criminalip import extract as criminalip_extract
from .feodotracker import extract as feodotracker_extract
from .viribacktracker import extract as viribacktracker_extract
from .threatfox import extract as threatfox_extract

# Maps source name (as defined in sources.json) to its extractor function.
# Each extractor must accept a raw response body (str) and return a list of payloads.
# To add a new source: import its extract function and add it here.
REGISTRY: dict[str, callable] = {
    "criminalip": criminalip_extract,
    "feodotracker": feodotracker_extract,
    "viribacktracker": viribacktracker_extract,
    "threatfox": threatfox_extract,
}
