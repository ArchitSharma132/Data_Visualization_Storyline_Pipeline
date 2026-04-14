"""
main.py — Data Visualisation Story Line
========================================
Entry point for the full pipeline:
  P1 → Ingest  →  P2 → Clean  →  P3 → Analyse
  →  P4 → Visualise  →  P5 → Narrate  →  P6 → Report

Usage:
    python main.py                          # uses default dataset
    python main.py --data path/to/data.csv  # custom dataset
    python main.py --help
"""

import argparse
import os
import sys

#Make sure the pipeline package is importable 
sys.path.insert(0, os.path.dirname(__file__))

from pipeline.ingestion      import load_dataset, validate_structure
from pipeline.cleaning       import clean_dataset
from pipeline.analysis       import run_all_analyses
from pipeline.visualization  import generate_all_charts
from pipeline.narrative      import generate_narratives
from pipeline.report_builder import build_report


#Paths 
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(BASE_DIR, "data", "sales_data.csv")
CHART_DIR   = os.path.join(BASE_DIR, "output", "charts")
REPORT_PATH = os.path.join(BASE_DIR, "output", "DataViz_StoryLine_Report.pdf")


def print_banner():
    print("\n" + "=" * 60)
    print("  DATA VISUALISATION STORY LINE")
    print("  Chandigarh University — CSE Department")
    print("  Ronak Lodhi | Archit Sharma | Jatin Kumar")
    print("=" * 60 + "\n")


def main(csv_path: str):
    print_banner()

    #P1: Ingest
    df_raw = load_dataset(csv_path)
    validate_structure(df_raw)

    #P2: Clean 
    df_clean, cleaning_log = clean_dataset(df_raw)

    #P3: Analyse 
    analysis = run_all_analyses(df_clean)

    #P4: Visualise
    chart_paths = generate_all_charts(df_clean, analysis, CHART_DIR)

    #P5: Narrate 
    narratives = generate_narratives(df_clean, analysis)

    #P6: Report
    build_report(chart_paths, narratives, cleaning_log, REPORT_PATH)

    #Summary
    print("=" * 60)
    print("  PIPELINE COMPLETE")
    print(f"  Charts : {CHART_DIR}")
    print(f"  Report : {REPORT_PATH}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Data Visualisation Story Line — full analytics pipeline"
    )
    parser.add_argument(
        "--data",
        default=DEFAULT_CSV,
        help=f"Path to input CSV or Excel file (default: {DEFAULT_CSV})"
    )
    args = parser.parse_args()
    main(args.data)
