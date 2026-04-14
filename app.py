import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from pipeline.ingestion import load_dataset, validate_structure
from pipeline.cleaning import clean_dataset
from pipeline.analysis import run_all_analyses
from pipeline.visualization import generate_all_charts
from pipeline.narrative import generate_narratives
from pipeline.report_builder import build_report

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHART_DIR = os.path.join(BASE_DIR, "output", "charts")
REPORT_PATH = os.path.join(BASE_DIR, "output", "DataViz_StoryLine_Report.pdf")

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "templates"),
            static_folder=os.path.join(BASE_DIR, "static"))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Pipeline state — starts empty (no pre-loaded data) 
pipeline_state = {
    "ran": False,
    "narratives": {},
    "cleaning_log": [],
    "chart_paths": {},
    "dataset_info": {},
    "filename": "",
    "error": None,
}


def run_pipeline(csv_path: str, original_filename: str):
    """Execute the full 6-stage pipeline and cache results."""
    global pipeline_state
    try:
        df_raw = load_dataset(csv_path)
        validate_structure(df_raw)
        df_clean, cleaning_log = clean_dataset(df_raw)
        analysis = run_all_analyses(df_clean)
        chart_paths = generate_all_charts(df_clean, analysis, CHART_DIR)
        narratives = generate_narratives(df_clean, analysis)
        build_report(chart_paths, narratives, cleaning_log, REPORT_PATH)

        total_revenue = float(df_clean["Revenue"].sum())
        total_units = int(df_clean["Units_Sold"].sum())
        avg_revenue = float(df_clean["Revenue"].mean())
        num_products = int(df_clean["Product"].nunique())
        num_categories = int(df_clean["Category"].nunique())
        num_regions = int(df_clean["Region"].nunique())
        date_range = f"{df_clean['Date'].min().strftime('%b %Y')} — {df_clean['Date'].max().strftime('%b %Y')}"

        pipeline_state = {
            "ran": True,
            "narratives": narratives,
            "cleaning_log": cleaning_log,
            "chart_paths": chart_paths,
            "dataset_info": {
                "total_revenue": total_revenue,
                "total_units": total_units,
                "avg_revenue": avg_revenue,
                "num_products": num_products,
                "num_categories": num_categories,
                "num_regions": num_regions,
                "date_range": date_range,
                "rows": len(df_clean),
                "cols": len(df_clean.columns),
            },
            "filename": original_filename,
            "error": None,
        }
    except Exception as e:
        pipeline_state["error"] = str(e)
        pipeline_state["ran"] = False
        raise


# Routes 
@app.route("/")
def index():
    return render_template("index.html", state=pipeline_state)


@app.route("/charts/<path:filename>")
def serve_chart(filename):
    return send_from_directory(CHART_DIR, filename)


@app.route("/download-report")
def download_report():
    if os.path.exists(REPORT_PATH):
        return send_from_directory(os.path.dirname(REPORT_PATH),
                                   os.path.basename(REPORT_PATH),
                                   as_attachment=True)
    return "Report not yet generated. Upload a dataset first.", 404


@app.route("/upload", methods=["POST"])
def upload():
    if "datafile" not in request.files:
        return redirect(url_for("index"))
    file = request.files["datafile"]
    if file.filename == "":
        return redirect(url_for("index"))

    save_path = os.path.join(DATA_DIR, "sales_data.csv")
    os.makedirs(DATA_DIR, exist_ok=True)
    file.save(save_path)

    try:
        run_pipeline(save_path, file.filename)
    except Exception as e:
        pipeline_state["error"] = str(e)
        pipeline_state["ran"] = False

    return redirect(url_for("index"))


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DATA VISUALISATION STORY LINE — WEB DASHBOARD")
    print("  Open: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=False, host="0.0.0.0", port=5000)
