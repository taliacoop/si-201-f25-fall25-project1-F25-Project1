import csv
from typing import List, Dict, Any


# -----------------------------
# Part 2: Load / Explore Data
# -----------------------------

def load_data(filename: str) -> List[Dict[str, Any]]:
    """
    Reads a CSV into a list of row dictionaries using csv.DictReader.
    Returns: list[dict] where keys are column names and values are strings from the CSV.
    """
    data: List[Dict[str, Any]] = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def explore_data_brief(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Returns quick metadata: number of rows, column names, and a sample row.
    (Helpful during dev; not required for final output.)
    """
    info = {
        "num_rows": len(data),
        "columns": list(data[0].keys()) if data else [],
        "sample_row": data[0] if data else {}
    }
    return info

