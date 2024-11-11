import json


def load_data_from_json(file_path):
    """Load financial data from a JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
