"""Orquestacion de carga, analisis y escritura de resultados."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .analysis import (
    analyzable_transactions,
    customer_segments_monthly,
    monthly_metrics,
    prepare_transactions,
    quality_metrics,
)
from .reporting import build_report, save_monthly_chart


@dataclass(frozen=True)
class AnalysisRun:
    total_rows: int
    analyzed_rows: int
    net_revenue: float
    output_dir: Path
    report_path: Path


def load_excel(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"No se encontro el archivo de entrada: {path}. "
            "Consulta README.md para descargar el dataset."
        )
    try:
        return pd.read_excel(path, sheet_name="Online Retail")
    except ValueError as error:
        raise ValueError(
            "El libro debe contener una hoja llamada 'Online Retail'."
        ) from error


def run_analysis(input_path: Path, output_dir: Path) -> AnalysisRun:
    raw = load_excel(input_path)
    prepared = prepare_transactions(raw)
    analyzed = analyzable_transactions(prepared)
    monthly = monthly_metrics(prepared)
    segments = customer_segments_monthly(prepared)
    quality = quality_metrics(prepared)

    output_dir.mkdir(parents=True, exist_ok=True)
    monthly.to_csv(output_dir / "monthly_metrics.csv", index=False)
    segments.to_csv(output_dir / "customer_segments.csv", index=False)
    quality.to_csv(output_dir / "data_quality.csv", index=False)
    save_monthly_chart(monthly, output_dir / "monthly_revenue.png")

    report_path = output_dir / "report.md"
    report_path.write_text(
        build_report(monthly, segments, quality, input_path.name),
        encoding="utf-8",
    )
    return AnalysisRun(
        total_rows=len(prepared),
        analyzed_rows=len(analyzed),
        net_revenue=float(analyzed["Revenue"].sum()),
        output_dir=output_dir,
        report_path=report_path,
    )
