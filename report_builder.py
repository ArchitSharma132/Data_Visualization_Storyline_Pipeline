"""
P6: Report Builder
Compiles all charts + narratives into a professional PDF report.
"""

import os
from datetime import datetime
from fpdf import FPDF


# ── Colour constants (RGB) ────────────────────────────────────────────────────
CRIMSON = (192, 57, 43)
DARK    = (44, 62, 80)
LIGHT   = (250, 250, 250)
WHITE   = (255, 255, 255)
GREY    = (189, 195, 199)


class StoryLineReport(FPDF):
    """Custom FPDF subclass with branded header and footer."""

    def __init__(self, title: str = "Data Visualisation Story Line Report"):
        super().__init__()
        self.report_title = title
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 18, 18)

    # ── Header ────────────────────────────────────────────────────────────────
    def header(self):
        # Red top bar
        self.set_fill_color(*CRIMSON)
        self.rect(0, 0, 210, 8, "F")

        self.set_xy(18, 12)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*CRIMSON)
        self.cell(0, 6, self.report_title, align="L")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GREY)
        self.set_xy(18, 18)

    # ── Footer ────────────────────────────────────────────────────────────────
    def footer(self):
        self.set_y(-14)
        self.set_fill_color(*DARK)
        self.rect(0, self.get_y() - 2, 210, 16, "F")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*WHITE)
        self.cell(0, 10,
                  f"Chandigarh University - CSE Dept  |  Page {self.page_no()}  |  "
                  f"Generated: {datetime.now().strftime('%d %b %Y')}",
                  align="C")

    # ── Section heading ───────────────────────────────────────────────────────
    def section_heading(self, text: str):
        self.ln(4)
        self.set_fill_color(*CRIMSON)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 9, f"  {text}", fill=True, ln=True)
        self.ln(3)
        self.set_text_color(*DARK)

    # ── Sub heading ──────────────────────────────────────────────────────────
    def sub_heading(self, text: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*CRIMSON)
        self.cell(0, 7, text, ln=True)
        self.set_text_color(*DARK)

    # ── Body paragraph ────────────────────────────────────────────────────────
    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 6, text)
        self.ln(2)

    # ── Divider ───────────────────────────────────────────────────────────────
    def divider(self):
        self.set_draw_color(*GREY)
        self.set_line_width(0.3)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(3)

    # ── Insert chart ─────────────────────────────────────────────────────────
    def insert_chart(self, img_path: str, caption: str, narrative: str):
        if not os.path.exists(img_path):
            self.body_text(f"[Chart not found: {img_path}]")
            return

        # Image centred
        self.image(img_path, x=18, w=174)
        self.ln(2)

        # Caption in italic
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GREY)
        self.cell(0, 5, caption, align="C", ln=True)
        self.ln(2)

        # Narrative
        self.body_text(narrative)
        self.divider()

    # ── Key metrics box ───────────────────────────────────────────────────────
    def metrics_box(self, lines: list[str]):
        self.set_fill_color(240, 240, 240)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        x0, y0 = self.get_x(), self.get_y()
        for line in lines:
            self.set_x(22)
            self.cell(0, 7, line, ln=True)
        self.ln(2)


