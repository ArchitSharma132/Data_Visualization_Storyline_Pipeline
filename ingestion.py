"""
P1: Data Ingestion Module
Loads dataset from CSV or Excel files and validates structure.
"""

import pandas as pd
import os


def load_dataset(filepath: str) -> pd.DataFrame:
    """Load dataset from CSV or Excel file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    print(f"[P1] Dataset loaded: {filepath}")
    print(f"     Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"     Columns: {list(df.columns)}\n")
    return df


def validate_structure(df: pd.DataFrame) -> dict:
    """Basic structural validation and summary."""
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    print("[P1] Validation Summary:")
    print(f"     Rows: {report['total_rows']} | Columns: {report['total_columns']}")
    print(f"     Duplicates found: {report['duplicate_rows']}")
    print(f"     Columns with nulls: "
          f"{[c for c, v in report['null_counts'].items() if v > 0]}\n")

    return report
