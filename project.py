


# Talia Cooper and Casey Sara
# Talia UMID: 8968 5759
# Casey UMID: 0806 3805
# tcooperr@umich.edu
# chsara@umich.edu
# collaborators: Talia Cooper, Casey Sara, and ChatGPT. Used ChatGPT for hints about csv files and writing our functions. 
# Talia created functions that calculated the average sales in the south and the average sales for each state.
# Casey created functions that calculated percentage of sales in California that were furniture and percentage of sales that are office supplies


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

def percent_sales_in_california_furniture(data: List[Dict[str, Any]]) -> float:

   total_ca_sales = 0.0
   furniture_sales = 0.0


   for row in data:
       if row.get("State") == "California":
           try:
               s = float(row.get("Sales", "0") or "0")
           except ValueError:
               continue
           total_ca_sales += s
           if row.get("Category") == "Furniture":
               furniture_sales += s


   if total_ca_sales == 0:
       return 0.0
   return (furniture_sales / total_ca_sales) * 100.0

def percent_sales_office_supplies(data: List[Dict[str, Any]]) -> float:
   total_sales = 0.0
   office_sales = 0.0


   for row in data:
       try:
           s = float(row.get("Sales", "0") or "0")
       except ValueError:
           continue
       total_sales += s
       if row.get("Category") == "Office Supplies":
           office_sales += s


   if total_sales == 0:
       return 0.0
   return (office_sales / total_sales) * 100.0

#test cases
import unittest


class TestCalculations(unittest.TestCase):
    def test_average_sales_in_south(self):
        data = [
            {"Region": "South", "Sales": "100"},
            {"Region": "South", "Sales": "300"},
            {"Region": "West", "Sales": "500"}
        ]
        # Normal cases
        self.assertEqual(average_sales_in_south(data), 200.0)
        self.assertEqual(average_sales_in_south([{"Region": "South", "Sales": "50"}]), 50.0)
        # Edge cases
        self.assertEqual(average_sales_in_south([]), 0.0)
        self.assertEqual(average_sales_in_south([{"Region": "South", "Sales": "not_a_number"}]), 0.0)

    def test_average_sales_by_state(self):
       data = [
           {"State": "California", "Sales": "100"},
           {"State": "California", "Sales": "200"},
           {"State": "Texas", "Sales": "300"}
       ]
       # Normal cases
       result = average_sales_by_state(data)
       self.assertEqual(result["California"], 150.0)
       self.assertEqual(result["Texas"], 300.0)
       # Edge cases
       self.assertEqual(average_sales_by_state([]), {})
       self.assertEqual(average_sales_by_state([{"State": "California", "Sales": "oops"}]), {})

    def test_percent_sales_in_california_furniture(self):
       data = [
           {"State": "California", "Category": "Furniture", "Sales": "50"},
           {"State": "California", "Category": "Office Supplies", "Sales": "50"},
           {"State": "Texas", "Category": "Furniture", "Sales": "100"}
       ]
       # Normal cases
       self.assertEqual(percent_sales_in_california_furniture(data), 50.0)
       data2 = [
           {"State": "California", "Category": "Furniture", "Sales": "25"},
           {"State": "California", "Category": "Furniture", "Sales": "75"}
       ]
       self.assertEqual(round(percent_sales_in_california_furniture(data2)), 100)
       # Edge cases
       self.assertEqual(percent_sales_in_california_furniture([]), 0.0)
       self.assertEqual(percent_sales_in_california_furniture([{"State": "California", "Sales": "oops"}]), 0.0)

    def test_percent_sales_office_supplies(self):
       data = [
           {"Category": "Office Supplies", "Sales": "100"},
           {"Category": "Furniture", "Sales": "100"},
           {"Category": "Technology", "Sales": "100"}
       ]
       # Normal cases
       self.assertAlmostEqual(percent_sales_office_supplies(data), (100 / 300) * 100)
       self.assertEqual(percent_sales_office_supplies([{"Category": "Office Supplies", "Sales": "50"}]), 100.0)
       # Edge cases
       self.assertEqual(percent_sales_office_supplies([]), 0.0)
       self.assertEqual(percent_sales_office_supplies([{"Category": "Office Supplies", "Sales": "oops"}]), 0.0)




if __name__ == "__main__":
    unittest.main()