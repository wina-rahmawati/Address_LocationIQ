import pytest
import json
import os
import sys
from typing import Iterator, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def read_json_folder(folder_path: str) -> Iterator[Dict]:
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")

    files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    if not files:
        raise FileNotFoundError("No JSON files found in the folder")

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue 

        if isinstance(data, list):
            for record in data:
                if record: yield record
        elif isinstance(data, dict):
            if data: yield data

def test_read_json_folder_success(tmp_path):
    # 1. Create a dummy folder and file
    d = tmp_path / "data"
    d.mkdir()
    f = d / "test.json"
    
    # Write some dummy data
    f.write_text(json.dumps([{"id": 1, "address": "Sydney"}]))

    # 2. Run your function
    results = list(read_json_folder(str(d)))
    
    # 3. Check if it worked
    assert len(results) == 1
    assert results[0]["id"] == 1