"""
P3: Analysis Engine
Statistical computation, trend detection, correlation analysis.
"""

import pandas as pd


def descriptive_stats(df: pd.DataFrame) -> dict:
    """Compute mean, median, std, min, max for numeric columns."""
    numeric = df.select_dtypes(include="number")
    stats = {}
    for col in numeric.columns:
        stats[col] = {
            "mean":   round(numeric[col].mean(), 2),
            "median": round(numeric[col].median(), 2),
            "std":    round(numeric[col].std(), 2),
            "min":    round(numeric[col].min(), 2),
            "max":    round(numeric[col].max(), 2),
        }
    print("[P3] Descriptive statistics computed.\n")
    return stats


def monthly_revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total revenue per month."""
    trend = (df.groupby("Month")["Revenue"]
               .sum()
               .reset_index()
               .sort_values("Month"))
    return trend


def category_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Total revenue by product category."""
    return (df.groupby("Category")["Revenue"]
              .sum()
              .reset_index()
              .sort_values("Revenue", ascending=False))


def product_units_sold(df: pd.DataFrame) -> pd.DataFrame:
    """Total units sold per product."""
    return (df.groupby("Product")["Units_Sold"]
              .sum()
              .reset_index()
              .sort_values("Units_Sold", ascending=False))


def region_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue breakdown by region."""
    return (df.groupby("Region")["Revenue"]
              .sum()
              .reset_index()
              .sort_values("Revenue", ascending=False))


def top_products_by_revenue(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Top-N products by total revenue."""
    return (df.groupby("Product")["Revenue"]
              .sum()
              .reset_index()
              .sort_values("Revenue", ascending=False)
              .head(n))


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Correlation among numeric columns."""
    return df.select_dtypes(include="number").corr()


def age_group_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue split across customer age bands."""
    bins = [0, 25, 35, 45, 100]
    labels = ["18-25", "26-35", "36-45", "46+"]
    df = df.copy()
    df["Age_Group"] = pd.cut(df["Customer_Age"], bins=bins, labels=labels, right=True)
    return (df.groupby("Age_Group", observed=True)["Revenue"]
              .sum()
              .reset_index())


def run_all_analyses(df: pd.DataFrame) -> dict:
    """Run all analyses and return results dict."""
    print("[P3] Running full analysis suite...")
    results = {
        "descriptive_stats":    descriptive_stats(df),
        "monthly_revenue":      monthly_revenue_trend(df),
        "category_revenue":     category_revenue(df),
        "product_units_sold":   product_units_sold(df),
        "region_revenue":       region_revenue(df),
        "top_products":         top_products_by_revenue(df),
        "correlation":          correlation_matrix(df),
        "age_group_revenue":    age_group_revenue(df),
    }
    print("[P3] All analyses complete.\n")
    return results
