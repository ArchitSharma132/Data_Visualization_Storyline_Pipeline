# Data Visualisation Story Line
---

## Overview
A structured, end-to-end Python pipeline that transforms raw sales data into a
**narrative-driven PDF report** with eight professional visualisations and
automatically generated business insights.

## Pipeline Stages
| Stage | Module | Description |
|-------|--------|-------------|
| P1 | `pipeline/ingestion.py` | Load CSV/Excel, validate structure |
| P2 | `pipeline/cleaning.py` | Remove nulls/dupes, fix types, log changes |
| P3 | `pipeline/analysis.py` | Stats, trends, correlations |
| P4 | `pipeline/visualization.py` | 8 charts (bar, line, pie, scatter, heatmap, stacked) |
| P5 | `pipeline/narrative.py` | Auto-generate story text per chart |
| P6 | `pipeline/report_builder.py` | Compile PDF report |

## Project Structure
```
data_viz_project/
├── main.py                     ← Entry point
├── requirements.txt
├── data/
│   └── sales_data.csv          ← Sample dataset (replace with your own)
├── pipeline/
│   ├── ingestion.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── visualization.py
│   ├── narrative.py
│   └── report_builder.py
└── output/
    ├── charts/                 ← Generated PNG charts
    └── DataViz_StoryLine_Report.pdf
```

## Setup & Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with default dataset
python main.py

# 3. Run with your own dataset
python main.py --data path/to/your_data.csv
```

## Dataset Format (CSV)
Required columns:
- `Date` — transaction date (YYYY-MM-DD)
- `Product` — product name
- `Category` — product category
- `Region` — sales region
- `Units_Sold` — number of units
- `Unit_Price` — price per unit
- `Revenue` — total revenue (Units_Sold × Unit_Price)
- `Customer_Age` — buyer's age
- `Rating` — product rating (1–5)

## Output
- **8 PNG charts** saved to `output/charts/`
- **1 PDF report** saved to `output/DataViz_StoryLine_Report.pdf`

The PDF includes: cover page, executive summary, data cleaning log,
8 chart pages (each with the chart + narrative), and a conclusion.
