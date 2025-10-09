


#Talia Cooper 
#
# tcooperr@umich.edu
# collaborators: Casey Sara and ChatGPT. Used ChatGPT for hints about csv files and writing our functions. 
# Talia created functions.... 


import csv
from typing import List, Dict, Any


# Part 2: Load / Explore Data

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

## part 7 - calculations

def average_sales_in_south(data: List[Dict[str, Any]]) -> float:
   """
   Calculation 1:
   Average of 'Sales' for rows where Region == 'South'.
   Uses columns: Region, Sales
   """
   total_sales = 0.0
   count = 0
   for row in data:
       if row.get("Region") == "South":
           try:
               total_sales += float(row.get("Sales", "0") or "0")
               count += 1
           except ValueError:
               # Skip rows with non-numeric Sales
               continue
   return (total_sales / count) if count > 0 else 0.0

def average_sales_by_state(data: List[Dict[str, Any]]) -> Dict[str, float]:
   """
   Calculation 3:
   Returns a dict: {state: average_sales}.
   Uses columns: State, Sales
   """
   by_state: Dict[str, List[float]] = {}
   for row in data:
       state = row.get("State")
       if not state:
           continue
       try:
           s = float(row.get("Sales", "0") or "0")
       except ValueError:
           continue
       by_state.setdefault(state, []).append(s)


   avg_by_state: Dict[str, float] = {}
   for state, sales_list in by_state.items():
       if sales_list:
           avg_by_state[state] = sum(sales_list) / len(sales_list)
   return avg_by_state

