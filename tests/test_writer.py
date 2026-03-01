import json
import os
from typing import Iterator, Dict

def write_to_json(data_iterator: Iterator[Dict], target_path: str) -> None:
    # 1. Create the folder if it doesn't exist (from your code)
    directory = os.path.dirname(target_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # 2. Convert iterator to list (from your code)
    try:
        data_list = list(data_iterator)
    except Exception as e:
        raise RuntimeError(f"Failed to consume data iterator: {e}")

    # 3. Write to JSON
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

def test_write_to_json_success(tmp_path):
    # 1. Arrange
    output_file = tmp_path / "output.json"
    sample_data = [{"id": 1, "status": "enriched"}]
    
    # 2. Act
    write_to_json(iter(sample_data), str(output_file))
    
    # 3. Assert
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        data = json.load(f)
        assert data[0]["id"] == 1