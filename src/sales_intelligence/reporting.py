"""Generacion de artefactos y narrativa del caso de estudio."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def save_monthly_chart(monthly: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(monthly["Month"], monthly["net_revenue"], marker="o", linewidth=2)
    partial_month = monthly.loc[monthly["Month"] == "2011-12"]
    if not partial_month.empty:
        row = partial_month.iloc[0]
        ax.scatter(
            row["Month"],
            row["net_revenue"],
            color="tab:orange",
            edgecolor="black",
            zorder=3,
        )
        ax.annotate(
            "Mes parcial\n(hasta 09 dic)",
            (row["Month"], row["net_revenue"]),
            xytext=(-58, 28),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->", "color": "tab:orange"},
        )
    ax.set_title("Revenue neto mensual")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Revenue (GBP)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def _segment_value(
    segments: pd.DataFrame, month: str, customer_type: str, column: str
) -> float:
    values = segments.loc[
        (segments["Month"] == month)
        & (segments["CustomerType"] == customer_type),
        column,
    ]
    return float(values.iloc[0]) if not values.empty else 0.0


def build_report(
    monthly: pd.DataFrame,
    segments: pd.DataFrame,
    quality: pd.DataFrame,
    source_name: str,
) -> str:
    """Crea un reporte Markdown rastreable a las salidas tabulares."""
    monthly_index = monthly.set_index("Month")
    required = {"2011-09", "2011-10", "2011-11"}
    has_focus_period = required.issubset(set(monthly_index.index))

    focus = "No estan disponibles los tres meses del periodo de estudio."
    if has_focus_period:
        sep_revenue = float(monthly_index.loc["2011-09", "net_revenue"])
        oct_revenue = float(monthly_index.loc["2011-10", "net_revenue"])
        nov_revenue = float(monthly_index.loc["2011-11", "net_revenue"])
        growth_oct_nov = 100 * (nov_revenue / oct_revenue - 1)

        sep_new = _segment_value(segments, "2011-09", "New", "customers")
        sep_returning = _segment_value(segments, "2011-09", "Returning", "customers")
        oct_new = _segment_value(segments, "2011-10", "New", "customers")
        oct_returning = _segment_value(segments, "2011-10", "Returning", "customers")
        nov_new = _segment_value(segments, "2011-11", "New", "customers")
        nov_returning = _segment_value(segments, "2011-11", "Returning", "customers")
        nov_new_revenue = _segment_value(
            segments, "2011-11", "New", "purchase_revenue"
        )
        nov_returning_revenue = _segment_value(
            segments, "2011-11", "Returning", "purchase_revenue"
        )
        identified_nov_revenue = nov_new_revenue + nov_returning_revenue
        returning_share = (
            100 * nov_returning_revenue / identified_nov_revenue
            if identified_nov_revenue
            else 0
        )

        focus = f"""
| Mes | Revenue neto | Clientes New | Clientes Returning |
|---|---:|---:|---:|
| 2011-09 | {sep_revenue:,.2f} | {sep_new:,.0f} | {sep_returning:,.0f} |
| 2011-10 | {oct_revenue:,.2f} | {oct_new:,.0f} | {oct_returning:,.0f} |
| 2011-11 | {nov_revenue:,.2f} | {nov_new:,.0f} | {nov_returning:,.0f} |

De octubre a noviembre, el revenue neto aumento {growth_oct_nov:.1f}%. Los clientes
`New` bajaron de {oct_new:,.0f} a {nov_new:,.0f}, mientras los `Returning` subieron de
{oct_returning:,.0f} a {nov_returning:,.0f}. Dentro de las compras positivas con
cliente identificado, los recurrentes aportaron {returning_share:.1f}% del revenue de
noviembre. La evidencia descriptiva indica que el pico coincide principalmente con
actividad de clientes ya observados; no demuestra que la recurrencia causara el aumento.
""".strip()

    quality_index = quality.set_index("metric")["value"]
    coverage = float(quality_index["identified_revenue_coverage_pct"])
    missing_customers = int(quality_index["missing_customer_rows"])
    duplicate_rows = int(quality_index["duplicate_rows"])

    return f"""# Reporte reproducible de sales intelligence

Fuente procesada: `{source_name}`.

## Pregunta de negocio

¿El aumento de ventas entre septiembre y noviembre de 2011 coincide principalmente
con adquisicion de clientes nuevos, actividad de clientes recurrentes o ambas?

## Resultado

{focus}

## Definiciones

- **Revenue neto:** suma de `Quantity * UnitPrice` en filas con `UnitPrice > 0`;
  incorpora cantidades negativas.
- **New:** cliente cuya compra positiva ocurre en su primer mes de compra positiva
  observado en el archivo.
- **Returning:** cliente con una compra positiva posterior a ese primer mes observado.
- La segmentacion excluye devoluciones y filas sin `CustomerID`; por eso su revenue no
  reconcilia directamente con el revenue neto total.

## Calidad y limites

- {missing_customers:,} filas no tienen `CustomerID`.
- El revenue positivo con cliente identificable cubre {coverage:.1f}% del revenue
  positivo total.
- Se detectaron {duplicate_rows:,} filas exactamente duplicadas; se cuantifican pero no
  se eliminan porque no hay una clave de linea confirmada para distinguir duplicados
  erroneos de registros validos.
- Diciembre de 2011 termina el dia 9 y no debe compararse como un mes completo.
- `New` significa nuevo en la ventana observada, no necesariamente nuevo para el negocio.
- El analisis es descriptivo: asociacion temporal no equivale a causalidad.

## Artefactos auditables

- `monthly_metrics.csv`: revenue, unidades, facturas y clientes por mes.
- `customer_segments.csv`: clientes, facturas y revenue positivo por tipo.
- `data_quality.csv`: exclusiones, cobertura y controles de consistencia.
- `monthly_revenue.png`: visualizacion del revenue neto mensual.
"""
