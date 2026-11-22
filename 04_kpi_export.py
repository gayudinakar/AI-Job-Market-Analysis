"""
==================================================================
  SCRIPT 4: KPI Summary Export for Power BI
==================================================================
PURPOSE:
  Computes all KPI numbers that will appear on Power BI cards,
  then writes them to a compact CSV that Power BI can import
  as a table with single-row metrics.

HOW TO RUN:
  python scripts/04_kpi_export.py

OUTPUT:
  data/cleaned/kpi_summary.csv
  data/cleaned/yearly_trends.csv
  data/cleaned/region_summary.csv
"""

import pandas as pd
import numpy as np
import os

# ── Load data ─────────────────────────────────────────────────────────────────
df       = pd.read_csv(os.path.join("data", "cleaned", "ai_jobs_cleaned.csv"))
df_skills = pd.read_csv(os.path.join("data", "cleaned", "ai_skills_exploded.csv"))

# ── A. KPI flat table ─────────────────────────────────────────────────────────
kpis = {
    "total_jobs":              len(df),
    "unique_companies":        df["company"].nunique(),
    "unique_job_titles":       df["job_title"].nunique(),
    "avg_salary_usd":          round(df["salary_usd"].mean(), 0),
    "median_salary_usd":       round(df["salary_usd"].median(), 0),
    "max_salary_usd":          round(df["salary_usd"].max(), 0),
    "min_salary_usd":          round(df["salary_usd"].min(), 0),
    "pct_remote":              round((df["work_mode"] == "Remote").mean() * 100, 1),
    "pct_hybrid":              round((df["work_mode"] == "Hybrid").mean() * 100, 1),
    "pct_onsite":              round((df["work_mode"] == "Onsite").mean() * 100, 1),
    "pct_visa_sponsored":      round(df["is_visa_sponsored"].mean() * 100, 1),
    "avg_applications":        round(df["applications"].mean(), 1),
    "top_job_title":           df["job_title"].mode()[0],
    "top_skill":               df_skills["skill"].value_counts().idxmax(),
    "top_company":             df["company"].value_counts().idxmax(),
    "top_industry":            df["industry"].value_counts().idxmax(),
    "highest_paid_role":       df.groupby("job_title")["salary_usd"].mean().idxmax(),
    "highest_paid_level":      df.groupby("experience_level")["salary_usd"].mean().idxmax(),
    "pct_entry_level":         round((df["experience_level"] == "Entry").mean() * 100, 1),
    "pct_senior_level":        round((df["experience_level"] == "Senior").mean() * 100, 1),
    "total_skills_analyzed":   df_skills["skill"].nunique(),
}

df_kpi = pd.DataFrame(list(kpis.items()), columns=["metric", "value"])
df_kpi.to_csv(os.path.join("data", "cleaned", "kpi_summary.csv"), index=False)
print("✅ kpi_summary.csv saved")

# ── B. Yearly trends ──────────────────────────────────────────────────────────
yearly = (
    df.groupby("post_year")
      .agg(
          job_count    =("job_id",      "count"),
          avg_salary   =("salary_usd",  "mean"),
          median_salary=("salary_usd",  "median"),
          avg_apps     =("applications","mean"),
          pct_remote   =("work_mode",   lambda x: (x == "Remote").mean() * 100),
          pct_hybrid   =("work_mode",   lambda x: (x == "Hybrid").mean() * 100),
          pct_onsite   =("work_mode",   lambda x: (x == "Onsite").mean() * 100),
      )
      .round(1)
      .reset_index()
)
yearly.to_csv(os.path.join("data", "cleaned", "yearly_trends.csv"), index=False)
print("✅ yearly_trends.csv saved")

# ── C. Region summary ─────────────────────────────────────────────────────────
region = (
    df.groupby("region")
      .agg(
          job_count    =("job_id",     "count"),
          avg_salary   =("salary_usd", "mean"),
          median_salary=("salary_usd", "median"),
      )
      .round(0)
      .reset_index()
      .sort_values("job_count", ascending=False)
)
region.to_csv(os.path.join("data", "cleaned", "region_summary.csv"), index=False)
print("✅ region_summary.csv saved")

# ── D. Experience level summary ───────────────────────────────────────────────
exp_summary = (
    df.groupby("experience_level")
      .agg(
          job_count    =("job_id",     "count"),
          avg_salary   =("salary_usd", "mean"),
          median_salary=("salary_usd", "median"),
      )
      .round(0)
      .reset_index()
)
exp_summary.to_csv(os.path.join("data", "cleaned", "experience_summary.csv"), index=False)
print("✅ experience_summary.csv saved")

# ── E. Top 20 skills frequency ────────────────────────────────────────────────
top20 = (
    df_skills["skill"]
    .value_counts()
    .head(20)
    .reset_index()
)
top20.columns = ["skill", "frequency"]
top20["pct_of_jobs"] = (top20["frequency"] / len(df) * 100).round(1)
top20.to_csv(os.path.join("data", "cleaned", "top_skills_freq.csv"), index=False)
print("✅ top_skills_freq.csv saved")

print("\n🎉 All KPI exports complete — ready to import into Power BI!")
print(f"\n{'='*50}")
print("  Quick KPI Preview:")
print(f"{'='*50}")
for m, v in kpis.items():
    print(f"  {m:<30}: {v}")
