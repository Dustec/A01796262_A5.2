"""Unit tests for computeSales.py."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from computeSales import (
    build_catalog,
    compute_sales_total,
    parse_sales_records,
)

BASE_DIR = Path(__file__).resolve().parents[1]
TEST_DATA_DIR = BASE_DIR / "test_data"


class ComputeSalesTests(unittest.TestCase):
    """Validate totals using provided assignment test cases."""

    def setUp(self) -> None:
        """Load shared product catalog used by all provided test cases."""
        catalog_path = TEST_DATA_DIR / "TC1" / "TC1.ProductList.json"
        with catalog_path.open("r", encoding="utf-8") as file_obj:
            products_data = json.load(file_obj)
        self.catalog, catalog_errors = build_catalog(products_data)
        self.assertEqual(catalog_errors, [])

    def assert_total_for_case(
        self,
        sales_file_name: str,
        expected_total: float,
        expected_error_count: int,
    ) -> None:
        """Compute and validate total and number of recoverable data errors."""
        sales_path = TEST_DATA_DIR / sales_file_name
        with sales_path.open("r", encoding="utf-8") as file_obj:
            sales_data = json.load(file_obj)

        sales_records, parse_errors = parse_sales_records(sales_data)
        total, computation_errors = compute_sales_total(
            self.catalog,
            sales_records,
        )

        self.assertEqual(parse_errors, [])
        self.assertAlmostEqual(total, expected_total, places=2)
        self.assertEqual(len(computation_errors), expected_error_count)

    def test_tc1_total(self) -> None:
        """TC1 should match expected total and contain no data errors."""
        self.assert_total_for_case("TC1/TC1.Sales.json", 2481.86, 0)

    def test_tc2_total(self) -> None:
        """TC2 should match expected total and contain no data errors."""
        self.assert_total_for_case("TC2/TC2.Sales.json", 166568.23, 0)

    def test_tc3_total(self) -> None:
        """TC3 should match expected total and contain two unknown products."""
        self.assert_total_for_case("TC3/TC3.Sales.json", 165235.37, 2)


if __name__ == "__main__":
    unittest.main()
