from __future__ import annotations

import unittest

import pandas as pd

from sales_intelligence.analysis import (
    classify_customer_purchases,
    customer_segments_monthly,
    monthly_metrics,
    prepare_transactions,
    validate_schema,
)


def row(
    invoice: str,
    quantity: int,
    date: str,
    price: float,
    customer: float | None,
) -> dict[str, object]:
    return {
        "InvoiceNo": invoice,
        "StockCode": "ITEM",
        "Description": "Synthetic item",
        "Quantity": quantity,
        "InvoiceDate": date,
        "UnitPrice": price,
        "CustomerID": customer,
        "Country": "Test country",
    }


class SchemaTests(unittest.TestCase):
    def test_missing_column_has_clear_error(self) -> None:
        data = pd.DataFrame([row("1", 1, "2011-01-01", 2.0, 10)])
        data = data.drop(columns="Country")

        with self.assertRaisesRegex(ValueError, "Country"):
            validate_schema(data)


class MetricTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prepared = prepare_transactions(
            pd.DataFrame(
                [
                    row("C0", -1, "2010-12-20", 5.0, 10),
                    row("1", 2, "2011-01-02", 5.0, 10),
                    row("2", 1, "2011-01-20", 10.0, 10),
                    row("3", 1, "2011-01-20", 7.0, 20),
                    row("4", 3, "2011-02-03", 5.0, 10),
                    row("5", 1, "2011-02-04", 4.0, None),
                    row("6", 1, "2011-02-05", 0.0, 30),
                ]
            )
        )

    def test_return_before_purchase_does_not_define_first_purchase(self) -> None:
        purchases = classify_customer_purchases(self.prepared)
        customer_10 = purchases.loc[purchases["CustomerID"] == 10]

        january_types = set(
            customer_10.loc[customer_10["Month"] == "2011-01", "CustomerType"]
        )
        february_types = set(
            customer_10.loc[customer_10["Month"] == "2011-02", "CustomerType"]
        )
        self.assertEqual(january_types, {"New"})
        self.assertEqual(february_types, {"Returning"})

    def test_multiple_first_month_purchases_count_one_new_customer(self) -> None:
        segments = customer_segments_monthly(self.prepared)
        january_new = segments.loc[
            (segments["Month"] == "2011-01")
            & (segments["CustomerType"] == "New")
        ].iloc[0]

        self.assertEqual(january_new["customers"], 2)
        self.assertEqual(january_new["purchase_revenue"], 27.0)

    def test_monthly_revenue_includes_returns_and_excludes_zero_price(self) -> None:
        monthly = monthly_metrics(self.prepared).set_index("Month")

        self.assertEqual(monthly.loc["2010-12", "net_revenue"], -5.0)
        self.assertEqual(monthly.loc["2011-02", "net_revenue"], 19.0)
        self.assertEqual(monthly.loc["2011-02", "purchasing_customers"], 1)


if __name__ == "__main__":
    unittest.main()