# ── Builder function ─────────────────────────────────────────────────────────
def build_report(chart_paths: dict,
                 narratives: dict,
                 cleaning_log: list[str],
                 out_path: str) -> str:
    """Assemble the full PDF report."""

    pdf = StoryLineReport()

    # ── Cover page ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*CRIMSON)
    pdf.rect(0, 60, 210, 80, "F")

    pdf.set_xy(18, 75)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(174, 14, "Data Visualisation\nStory Line Report", align="C")

    pdf.set_xy(18, 120)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(174, 8, "Sales Analytics - January to June 2024", align="C", ln=True)

    pdf.set_xy(18, 175)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*DARK)
    info_lines = [
        "Submitted by: Ronak Lodhi | Archit Sharma | Jatin Kumar",
        "Submitted to: Mr. Vishal Dutt",
        "Department: Computer Science & Engineering",
        "Institution: Chandigarh University",
        f"Date: {datetime.now().strftime('%d %B %Y')}",
    ]
    for line in info_lines:
        pdf.set_x(18)
        pdf.cell(0, 7, line, ln=True)

    # ── Executive Summary ─────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_heading("Executive Summary")
    for line in narratives["executive_summary"].split("\n"):
        if line.startswith("Total") or line.startswith("Average") or \
           line.startswith("Top") or line.startswith("Best") or \
           line.startswith("Key") or line.startswith("Revenue") or \
           line.startswith("Highest"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*DARK)
            pdf.cell(0, 6, line, ln=True)
        elif line.startswith("EXECUTIVE"):
            pass
        else:
            pdf.body_text(line)

    # ── Data Cleaning Log ─────────────────────────────────────────────────────
    pdf.ln(4)
    pdf.section_heading("Data Cleaning Log")
    pdf.body_text(
        "Before analysis, the raw dataset was cleaned through a structured pipeline. "
        "All changes are recorded below for full transparency and reproducibility:"
    )
    for entry in cleaning_log:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*DARK)
        pdf.set_x(22)
        pdf.multi_cell(168, 6, f"\*  {entry}")
    pdf.ln(2)

    # ── Chart sections ────────────────────────────────────────────────────────
    chart_config = [
        ("monthly_revenue",  "Chart 1 - Monthly Revenue Trend (Line Graph)",
         "Fig 1: Monthly revenue trajectory from January to June 2024"),
        ("category_revenue", "Chart 2 - Revenue by Product Category (Bar Chart)",
         "Fig 2: Revenue contribution per category"),
        ("region_pie",       "Chart 3 - Revenue by Region (Pie Chart)",
         "Fig 3: Geographic revenue distribution"),
        ("product_units",    "Chart 4 - Units Sold per Product (Horizontal Bar)",
         "Fig 4: Volume leaders across product lines"),
        ("age_revenue",      "Chart 5 - Revenue by Customer Age Group (Bar Chart)",
         "Fig 5: Demographic revenue segmentation"),
        ("correlation",      "Chart 6 - Correlation Heatmap",
         "Fig 6: Pairwise correlations between numeric variables"),
        ("scatter",          "Chart 7 - Units Sold vs Revenue (Scatter Plot)",
         "Fig 7: Relationship between volume and revenue by category"),
        ("stacked_monthly",  "Chart 8 - Monthly Revenue by Category (Stacked Bar)",
         "Fig 8: Category mix over time"),
    ]

    for key, heading, caption in chart_config:
        pdf.add_page()
        pdf.section_heading(heading)
        pdf.insert_chart(
            chart_paths.get(key, ""),
            caption,
            narratives.get(key, "No narrative available.")
        )

    # ── Conclusion ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_heading("Conclusion")
    pdf.body_text(
        "The Data Visualisation Story Line project successfully transforms raw "
        "transactional data into a clear, narrative-driven analytical report. "
        "Every chart is accompanied by a structured insight that bridges the gap "
        "between numbers and business decisions."
    )
    pdf.body_text(
        "Key outcomes of this analysis: (1) Revenue grew by over 100% between "
        "January and June, confirming strong business momentum. (2) Electronics "
        "is the dominant revenue category. (3) The 26-35 age group is the most "
        "valuable customer segment. (4) Regional expansion strategies should "
        "target the lower-performing geographies identified in the pie chart."
    )
    pdf.body_text(
        "Future enhancements can extend this framework to include real-time data "
        "feeds, ML-based predictive narratives, and interactive web dashboards - "
        "building on the solid analytical foundation established here."
    )

    # ── Save ──────────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    print(f"[P6] Report saved: {out_path}\n")
    return out_path
