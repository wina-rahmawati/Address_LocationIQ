import os
import re
from dotenv import load_dotenv
from src.integrations.geocode_util import get_structured_address



DIRPATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
load_dotenv()
path = os.path.join(DIRPATH, "abbreviation.txt")
# path = "abbreviation.txt"

class _AddressTransformer:

    def __init__(self):
        self.abbreviation_map = self._load_abbreviation()
        self.pattern = self._build_pattern()

    def _load_abbreviation(self):
        mapping = {}
        # path = os.path.join(DIRPATH, ABBREVIATION_FILE)

        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split(";")
                mapping[key.strip()] = value.strip()

        return mapping

    def _build_pattern(self):
        return re.compile(
            r"\b(" + "|".join(map(re.escape, self.abbreviation_map.keys())) + r")\b"
        )

    def _clean(self, text: str):
        text = re.sub(r'[^a-z0-9\s]', '', text.lower())
        return " ".join(text.split())

    def enrich(self, record: dict):

        raw_address = record.get("project_address")

        if not raw_address or not isinstance(raw_address, str):
            return record

        cleaned = self._clean(raw_address)
        cleaned = self.pattern.sub(
            lambda m: self.abbreviation_map[m.group()],
            cleaned
        )

        geo_data = get_structured_address(cleaned)

        if geo_data:
            record["latitude"] = geo_data.get("latitude")
            record["longitude"] = geo_data.get("longitude")
            record["full_address"] = geo_data.get("full_address")

        return record


# REQUIRED FUNCTION
def transform(address_iter):
    """
    Transforms an iterator of address dictionaries by enriching each address.
    Yields enriched addresses one by one.
    """
    transformer = _AddressTransformer()

    for record in address_iter:
        enriched = transformer.enrich(record)
        if enriched:  # skip None
            yield enriched