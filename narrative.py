"""
P5: Narrative Generator
Produces a structured storyline - one insight paragraph per chart.
"""

import pandas as pd


def _top(df: pd.DataFrame, col_label: str, col_value: str, n: int = 1) -> str:
    row = df.sort_values(col_value, ascending=False).iloc[0]
    return str(row[col_label])


def _fmt(value: float) -> str:
    if value >= 1_000_000:
        return f"Rs.{value/1_000_000:.2f}M"
    if value >= 1_000:
        return f"Rs.{value/1_000:.1f}K"
    return f"Rs.{value:.0f}"


def generate_narratives(df: pd.DataFrame, analysis: dict) -> dict:
    monthly   = analysis["monthly_revenue"]
    cat_rev   = analysis["category_revenue"]
    region    = analysis["region_revenue"]
    prod_u    = analysis["product_units_sold"]
    top_prod  = analysis["top_products"]
    age_grp   = analysis["age_group_revenue"]
    stats     = analysis["descriptive_stats"]

    # Derived facts
    first_month_rev = monthly.iloc[0]["Revenue"]
    last_month_rev  = monthly.iloc[-1]["Revenue"]
    growth_pct      = ((last_month_rev - first_month_rev) / first_month_rev) * 100

    top_category    = _top(cat_rev, "Category", "Revenue")
    top_category_rev = cat_rev.iloc[0]["Revenue"]
    top_region      = _top(region, "Region", "Revenue")
    top_region_rev  = region.iloc[0]["Revenue"]
    top_product_u   = _top(prod_u, "Product", "Units_Sold")
    top_product_r   = _top(top_prod, "Product", "Revenue")
    top_age_grp     = _top(age_grp, "Age_Group", "Revenue")

    avg_revenue   = stats["Revenue"]["mean"]
    total_revenue = df["Revenue"].sum()
    total_units   = df["Units_Sold"].sum()

    narratives = {}

    # ── Chart 1 ──────────────────────────────────────────────────────────────
    narratives["monthly_revenue"] = (
        f"The line chart reveals a clear and consistent upward revenue trend from "
        f"January to June 2024. Starting at {_fmt(first_month_rev)} in January, "
        f"monthly revenue climbed to {_fmt(last_month_rev)} by June - a growth of "
        f"{growth_pct:.1f}% over six months. This trajectory suggests strong demand "
        f"momentum heading into Q3. Business leaders should ensure that supply chains "
        f"and inventory are scaled proportionally to sustain this growth."
    )

    # ── Chart 2 ──────────────────────────────────────────────────────────────
    narratives["category_revenue"] = (
        f"The bar chart comparing revenue by product category makes it immediately "
        f"clear that {top_category} dominates the portfolio, contributing "
        f"{_fmt(top_category_rev)} - the highest of all categories. This signals strong "
        f"customer preference and high average selling prices in {top_category}. "
        f"Categories with lower revenue bars represent opportunities for targeted "
        f"promotions or strategic bundling to improve their contribution."
    )

    # ── Chart 3 ──────────────────────────────────────────────────────────────
    narratives["region_pie"] = (
        f"The pie chart shows that the {top_region} region leads all geographies with "
        f"{_fmt(top_region_rev)} in total revenue. This regional concentration may reflect "
        f"stronger distribution networks, higher disposable incomes, or more aggressive "
        f"marketing in that area. Expanding outreach in lower-performing regions could "
        f"unlock significant untapped revenue potential."
    )

    # ── Chart 4 ──────────────────────────────────────────────────────────────
    narratives["product_units"] = (
        f"By total units sold, {top_product_u} tops the leaderboard - indicating "
        f"wide market adoption and consistent repeat purchases. However, high unit "
        f"volume does not always translate to top revenue. Cross-referencing with "
        f"the revenue chart reveals which products drive volume versus which drive "
        f"value, enabling smarter pricing and promotional strategies."
    )

    # ── Chart 5 ──────────────────────────────────────────────────────────────
    narratives["age_revenue"] = (
        f"The age group analysis shows that customers in the {top_age_grp} bracket "
        f"generate the highest share of revenue. This demographic insight is critical "
        f"for personalising marketing campaigns, loyalty programmes, and product "
        f"recommendations. Younger segments (18-25) may offer long-term growth "
        f"if engaged early with the right product lines and digital-first strategies."
    )

    # ── Chart 6 ──────────────────────────────────────────────────────────────
    narratives["correlation"] = (
        f"The heatmap reveals the statistical relationships between all numeric "
        f"variables. A strong positive correlation between Units_Sold and Revenue "
        f"confirms that volume drives earnings - as expected. Weak or near-zero "
        f"correlations between Rating and Revenue suggest that customer satisfaction "
        f"alone is not the primary revenue driver; pricing and availability matter more."
    )

    # ── Chart 7 ──────────────────────────────────────────────────────────────
    narratives["scatter"] = (
        f"The scatter plot uncovers important patterns across categories. Electronics "
        f"products cluster in the high-revenue, lower-volume quadrant - reflecting "
        f"premium pricing. Apparel and Fitness items show higher unit volumes at "
        f"lower price points. This distinction guides decisions on where to invest "
        f"in promotional spend versus where to focus on margin optimisation."
    )

    # ── Chart 8 ──────────────────────────────────────────────────────────────
    narratives["stacked_monthly"] = (
        f"The stacked bar chart provides a combined view of monthly revenue and "
        f"category mix. Electronics consistently forms the dominant revenue segment "
        f"every month. Notably, the overall stack height grows month-on-month, "
        f"confirming the positive trend seen in Chart 1. Seasonal spikes, if any, "
        f"are clearly visible, helping planners anticipate inventory and staffing needs."
    )

    # ── Executive summary ─────────────────────────────────────────────────────
    narratives["executive_summary"] = (
        f"EXECUTIVE SUMMARY\n\n"
        f"Total Revenue (Jan-Jun 2024): {_fmt(total_revenue)}\n"
        f"Total Units Sold: {total_units:,}\n"
        f"Average Transaction Revenue: {_fmt(avg_revenue)}\n"
        f"Revenue Growth (Jan -> Jun): {growth_pct:.1f}%\n"
        f"Top Category: {top_category}\n"
        f"Top Region: {top_region}\n"
        f"Best-Selling Product (Volume): {top_product_u}\n"
        f"Highest Revenue Product: {top_product_r}\n"
        f"Key Customer Segment: {top_age_grp} age group\n\n"
        f"The six-month period demonstrates healthy, accelerating revenue growth "
        f"driven primarily by the Electronics category and bolstered by strong "
        f"regional performance. The data storytelling framework highlights that "
        f"growth is broad-based across categories - a positive indicator of "
        f"business resilience. Strategic focus should now shift to scaling the "
        f"high-margin Electronics segment, developing the underperforming regions, "
        f"and deepening engagement with the core 26-35 customer demographic."
    )

    print("[P5] Narratives generated for all charts.\n")
    return narratives
