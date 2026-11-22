"""
==================================================================
  SCRIPT 5: Run All Scripts in Sequence (Master Runner)
==================================================================
PURPOSE:
  One command to run the entire pipeline:
    1. Generate dataset
    2. Clean & preprocess
    3. EDA & charts
    4. KPI export

HOW TO RUN:
  python scripts/05_run_all.py

  Or from the project root:
  python -m scripts.05_run_all
"""

import subprocess
import sys
import time
import os

scripts = [
    ("01_generate_dataset.py", "🔄 Generating synthetic dataset"),
    ("02_data_cleaning.py",    "🧹 Cleaning & preprocessing data"),
    ("03_eda_and_charts.py",   "📊 Running EDA & creating charts"),
    ("04_kpi_export.py",       "📋 Exporting KPIs for Power BI"),
]

PYTHON = sys.executable   # uses the same Python that is running this script

print("=" * 60)
print("  🚀  AI JOB MARKET ANALYSIS – Full Pipeline")
print("=" * 60)

total_start = time.time()

for script_file, label in scripts:
    script_path = os.path.join("scripts", script_file)
    print(f"\n{label} …")
    print(f"  Running: {script_path}")
    start = time.time()

    result = subprocess.run(
        [PYTHON, script_path],
        capture_output=False,   # let output stream to console
        text=True,
    )

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"\n❌ ERROR in {script_file}  (exit code {result.returncode})")
        sys.exit(result.returncode)
    else:
        print(f"  ✅ Completed in {elapsed:.1f}s")

total = time.time() - total_start
print("\n" + "=" * 60)
print(f"  🎉 Pipeline finished in {total:.1f}s")
print("  📁 Outputs:")
print("       data/cleaned/   – cleaned CSV files for Power BI")
print("       charts/         – 10 PNG chart files")
print("=" * 60)
