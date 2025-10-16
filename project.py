


# Talia Cooper and Casey Sara
# Talia UMID: 8968 5759
# Casey UMID: 0806 3805
# tcooperr@umich.edu
# chsara@umich.edu
# collaborators: Talia Cooper, Casey Sara, and ChatGPT. Used ChatGPT for help with csv files, understanding erros, and help with the calculations. 
# Talia created functions that calculated the average sales in the South (by category)
# and the average sales for each state (by category).
# Casey created functions that calculated percent of sales in California that were Furniture (in South)
# and percent of sales that are Office Supplies (by region).
import csv
from typing import List, Dict, Any


# load / explore Data

def load_data(filename: str) -> List[Dict[str, Any]]:
    
    data: List[Dict[str, Any]] = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def explore_data_brief(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    
    info = {
        "num_rows": len(data),
        "columns": list(data[0].keys()) if data else [],
        "sample_row": data[0] if data else {}
    }
    return info

#calculations


def average_sales_in_south(data: List[Dict[str, Any]]) -> Dict[str, float]:
    #Calculates the average sales in the South for each Category.
    #Uses columns: Region, Category, Sales
    
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
    #Calculates average sales for each Category within each State.
    #Uses columns: State, Category, Sales
    
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
    
    #Calculates the % of California sales that are Furniture in the South region.
    #Uses columns: State, Region, Category, Sales
    
    total_ca_south_sales = 0.0
    furniture_sales = 0.0

    for row in data:
        if row.get("State") == "California" and row.get("Region") == "South":
            try:
                s = float(row.get("Sales", "0") or "0")
            except ValueError:
                continue
            total_ca_south_sales += s
            if row.get("Category") == "Furniture":
                furniture_sales += s

    if total_ca_south_sales == 0:
        return 0.0
    return (furniture_sales / total_ca_south_sales) * 100.0


def percent_sales_office_supplies(data: List[Dict[str, Any]]) -> Dict[str, float]:
    
    #Calculates % of Office Supplies sales within each Region.
    #Uses columns: Region, Category, Sales
    
    region_totals = {}
    region_office = {}

    for row in data:
        region = row.get("Region")
        try:
            s = float(row.get("Sales", "0") or "0")
        except ValueError:
            continue

        region_totals[region] = region_totals.get(region, 0.0) + s
        if row.get("Category") == "Office Supplies":
            region_office[region] = region_office.get(region, 0.0) + s

    pct_by_region = {}
    for region in region_totals:
        total = region_totals[region]
        office = region_office.get(region, 0.0)
        pct_by_region[region] = (office / total) * 100 if total > 0 else 0.0

    return pct_by_region


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
        # Edge case
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
        # Edge case
        self.assertEqual(average_sales_by_state([{"State": "TX", "Category": "Furniture", "Sales": "oops"}]), {})

    def test_percent_sales_in_california_furniture(self):
        data = [
            {"State": "California", "Region": "South", "Category": "Furniture", "Sales": "100"},
            {"State": "California", "Region": "South", "Category": "Technology", "Sales": "100"},
            {"State": "Texas", "Region": "South", "Category": "Furniture", "Sales": "200"}
        ]
        result = percent_sales_in_california_furniture(data)
        self.assertAlmostEqual(result, 50.0)
        # Edge cases
        self.assertEqual(percent_sales_in_california_furniture([]), 0.0)
        self.assertEqual(percent_sales_in_california_furniture([{"State": "California", "Region": "South", "Sales": "oops"}]), 0.0)

    def test_percent_sales_office_supplies(self):
        data = [
            {"Region": "South", "Category": "Office Supplies", "Sales": "50"},
            {"Region": "South", "Category": "Furniture", "Sales": "50"},
            {"Region": "West", "Category": "Office Supplies", "Sales": "200"},
            {"Region": "West", "Category": "Technology", "Sales": "100"},
        ]
        result = percent_sales_office_supplies(data)
        self.assertAlmostEqual(result["South"], 50.0)
        self.assertAlmostEqual(result["West"], (200 / 300) * 100)
        # Edge case
        self.assertEqual(percent_sales_office_supplies([]), {})

# write into txt file
def write_results_to_txt(
    filename: str,
    avg_south: Dict[str, float],
    pct_ca_furn: float,
    pct_office: Dict[str, float],
    avg_by_state: Dict[str, Dict[str, float]]
) -> None:
    """Writes all results neatly to a .txt file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("--- Real Data Results ---\n\n")

        f.write("Average Sales in the South by Category:\n")
        for category, avg in avg_south.items():
            f.write(f"{category}: ${avg:.2f}\n")
        f.write("\n")

        f.write(f"% of California Sales that are Furniture (in South): {pct_ca_furn:.2f}%\n\n")

        f.write("Percent of Office Supplies Sales by Region:\n")
        for region, pct in pct_office.items():
            f.write(f"{region}: {pct:.2f}%\n")
        f.write("\n")

        f.write("Average Sales by State and Category:\n")
        for state, cat_dict in avg_by_state.items():
            f.write(f"{state}:\n")
            for cat, avg in cat_dict.items():
                f.write(f"  {cat}: ${avg:.2f}\n")
            f.write("\n")

    print(f"\nResults successfully written to '{filename}'")


# check real data 

def run_data_and_write_output(csv_filename: str) -> None:
    data = load_data(csv_filename)

    avg_south = average_sales_in_south(data)
    pct_ca_furn = percent_sales_in_california_furniture(data)
    avg_by_state = average_sales_by_state(data)
    pct_office = percent_sales_office_supplies(data)

    print("\n--- Real Data Results ---")

    print("\nAverage Sales in the South by Category:")
    for category, avg in avg_south.items():
        print(f"  {category}: ${avg:.2f}")

    print(f"\n% of California Sales that are Furniture (in South): {pct_ca_furn:.2f}%")

    print("\nPercent of Office Supplies Sales by Region:")
    for region, pct in pct_office.items():
        print(f"  {region}: {pct:.2f}%")

    print("\nAverage Sales by State and Category:")
    for state, cat_dict in avg_by_state.items():
        print(f"{state}:")
        for cat, avg in cat_dict.items():
            print(f"  {cat}: ${avg:.2f}")

    write_results_to_txt("results.txt", avg_south, pct_ca_furn, pct_office, avg_by_state)

if __name__ == "__main__":
    #unittest.main()

    csvFile = "SampleSuperstore.csv"
    run_data_and_write_output(csvFile)