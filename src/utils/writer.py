import os
import json
from typing import Iterator, Dict


class _JsonWriter:

    def __init__(self, path: str):
        self.path = path

    # def _ensure_directory(self):
    #     directory = os.path.dirname(self.path)
        # if directory and not os.path.exists(directory):
        #     os.makedirs(directory, exist_ok=True)

    def write(self, data_iter: Iterator[Dict]):

        if data_iter is None:
            raise ValueError("data_iter cannot be None")

        # self._ensure_directory()

        try:
            data_list = list(data_iter)
        except Exception as e:
            return "Failed to consume iterator: {e}"
            # raise RuntimeError(f"Failed to consume iterator: {e}")

        if not isinstance(data_list, list):
            raise TypeError("Data must be iterable of dictionaries")

        try:
            with open(self.path, "w", encoding="utf-8") as f:
                # print('data_list', data_list)
                json.dump(data_list, f, indent=4, ensure_ascii=False)
                # print(data_list)
        except IOError as e:
            raise IOError(f"Failed to write JSON file: {e}")


# REQUIRED FUNCTION
def write_json(data_iter, path):
    """
    Takes an iterator of enriched data and writes to a JSON file.
    """
    writer = _JsonWriter(path)
    writer.write(data_iter)