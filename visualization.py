"""
P4: Visualization Module
Creates all charts using Matplotlib and Seaborn.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

# ── Global style ─────────────────────────────────────────────────────────────
PALETTE = ["#C0392B", "#2C3E50", "#E67E22", "#27AE60", "#2980B9",
           "#8E44AD", "#F39C12", "#16A085"]
CRIMSON  = "#C0392B"
DARK     = "#2C3E50"
BG       = "#FAFAFA"

sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   BG,
    "axes.edgecolor":   DARK,
    "axes.labelcolor":  DARK,
    "xtick.color":      DARK,
    "ytick.color":      DARK,
    "text.color":       DARK,
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   14,
    "axes.labelsize":   11,
})


def _save(fig: plt.Figure, out_dir: str, filename: str) -> str:
    path = os.path.join(out_dir, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  [P4] Saved: {filename}")
    return path


def fmt_lakhs(x, _):
    """Format large rupee values as Rs.X.XL."""
    if x >= 1_000_000:
        return f"Rs.{x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"Rs.{x/1_000:.1f}K"
    return f"Rs.{x:.0f}"


def _smart_scale(max_val):
    """Pick divisor and unit label based on data magnitude."""
    if max_val >= 1_000_000:
        return 1_000_000, "M", "Millions"
    if max_val >= 1_000:
        return 1_000, "K", "Thousands"
    return 1, "", ""


# ── Chart 1: Monthly Revenue Trend (Line) ────────────────────────────────────
def plot_monthly_revenue(monthly_df: pd.DataFrame, out_dir: str) -> str:
    div, unit, unit_long = _smart_scale(monthly_df["Revenue"].max())
    fig, ax = plt.subplots(figsize=(10, 5))
    y_vals = monthly_df["Revenue"] / div
    ax.plot(monthly_df["Month"], y_vals,
            marker="o", color=CRIMSON, linewidth=2.5, markersize=8, label=f"Revenue ({unit})")
    ax.fill_between(monthly_df["Month"], y_vals, alpha=0.12, color=CRIMSON)
    # Dynamic title showing actual date range
    months = monthly_df["Month"].tolist()
    title_range = f"{months[0]} – {months[-1]}" if len(months) > 1 else months[0]
    ax.set_title(f"Monthly Revenue Trend ({title_range})", fontweight="bold", pad=14)
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Revenue (Rs. {unit_long})" if unit_long else "Revenue (Rs.)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x:.1f}{unit}"))
    ax.set_xticks(range(len(monthly_df)))
    ax.set_xticklabels(monthly_df["Month"], rotation=30, ha="right")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    return _save(fig, out_dir, "01_monthly_revenue_trend.png")


# ── Chart 2: Revenue by Category (Bar) ───────────────────────────────────────
def plot_category_revenue(cat_df: pd.DataFrame, out_dir: str) -> str:
    div, unit, unit_long = _smart_scale(cat_df["Revenue"].max())
    fig, ax = plt.subplots(figsize=(10, 6))
    y_vals = cat_df["Revenue"] / div
    # Shorten long category names for readability
    short_names = [n.replace(" and ", " & ") for n in cat_df["Category"]]
    bars = ax.bar(short_names, y_vals,
                  color=PALETTE[:len(cat_df)], edgecolor="white", linewidth=0.8)
    max_h = y_vals.max()
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max_h * 0.02,
                f"Rs.{bar.get_height():.1f}{unit}",
                ha="center", va="bottom", fontsize=9, fontweight="bold", color=DARK)
    ax.set_title("Total Revenue by Product Category", fontweight="bold", pad=14)
    ax.set_xlabel("Category")
    ax.set_ylabel(f"Revenue (Rs. {unit_long})" if unit_long else "Revenue (Rs.)")
    ax.set_ylim(0, max_h * 1.18)
    ax.set_xticks(range(len(short_names)))
    ax.set_xticklabels(short_names, rotation=25, ha="right", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.subplots_adjust(bottom=0.18)
    return _save(fig, out_dir, "02_category_revenue_bar.png")


# ── Chart 3: Region Revenue (Pie) ─────────────────────────────────────────────
def plot_region_pie(region_df: pd.DataFrame, out_dir: str) -> str:
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        region_df["Revenue"],
        labels=region_df["Region"],
        autopct="%1.1f%%",
        colors=PALETTE[:len(region_df)],
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        pctdistance=0.80,
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
    ax.set_title("Revenue Share by Region", fontweight="bold", pad=14)
    return _save(fig, out_dir, "03_region_revenue_pie.png")


# ── Chart 4: Top Products by Units Sold (Horizontal Bar) ─────────────────────
def plot_top_products(prod_df: pd.DataFrame, out_dir: str) -> str:
    prod_df = prod_df.sort_values("Units_Sold")
    # Show top 15 products max to keep chart readable
    if len(prod_df) > 15:
        prod_df = prod_df.tail(15)
    n = len(prod_df)
    fig_h = max(5, n * 0.45)  # scale figure height to product count
    fig, ax = plt.subplots(figsize=(10, fig_h))
    # Shorten product names: "NextGen Electronic accessories" → "NextGen Elec."
    short = []
    for name in prod_df["Product"]:
        parts = name.split()
        if len(parts) > 2:
            short.append(parts[0] + " " + parts[1][:4] + ".")
        else:
            short.append(name)
    colors = [PALETTE[i % len(PALETTE)] for i in range(n)]
    bars = ax.barh(short, prod_df["Units_Sold"], color=colors, edgecolor="white", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + prod_df["Units_Sold"].max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width()):,}", va="center", fontsize=9, color=DARK)
    ax.set_title("Top Products by Units Sold", fontweight="bold", pad=14)
    ax.set_xlabel("Units Sold")
    ax.set_xlim(0, prod_df["Units_Sold"].max() * 1.12)
    ax.tick_params(axis="y", labelsize=9)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    fig.subplots_adjust(left=0.22)
    return _save(fig, out_dir, "04_product_units_sold_bar.png")


# ── Chart 5: Age Group vs Revenue (Bar) ──────────────────────────────────────
def plot_age_group_revenue(age_df: pd.DataFrame, out_dir: str) -> str:
    div, unit, unit_long = _smart_scale(age_df["Revenue"].max())
    fig, ax = plt.subplots(figsize=(8, 5))
    y_vals = age_df["Revenue"] / div
    bars = ax.bar(age_df["Age_Group"].astype(str), y_vals,
                  color=[CRIMSON, "#E67E22", "#27AE60", "#2980B9"],
                  edgecolor="white", linewidth=0.8, width=0.55)
    max_h = y_vals.max()
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max_h * 0.02,
                f"Rs.{bar.get_height():.1f}{unit}",
                ha="center", va="bottom", fontsize=9, fontweight="bold", color=DARK)
    ax.set_title("Revenue by Customer Age Group", fontweight="bold", pad=14)
    ax.set_xlabel("Age Group")
    ax.set_ylabel(f"Revenue (Rs. {unit_long})" if unit_long else "Revenue (Rs.)")
    ax.set_ylim(0, max_h * 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    return _save(fig, out_dir, "05_age_group_revenue.png")


# ── Chart 6: Correlation Heatmap ──────────────────────────────────────────────
def plot_correlation_heatmap(corr_df: pd.DataFrame, out_dir: str) -> str:
    fig, ax = plt.subplots(figsize=(8, 6))
    mask = corr_df.isnull()
    cmap = sns.diverging_palette(10, 220, as_cmap=True)
    sns.heatmap(corr_df, annot=True, fmt=".2f", cmap=cmap,
                linewidths=0.5, linecolor="white",
                vmin=-1, vmax=1, center=0, ax=ax,
                annot_kws={"size": 10, "weight": "bold"}, mask=mask)
    ax.set_title("Correlation Matrix — Numeric Variables", fontweight="bold", pad=14)
    return _save(fig, out_dir, "06_correlation_heatmap.png")


# ── Chart 7: Scatter — Units Sold vs Revenue ──────────────────────────────────
def plot_scatter(df: pd.DataFrame, out_dir: str) -> str:
    div, unit, unit_long = _smart_scale(df["Revenue"].max())
    fig, ax = plt.subplots(figsize=(10, 6))
    categories = df["Category"].unique()
    cat_colors = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(categories)}
    # Shorten category names for a cleaner legend
    short_map = {c: c.replace(" and ", " & ") for c in categories}
    for cat in categories:
        sub = df[df["Category"] == cat]
        ax.scatter(sub["Units_Sold"], sub["Revenue"] / div,
                   label=short_map[cat], color=cat_colors[cat],
                   alpha=0.55, s=40, edgecolors="white", linewidths=0.4)
    ax.set_title("Units Sold vs Revenue (by Category)", fontweight="bold", pad=14)
    ax.set_xlabel("Units Sold")
    ax.set_ylabel(f"Revenue (Rs. {unit_long})" if unit_long else "Revenue (Rs.)")
    ax.legend(title="Category", fontsize=8, title_fontsize=9,
             loc="upper left", framealpha=0.9, edgecolor="#ddd")
    ax.grid(linestyle="--", alpha=0.3)
    return _save(fig, out_dir, "07_scatter_units_revenue.png")


# ── Chart 8: Monthly Revenue by Category (Stacked Bar) ───────────────────────
def plot_stacked_monthly(df: pd.DataFrame, out_dir: str) -> str:
    raw_pivot = df.pivot_table(index="Month", columns="Category",
                               values="Revenue", aggfunc="sum").fillna(0)
    div, unit, unit_long = _smart_scale(raw_pivot.sum(axis=1).max())
    pivot = raw_pivot / div
    pivot = pivot.loc[sorted(pivot.index)]

    fig, ax = plt.subplots(figsize=(11, 6))
    pivot.plot(kind="bar", stacked=True, ax=ax,
               color=PALETTE[:len(pivot.columns)], edgecolor="white", linewidth=0.6)
    ax.set_title("Monthly Revenue Split by Category", fontweight="bold", pad=14)
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Revenue (Rs. {unit_long})" if unit_long else "Revenue (Rs.)")
    ax.set_xticklabels(pivot.index, rotation=30, ha="right")
    ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    return _save(fig, out_dir, "08_stacked_monthly_category.png")


# ── Master function ───────────────────────────────────────────────────────────
def generate_all_charts(df: pd.DataFrame, analysis: dict, out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    print("[P4] Generating visualizations...")
    paths = {
        "monthly_revenue":   plot_monthly_revenue(analysis["monthly_revenue"], out_dir),
        "category_revenue":  plot_category_revenue(analysis["category_revenue"], out_dir),
        "region_pie":        plot_region_pie(analysis["region_revenue"], out_dir),
        "product_units":     plot_top_products(analysis["product_units_sold"], out_dir),
        "age_revenue":       plot_age_group_revenue(analysis["age_group_revenue"], out_dir),
        "correlation":       plot_correlation_heatmap(analysis["correlation"], out_dir),
        "scatter":           plot_scatter(df, out_dir),
        "stacked_monthly":   plot_stacked_monthly(df, out_dir),
    }
    print(f"[P4] All {len(paths)} charts generated.\n")
    return paths
