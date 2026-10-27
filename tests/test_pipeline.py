from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from sales_intelligence.pipeline import run_analysis


class PipelineTests(unittest.TestCase):
    def test_pipeline_creates_all_expected_artifacts(self) -> None:
        transactions = pd.DataFrame(
            [
                {
                    "InvoiceNo": "1",
                    "StockCode": "ITEM",
                    "Description": "Synthetic item",
                    "Quantity": 2,
                    "InvoiceDate": "2011-01-03",
                    "UnitPrice": 5.0,
                    "CustomerID": 10,
                    "Country": "Test country",
                }
            ]
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "input.xlsx"
            output_dir = root / "outputs"
            with pd.ExcelWriter(input_path) as writer:
                transactions.to_excel(writer, sheet_name="Online Retail", index=False)

            result = run_analysis(input_path, output_dir)

            self.assertEqual(result.total_rows, 1)
            self.assertEqual(result.net_revenue, 10.0)
            for filename in (
                "monthly_metrics.csv",
                "customer_segments.csv",
                "data_quality.csv",
                "monthly_revenue.png",
                "report.md",
            ):
                self.assertTrue((output_dir / filename).is_file(), filename)

    def test_missing_input_has_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing.xlsx"

            with self.assertRaisesRegex(FileNotFoundError, "README.md"):
                run_analysis(missing, Path(temp_dir) / "outputs")
