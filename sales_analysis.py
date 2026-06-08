"""
CSV Sales Analysis
------------------
A simple Python project for analyzing sales data from a CSV file.

Features:
- Read sales records from a CSV file
- Calculate total revenue
- Find the best-selling product
- Summarize revenue by product
- Summarize revenue by month
- Export a summary report to a text file
- Create a revenue chart using Matplotlib

Required library:
- matplotlib
"""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


DATA_FILE = Path("sales_data.csv")
REPORT_FILE = Path("sales_report.txt")
CHART_FILE = Path("revenue_by_product.png")


class SalesAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.records = []

    def load_data(self):
        if not self.file_path.exists():
            print(f"Data file not found: {self.file_path}")
            return False

        try:
            with self.file_path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    record = {
                        "date": row["date"],
                        "product": row["product"],
                        "quantity": int(row["quantity"]),
                        "unit_price": float(row["unit_price"]),
                    }
                    self.records.append(record)

            return True

        except (KeyError, ValueError) as error:
            print(f"Error while reading CSV file: {error}")
            return False

    def total_revenue(self):
        return sum(item["quantity"] * item["unit_price"] for item in self.records)

    def revenue_by_product(self):
        summary = defaultdict(float)

        for item in self.records:
            revenue = item["quantity"] * item["unit_price"]
            summary[item["product"]] += revenue

        return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

    def revenue_by_month(self):
        summary = defaultdict(float)

        for item in self.records:
            month = item["date"][:7]
            revenue = item["quantity"] * item["unit_price"]
            summary[month] += revenue

        return dict(sorted(summary.items()))

    def best_selling_product(self):
        quantity_summary = defaultdict(int)

        for item in self.records:
            quantity_summary[item["product"]] += item["quantity"]

        if not quantity_summary:
            return None

        return max(quantity_summary.items(), key=lambda x: x[1])

    def create_chart(self):
        product_revenue = self.revenue_by_product()

        if not product_revenue:
            print("No data available for chart.")
            return

        products = list(product_revenue.keys())
        revenues = list(product_revenue.values())

        plt.figure(figsize=(9, 5))
        plt.bar(products, revenues)
        plt.title("Revenue by Product")
        plt.xlabel("Product")
        plt.ylabel("Revenue")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(CHART_FILE)
        plt.close()

        print(f"Chart saved to {CHART_FILE}")

    def export_report(self):
        product_revenue = self.revenue_by_product()
        monthly_revenue = self.revenue_by_month()
        best_product = self.best_selling_product()

        with REPORT_FILE.open("w", encoding="utf-8") as file:
            file.write("Sales Analysis Report\n")
            file.write("=====================\n\n")

            file.write(f"Total revenue: {self.total_revenue():.2f}\n\n")

            if best_product:
                file.write(f"Best-selling product: {best_product[0]} ({best_product[1]} units)\n\n")

            file.write("Revenue by Product:\n")
            for product, revenue in product_revenue.items():
                file.write(f"- {product}: {revenue:.2f}\n")

            file.write("\nRevenue by Month:\n")
            for month, revenue in monthly_revenue.items():
                file.write(f"- {month}: {revenue:.2f}\n")

        print(f"Report saved to {REPORT_FILE}")

    def print_summary(self):
        print("\n===== Sales Analysis Summary =====")
        print(f"Total revenue: {self.total_revenue():.2f}")

        best_product = self.best_selling_product()
        if best_product:
            print(f"Best-selling product: {best_product[0]} ({best_product[1]} units)")

        print("\nRevenue by Product:")
        for product, revenue in self.revenue_by_product().items():
            print(f"- {product}: {revenue:.2f}")

        print("\nRevenue by Month:")
        for month, revenue in self.revenue_by_month().items():
            print(f"- {month}: {revenue:.2f}")


def main():
    analyzer = SalesAnalyzer(DATA_FILE)

    if not analyzer.load_data():
        return

    analyzer.print_summary()
    analyzer.export_report()
    analyzer.create_chart()


if __name__ == "__main__":
    main()
