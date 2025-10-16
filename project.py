


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


def average_sales_in_south(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculates the average sales in the South for each Category.
    Uses columns: Region, Category, Sales
    """
    category_sales = {}
    for row in data:
        if row.get("Region") == "South":
            category = row.get("Category")
            try:
                s = float(row.get("Sales", "0") or "0")
            except ValueError:
                continue
            category_sales.setdefault(category, []).append(s)

    avg_by_category = {cat: sum(vals)/len(vals) for cat, vals in category_sales.items() if vals}
    return avg_by_category

def average_sales_by_state(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Calculates average sales for each Category within each State.
    Uses columns: State, Category, Sales
    """
    state_cat_sales = {}
    for row in data:
        state = row.get("State")
        category = row.get("Category")
        try:
            s = float(row.get("Sales", "0") or "0")
        except ValueError:
            continue
        state_cat_sales.setdefault(state, {}).setdefault(category, []).append(s)

    avg_by_state_cat = {
        state: {cat: sum(vals)/len(vals) for cat, vals in cat_dict.items() if vals}
        for state, cat_dict in state_cat_sales.items()
    }
    return avg_by_state_cat

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
            {"Region": "South", "Category": "Furniture", "Sales": "100"},
            {"Region": "South", "Category": "Technology", "Sales": "200"},
            {"Region": "West", "Category": "Furniture", "Sales": "300"}
        ]
        result = average_sales_in_south(data)
        self.assertAlmostEqual(result["Furniture"], 100.0)
        self.assertAlmostEqual(result["Technology"], 200.0)
        # Edge case: empty data
        self.assertEqual(average_sales_in_south([]), {})


    def test_average_sales_by_state(self):
        data = [
            {"State": "Texas", "Category": "Furniture", "Sales": "100"},
            {"State": "Texas", "Category": "Furniture", "Sales": "200"},
            {"State": "California", "Category": "Technology", "Sales": "300"}
        ]
        result = average_sales_by_state(data)
        self.assertAlmostEqual(result["Texas"]["Furniture"], 150.0)
        self.assertAlmostEqual(result["California"]["Technology"], 300.0)
        # Edge case: invalid numeric
        self.assertEqual(average_sales_by_state([{"State": "TX", "Category": "Furniture", "Sales": "oops"}]), {})

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

# write into txt file
def write_results_to_txt(
    filename: str,
    avg_south: float,
    pct_ca_furn: float,
    pct_office: float,
    avg_by_state: Dict[str, float]
) -> None:
   
    with open(filename, "w", encoding="utf-8") as f:
        f.write("--- Real Data Results ---\n")
        f.write(f"Average Sales in South: ${avg_south:.2f}\n")
        f.write(f"% of California Sales that are Furniture: {pct_ca_furn:.2f}%\n")
        f.write(f"% of All Sales that are Office Supplies: {pct_office:.2f}%\n\n")

        f.write("Average Sales by State:\n")
        for state, avg in avg_by_state.items():
            f.write(f"{state}: ${avg:.2f}\n")

    print(f"\n Results successfully written to '{filename}'")


# check real data 

def run_data_and_write_output(csv_filename: str) -> None:
    data = load_data(csv_filename)
    
    avg_south = average_sales_in_south(data)
    pct_ca_furn = percent_sales_in_california_furniture(data)
    avg_by_state = average_sales_by_state(data)
    pct_office = percent_sales_office_supplies(data)

    print("\n--- Real Data Results ---")
    print(f"Average Sales in the South: {avg_south:.2f}")
    print(f"% of California Sales that are Furniture: {pct_ca_furn:.2f}%")
    print(f"% of All Sales that are Office Supplies: {pct_office:.2f}%")
    
    print("\nAverage Sales by State:")
    for state, avg in avg_by_state.items():
        print(f"{state}: ${avg:.2f}")
    write_results_to_txt("results.txt", avg_south, pct_ca_furn, pct_office, avg_by_state)

if __name__ == "__main__":
    unittest.main()

    csvFile = "SampleSuperstore.csv"
    run_data_and_write_output(csvFile)