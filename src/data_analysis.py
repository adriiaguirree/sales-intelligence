"""Punto de entrada del analisis reproducible de ventas."""

from __future__ import annotations

import argparse
from pathlib import Path

from sales_intelligence.pipeline import run_analysis


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analiza el dataset Online Retail y genera un reporte reproducible."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "Online Retail.xlsx",
        help="Ruta al archivo .xlsx de entrada.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "outputs",
        help="Directorio para CSV, grafica y reporte.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_analysis(args.input, args.output_dir)

    print("Analisis completado.")
    print(f"Filas de entrada: {result.total_rows:,}")
    print(f"Filas con UnitPrice > 0: {result.analyzed_rows:,}")
    print(f"Revenue neto: {result.net_revenue:,.2f}")
    print(f"Reporte: {result.report_path}")
    print(f"Salidas: {result.output_dir}")


if __name__ == "__main__":
    main()
