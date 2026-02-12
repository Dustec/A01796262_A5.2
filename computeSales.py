"""Compute the total sales amount from catalog and sales record JSON files."""

# pylint: disable=invalid-name

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

OUTPUT_FILE_NAME = "SalesResults.txt"


def parse_cli_arguments() -> argparse.Namespace:
    """Parse command line arguments required by the program."""
    parser = argparse.ArgumentParser(
        description=(
            "Compute total sales from a price catalog JSON and a sales "
            "record JSON."
        )
    )
    parser.add_argument("price_catalogue", help="Path to price catalog JSON")
    parser.add_argument("sales_record", help="Path to sales record JSON")
    return parser.parse_args()


def read_json_file(file_path: Path) -> Any:
    """Read and decode a JSON file.

    Raises:
        ValueError: If the file does not exist or cannot be parsed.
    """
    try:
        with file_path.open("r", encoding="utf-8") as source:
            return json.load(source)
    except FileNotFoundError as error:
        raise ValueError(f"File not found: {file_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON format in file: {file_path} (line {error.lineno})"
        ) from error


def is_number(value: Any) -> bool:
    """Return True when value is numeric and finite."""
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def build_catalog(products_data: Any) -> tuple[dict[str, float], list[str]]:
    """Create a title->price map from product JSON data."""
    errors: list[str] = []
    catalog: dict[str, float] = {}

    if not isinstance(products_data, list):
        return catalog, ["Catalog data must be a JSON array."]

    for index, item in enumerate(products_data, start=1):
        if not isinstance(item, dict):
            errors.append(f"Catalog item #{index} is not a JSON object.")
            continue

        title = item.get("title")
        price = item.get("price")

        if not isinstance(title, str) or not title.strip():
            errors.append(
                f"Catalog item #{index} has an invalid 'title' field."
            )
            continue

        if not is_number(price):
            errors.append(
                f"Catalog item #{index} has an invalid 'price' field for "
                f"product '{title}'."
            )
            continue

        catalog[title] = float(price)

    return catalog, errors


def parse_sales_records(
    sales_data: Any,
) -> tuple[list[tuple[str, float]], list[str]]:
    """Extract (product, quantity) tuples from sales JSON data."""
    errors: list[str] = []
    sales_records: list[tuple[str, float]] = []

    if not isinstance(sales_data, list):
        return sales_records, ["Sales record data must be a JSON array."]

    for index, item in enumerate(sales_data, start=1):
        if not isinstance(item, dict):
            errors.append(f"Sales item #{index} is not a JSON object.")
            continue

        product = item.get("Product")
        quantity = item.get("Quantity")

        if not isinstance(product, str) or not product.strip():
            errors.append(
                f"Sales item #{index} has an invalid 'Product' field."
            )
            continue

        if not is_number(quantity):
            errors.append(
                f"Sales item #{index} has an invalid 'Quantity' field for "
                f"product '{product}'."
            )
            continue

        sales_records.append((product, float(quantity)))

    return sales_records, errors


def compute_sales_total(
    catalog: dict[str, float], sales_records: list[tuple[str, float]]
) -> tuple[float, list[str]]:
    """Compute total sales amount and collect recoverable data errors."""
    total = 0.0
    errors: list[str] = []

    for product, quantity in sales_records:
        unit_price = catalog.get(product)
        if unit_price is None:
            errors.append(
                f"Product '{product}' does not exist in the catalog. "
                "Record skipped."
            )
            continue

        total += unit_price * quantity

    return total, errors


def create_report(total: float, elapsed_time: float, errors: list[str]) -> str:
    """Generate a human readable report."""
    lines = [
        "Sales Calculation Report",
        "------------------------",
        f"TOTAL: {total:.2f}",
        f"EXECUTION_TIME_SECONDS: {elapsed_time:.6f}",
        f"ERROR_COUNT: {len(errors)}",
    ]

    if errors:
        lines.append("ERRORS:")
        lines.extend(f"- {message}" for message in errors)
    else:
        lines.append("ERRORS: None")

    return "\n".join(lines)


def write_report(report_text: str, output_path: Path) -> None:
    """Persist report to output file."""
    with output_path.open("w", encoding="utf-8") as destination:
        destination.write(report_text)
        destination.write("\n")


def main() -> int:
    """Run command line workflow."""
    args = parse_cli_arguments()

    start_time = time.perf_counter()

    try:
        products_data = read_json_file(Path(args.price_catalogue))
        sales_data = read_json_file(Path(args.sales_record))
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    catalog, catalog_errors = build_catalog(products_data)
    sales_records, sales_errors = parse_sales_records(sales_data)
    total, computation_errors = compute_sales_total(catalog, sales_records)

    elapsed_time = time.perf_counter() - start_time
    all_errors = catalog_errors + sales_errors + computation_errors

    report = create_report(total, elapsed_time, all_errors)
    print(report)

    write_report(report, Path(OUTPUT_FILE_NAME))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
