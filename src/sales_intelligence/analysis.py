"""Reglas de datos y metricas puras del proyecto."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


EXPECTED_COLUMNS = (
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
)


def validate_schema(
    transactions: pd.DataFrame,
    expected_columns: Iterable[str] = EXPECTED_COLUMNS,
) -> None:
    """Comprueba columnas y valores indispensables antes del analisis."""
    missing = sorted(set(expected_columns) - set(transactions.columns))
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(missing)}")

    invalid = {}
    for column in ("Quantity", "UnitPrice"):
        converted = pd.to_numeric(transactions[column], errors="coerce")
        invalid[column] = int(converted.isna().sum())

    dates = pd.to_datetime(transactions["InvoiceDate"], errors="coerce")
    invalid["InvoiceDate"] = int(dates.isna().sum())
    invalid = {column: count for column, count in invalid.items() if count}
    if invalid:
        detail = ", ".join(f"{column}={count}" for column, count in invalid.items())
        raise ValueError(f"Valores nulos o invalidos en campos obligatorios: {detail}")


def prepare_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """Valida tipos y agrega campos derivados sin descartar la entrada original."""
    validate_schema(transactions)
    prepared = transactions.copy()
    prepared["Quantity"] = pd.to_numeric(prepared["Quantity"])
    prepared["UnitPrice"] = pd.to_numeric(prepared["UnitPrice"])
    prepared["InvoiceDate"] = pd.to_datetime(prepared["InvoiceDate"])
    prepared["InvoiceNo"] = prepared["InvoiceNo"].astype("string")
    prepared["Revenue"] = prepared["Quantity"] * prepared["UnitPrice"]
    prepared["Month"] = prepared["InvoiceDate"].dt.to_period("M").astype(str)
    prepared["IsCancellation"] = prepared["InvoiceNo"].str.upper().str.startswith("C")
    return prepared


def analyzable_transactions(prepared: pd.DataFrame) -> pd.DataFrame:
    """Aplica la regla vigente: analizar solamente precios estrictamente positivos."""
    return prepared.loc[prepared["UnitPrice"] > 0].copy()


def monthly_metrics(prepared: pd.DataFrame) -> pd.DataFrame:
    """Calcula metricas mensuales con denominadores visibles."""
    analyzed = analyzable_transactions(prepared)
    analyzed["PositiveRevenue"] = analyzed["Revenue"].where(
        analyzed["Quantity"] > 0, 0
    )
    analyzed["ReturnRevenue"] = analyzed["Revenue"].where(
        analyzed["Quantity"] < 0, 0
    )

    monthly = (
        analyzed.groupby("Month", sort=True)
        .agg(
            net_revenue=("Revenue", "sum"),
            positive_revenue=("PositiveRevenue", "sum"),
            return_revenue=("ReturnRevenue", "sum"),
            net_units=("Quantity", "sum"),
            unique_invoices=("InvoiceNo", "nunique"),
            unique_customers=("CustomerID", "nunique"),
        )
        .reset_index()
    )

    positive = analyzed.loc[analyzed["Quantity"] > 0]
    purchasing_customers = (
        positive.groupby("Month")["CustomerID"]
        .nunique()
        .rename("purchasing_customers")
        .reset_index()
    )
    monthly = monthly.merge(purchasing_customers, on="Month", how="left")
    monthly["purchasing_customers"] = (
        monthly["purchasing_customers"].fillna(0).astype(int)
    )
    monthly["net_revenue_per_invoice"] = (
        monthly["net_revenue"] / monthly["unique_invoices"]
    )
    return monthly


def classify_customer_purchases(prepared: pd.DataFrame) -> pd.DataFrame:
    """Etiqueta compras positivas identificadas como New o Returning.

    New significa primera compra positiva observada dentro de la ventana del archivo.
    """
    analyzed = analyzable_transactions(prepared)
    purchases = analyzed.loc[
        (analyzed["Quantity"] > 0) & analyzed["CustomerID"].notna()
    ].copy()

    first_purchase = purchases.groupby("CustomerID")["InvoiceDate"].transform("min")
    purchases["FirstPurchaseMonth"] = first_purchase.dt.to_period("M").astype(str)
    purchases["CustomerType"] = "Returning"
    purchases.loc[
        purchases["Month"] == purchases["FirstPurchaseMonth"], "CustomerType"
    ] = "New"
    return purchases


def customer_segments_monthly(prepared: pd.DataFrame) -> pd.DataFrame:
    """Resume clientes e ingreso positivo por mes y tipo de cliente."""
    purchases = classify_customer_purchases(prepared)
    return (
        purchases.groupby(["Month", "CustomerType"], sort=True)
        .agg(
            customers=("CustomerID", "nunique"),
            purchase_revenue=("Revenue", "sum"),
            invoices=("InvoiceNo", "nunique"),
        )
        .reset_index()
    )


def quality_metrics(prepared: pd.DataFrame) -> pd.DataFrame:
    """Cuantifica exclusiones, cobertura y consistencia de cancelaciones."""
    positive = prepared.loc[(prepared["UnitPrice"] > 0) & (prepared["Quantity"] > 0)]
    identified = positive.loc[positive["CustomerID"].notna()]
    positive_revenue = float(positive["Revenue"].sum())
    identified_revenue = float(identified["Revenue"].sum())
    cancellation_mismatch = prepared["IsCancellation"] != (prepared["Quantity"] < 0)

    rows = [
        ("total_rows", len(prepared), "Filas recibidas"),
        ("duplicate_rows", int(prepared.duplicated().sum()), "Duplicados exactos"),
        ("missing_customer_rows", int(prepared["CustomerID"].isna().sum()), "Sin CustomerID"),
        ("nonpositive_price_rows", int((prepared["UnitPrice"] <= 0).sum()), "Excluidas de revenue"),
        ("negative_quantity_rows", int((prepared["Quantity"] < 0).sum()), "Cantidades negativas"),
        ("cancelled_invoice_rows", int(prepared["IsCancellation"].sum()), "InvoiceNo inicia con C"),
        (
            "cancellation_mismatch_rows",
            int(cancellation_mismatch.sum()),
            "Prefijo C y cantidad negativa no coinciden",
        ),
        ("positive_purchase_rows", len(positive), "Quantity > 0 y UnitPrice > 0"),
        (
            "identified_positive_purchase_rows",
            len(identified),
            "Compras positivas con CustomerID",
        ),
        ("positive_purchase_revenue", positive_revenue, "Revenue positivo total"),
        (
            "identified_positive_purchase_revenue",
            identified_revenue,
            "Revenue positivo atribuible a un cliente",
        ),
        (
            "identified_revenue_coverage_pct",
            100 * identified_revenue / positive_revenue if positive_revenue else 0,
            "Cobertura del revenue positivo por CustomerID",
        ),
        ("date_min", prepared["InvoiceDate"].min().isoformat(), "Inicio observado"),
        ("date_max", prepared["InvoiceDate"].max().isoformat(), "Fin observado"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "meaning"])
