import json
from pathlib import Path


def load_schema(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_endpoints(schema: dict) -> dict:
    endpoints = {}
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            key = f"{method.upper()} {path}"
            endpoints[key] = details
    return endpoints