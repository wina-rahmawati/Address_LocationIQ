import os
import json


class _JsonReader:

    def __init__(self, path: str):
        self.path = path

    def read(self):

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Folder not found: {self.path}")

        files = [f for f in os.listdir(self.path) if f.endswith(".json")]

        if not files:
            raise FileNotFoundError("No JSON files found")

        for filename in files:
            file_path = os.path.join(self.path, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            if isinstance(data, list):
                for record in data:
                    yield record
            elif isinstance(data, dict):
                yield data


# REQUIRED FUNCTION
def read_json(path):
    """
    Reads JSON files from a specified directory and yields each record.
    """
    reader = _JsonReader(path)
    return reader.read()