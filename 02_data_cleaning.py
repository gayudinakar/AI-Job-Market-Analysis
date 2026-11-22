"""
============================================================
  SCRIPT 2: Data Cleaning & Preprocessing with Pandas
============================================================
PURPOSE:
  Reads the raw CSV, fixes quality issues, engineers new
  features, and exports a clean CSV for analysis and Power BI.

STEPS COVERED:
  1. Load data
  2. Remove exact duplicates
  3. Handle missing values
  4. Standardise text columns
  5. Convert data types
  6. Feature engineering (year, quarter, skill lists, etc.)
  7. Remove outliers in salary
  8. Save cleaned output

HOW TO RUN:
  python scripts/02_data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

# ── STEP 1: Load raw data ────────────────────────────────────────────────────
raw_path = os.path.join("data", "raw", "ai_jobs_raw.csv")
print(f"Loading data from: {raw_path}")
df = pd.read_csv(raw_path)
print(f"  Raw shape: {df.shape}")

# ── STEP 2: Remove exact duplicate rows ─────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
print(f"  Duplicates removed: {before - len(df)}")

# ── STEP 3: Handle missing values ────────────────────────────────────────────
# (a) Salary – fill nulls with the MEDIAN salary for that experience level
df["salary_usd"] = df.groupby("experience_level")["salary_usd"] \
                     .transform(lambda x: x.fillna(x.median()))

# (b) Location – fill with the most frequent location ('mode')
df["location"] = df["location"].fillna(df["location"].mode()[0])

# (c) Education level – fill with 'No Preference'
df["education_level"] = df["education_level"].fillna("No Preference")

print(f"  Missing after imputation:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# ── STEP 4: Standardise text columns ────────────────────────────────────────
# Strip leading/trailing whitespace and fix capitalisation
text_cols = ["job_title", "company", "location", "experience_level",
             "employment_type", "work_mode", "industry",
             "company_size", "education_level"]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# Normalise work_mode spelling edge cases
df["work_mode"] = df["work_mode"].str.replace("Work From Home", "Remote", regex=False)

# ── STEP 5: Convert data types ───────────────────────────────────────────────
df["job_posted_date"] = pd.to_datetime(df["job_posted_date"], errors="coerce")
df["salary_usd"]      = df["salary_usd"].astype(float)
df["applications"]    = df["applications"].astype(int)
df["is_visa_sponsored"] = df["is_visa_sponsored"].astype(bool)

# ── STEP 6: Feature Engineering ──────────────────────────────────────────────
# (a) Date-based features
df["post_year"]    = df["job_posted_date"].dt.year
df["post_quarter"] = "Q" + df["job_posted_date"].dt.quarter.astype(str)
df["post_month"]   = df["job_posted_date"].dt.month_name()
df["post_yearqtr"] = df["post_year"].astype(str) + "-" + df["post_quarter"]

# (b) Extract country / region from location
def extract_region(loc: str) -> str:
    loc = str(loc)
    if "Remote" in loc:   return "Remote"
    if ", CA" in loc or ", NY" in loc or ", WA" in loc or \
       ", TX" in loc or ", MA" in loc or ", IL" in loc or \
       ", GA" in loc or ", CO" in loc:
        return "USA"
    if "UK" in loc:        return "UK"
    if "Canada" in loc:    return "Canada"
    if "Germany" in loc:   return "Germany"
    if "Singapore" in loc: return "Singapore"
    if "India" in loc:     return "India"
    return "Other"

df["region"] = df["location"].apply(extract_region)

# (c) Salary band / tier (useful for grouping in Power BI)
bins   = [0, 80_000, 110_000, 150_000, 200_000, 300_000]
labels = ["<$80K", "$80K–$110K", "$110K–$150K", "$150K–$200K", ">$200K"]
df["salary_band"] = pd.cut(df["salary_usd"], bins=bins, labels=labels, right=False)

# (d) Skill count – how many skills each posting requires
df["skill_count"] = df["required_skills"].apply(
    lambda x: len(str(x).split(","))
)

# (e) Binary flags for most demanded skills
top_skills = ["Python", "Pytorch", "Tensorflow", "Sql", "Aws",
              "Machine Learning", "Nlp", "Docker", "Kubernetes", "Llms"]

# Title-case skills column so matching works
df["required_skills_norm"] = df["required_skills"].str.title()

for skill in top_skills:
    col_name = f"skill_{skill.lower().replace(' ', '_').replace('-', '_')}"
    df[col_name] = df["required_skills_norm"].str.contains(skill, na=False).astype(int)

# (f) Experience numeric order (for sorting in charts)
exp_order = {"Entry": 1, "Mid": 2, "Senior": 3, "Lead": 4, "Principal": 5}
df["experience_order"] = df["experience_level"].map(exp_order)

# ── STEP 7: Remove salary outliers (IQR method) ──────────────────────────────
Q1 = df["salary_usd"].quantile(0.25)
Q3 = df["salary_usd"].quantile(0.75)
IQR = Q3 - Q1
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

before = len(df)
df = df[(df["salary_usd"] >= lower_fence) & (df["salary_usd"] <= upper_fence)]
print(f"  Outliers removed (salary): {before - len(df)}")

# ── STEP 8: Final check & save ───────────────────────────────────────────────
df.reset_index(drop=True, inplace=True)
print(f"\n✅ Cleaned shape: {df.shape}")
print(df.dtypes)

os.makedirs("data/cleaned", exist_ok=True)
out_path = os.path.join("data", "cleaned", "ai_jobs_cleaned.csv")
df.to_csv(out_path, index=False)
print(f"\n✅ Cleaned data saved → {out_path}")

# ── STEP 9: Export specialised CSV slices for Power BI ───────────────────────
# (A) Skills explosion table – one skill per row (for skill frequency analysis)
skills_rows = []
for _, row in df.iterrows():
    for skill in str(row["required_skills"]).split(","):
        skill = skill.strip().title()
        if skill:
            skills_rows.append({
                "job_id":           row["job_id"],
                "job_title":        row["job_title"],
                "experience_level": row["experience_level"],
                "region":           row["region"],
                "salary_usd":       row["salary_usd"],
                "skill":            skill,
                "post_year":        row["post_year"],
            })

df_skills = pd.DataFrame(skills_rows)
df_skills.to_csv(os.path.join("data", "cleaned", "ai_skills_exploded.csv"), index=False)
print("✅ Skills exploded table saved → data/cleaned/ai_skills_exploded.csv")

# (B) Salary summary by experience + job title
salary_summary = (
    df.groupby(["experience_level", "job_title", "post_year"])["salary_usd"]
      .agg(["mean", "median", "min", "max", "count"])
      .rename(columns={"mean":"avg_salary", "median":"median_salary",
                       "min":"min_salary",  "max":"max_salary",
                       "count":"job_count"})
      .reset_index()
)
salary_summary.to_csv(os.path.join("data", "cleaned", "salary_summary.csv"), index=False)
print("✅ Salary summary saved → data/cleaned/salary_summary.csv")

# (C) Remote work distribution
remote_dist = (
    df.groupby(["work_mode", "post_year", "industry"])
      .size()
      .reset_index(name="job_count")
)
remote_dist.to_csv(os.path.join("data", "cleaned", "remote_distribution.csv"), index=False)
print("✅ Remote distribution saved → data/cleaned/remote_distribution.csv")

print("\n🎉 All cleaning & export complete!")
