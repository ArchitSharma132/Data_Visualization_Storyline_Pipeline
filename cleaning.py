"""
P2: Data Cleaning Module
Removes nulls, duplicates, fixes types, and logs all changes.
"""

import pandas as pd


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Clean the dataset and return (cleaned_df, change_log).
    """
    log = []
    df = df.copy()

    # ── Step 1: Remove fully empty rows ─────────────────────────────────────
    before = len(df)
    df.dropna(how="all", inplace=True)
    removed_empty = before - len(df)
    if removed_empty:
        log.append(f"Removed {removed_empty} fully empty row(s).")

    # ── Step 2: Remove duplicate rows ────────────────────────────────────────
    before = len(df)
    df.drop_duplicates(inplace=True)
    removed_dupes = before - len(df)
    if removed_dupes:
        log.append(f"Removed {removed_dupes} duplicate row(s).")

    # ── Step 3: Drop rows missing critical columns ───────────────────────────
    critical = ["Date", "Product", "Category", "Revenue"]
    existing_critical = [c for c in critical if c in df.columns]
    before = len(df)
    df.dropna(subset=existing_critical, inplace=True)
    removed_critical = before - len(df)
    if removed_critical:
        log.append(f"Dropped {removed_critical} row(s) missing critical fields: {existing_critical}.")

    # ── Step 4: Parse dates ──────────────────────────────────────────────────
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        bad_dates = df["Date"].isna().sum()
        df.dropna(subset=["Date"], inplace=True)
        if bad_dates:
            log.append(f"Dropped {bad_dates} row(s) with unparseable dates.")
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        df["Month_Num"] = df["Date"].dt.month
        log.append("Derived 'Month' and 'Month_Num' columns from 'Date'.")

    # ── Step 5: Fix numeric columns ──────────────────────────────────────────
    numeric_cols = ["Units_Sold", "Unit_Price", "Revenue", "Customer_Age", "Rating"]
    for col in numeric_cols:
        if col in df.columns:
            before_nulls = df[col].isna().sum()
            df[col] = pd.to_numeric(df[col], errors="coerce")
            after_nulls = df[col].isna().sum()
            if after_nulls > before_nulls:
                log.append(f"Coerced {after_nulls - before_nulls} non-numeric value(s) in '{col}' to NaN.")
            median_val = df[col].median()
            filled = df[col].isna().sum()
            df[col] = df[col].fillna(median_val)
            if filled:
                log.append(f"Filled {filled} NaN(s) in '{col}' with median ({median_val:.2f}).")

    # ── Step 6: Standardise string columns ──────────────────────────────────
    for col in ["Product", "Category", "Region"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    log.append("Standardised casing on Product, Category, Region columns.")

    # ── Step 7: Reset index ──────────────────────────────────────────────────
    df.reset_index(drop=True, inplace=True)
    log.append(f"Final clean dataset: {len(df)} rows × {len(df.columns)} columns.")

    print("[P2] Data Cleaning Complete:")
    for entry in log:
        print(f"     • {entry}")
    print()

    return df, log
