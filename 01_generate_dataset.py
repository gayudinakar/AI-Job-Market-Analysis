"""
========================================================
  SCRIPT 1: Generate Synthetic AI Job Market Dataset
========================================================
PURPOSE:
  Creates a realistic, synthetic dataset of AI/ML job postings.
  We use numpy's random functions so the data is repeatable
  (same seed = same numbers every time you run it).

HOW TO RUN:
  python scripts/01_generate_dataset.py

OUTPUT:
  data/raw/ai_jobs_raw.csv
"""

import pandas as pd
import numpy as np
import os

# ── Fix the random seed so results are reproducible ──────────────────────────
np.random.seed(42)
N = 2000   # total number of job postings to simulate

# ── 1. Define the pools of realistic values ───────────────────────────────────
job_titles = [
    "Machine Learning Engineer", "Data Scientist", "AI Engineer",
    "NLP Engineer", "Computer Vision Engineer", "MLOps Engineer",
    "Data Analyst", "AI Research Scientist", "Deep Learning Engineer",
    "Prompt Engineer", "AI Product Manager", "Robotics Engineer",
    "AI Ethics Researcher", "Data Engineer", "Business Intelligence Analyst"
]

# Weights control how often each title appears (sum must equal 1 or be proportional)
title_weights = [0.14, 0.14, 0.12, 0.09, 0.09, 0.08, 0.08,
                 0.07, 0.07, 0.05, 0.03, 0.02, 0.01, 0.01, 0.00]

companies = [
    "Google", "Meta", "Microsoft", "Amazon", "Apple", "OpenAI",
    "DeepMind", "NVIDIA", "Tesla", "IBM", "Salesforce", "Adobe",
    "Databricks", "Hugging Face", "Anthropic", "Cohere", "Scale AI",
    "Palantir", "Snowflake", "Oracle", "SAP", "Intel", "AMD",
    "Qualcomm", "Samsung"
]

locations = [
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
    "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
    "Atlanta, GA", "Remote", "London, UK", "Toronto, Canada",
    "Berlin, Germany", "Singapore", "Bangalore, India"
]

location_weights = [0.14, 0.12, 0.10, 0.08, 0.07, 0.06, 0.06,
                    0.05, 0.04, 0.12, 0.05, 0.03, 0.03, 0.03, 0.02]

experience_levels = ["Entry", "Mid", "Senior", "Lead", "Principal"]
exp_weights       = [0.15, 0.30, 0.35, 0.13, 0.07]

employment_types = ["Full-Time", "Part-Time", "Contract", "Internship"]
emp_weights      = [0.75, 0.05, 0.15, 0.05]

work_modes = ["Onsite", "Remote", "Hybrid"]
work_weights = [0.35, 0.30, 0.35]

industries = [
    "Technology", "Finance", "Healthcare", "E-Commerce", "Automotive",
    "Education", "Government", "Media & Entertainment", "Cybersecurity"
]

company_sizes = ["Startup (<50)", "Small (50-200)", "Medium (200-1000)",
                 "Large (1000-5000)", "Enterprise (5000+)"]

education_levels = [
    "Bachelor's", "Master's", "PhD", "Associate's", "No Preference"
]

# ── 2. AI Skills (each job has a comma-separated skill list) ─────────────────
skill_pool = [
    "Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning",
    "NLP", "Computer Vision", "SQL", "Spark", "Kubernetes", "Docker",
    "AWS", "GCP", "Azure", "Statistics", "R", "Tableau", "Power BI",
    "LLMs", "Transformers", "Hugging Face", "MLflow", "Airflow",
    "Data Visualization", "A/B Testing", "Feature Engineering",
    "Reinforcement Learning", "OpenCV", "ONNX", "Scikit-Learn"
]

def pick_skills(n_skills: int = None) -> str:
    """Return a comma-separated string of randomly chosen skills."""
    k = n_skills or np.random.randint(3, 8)
    return ", ".join(np.random.choice(skill_pool, size=k, replace=False))

# ── 3. Salary logic (experience level influences the range) ──────────────────
salary_ranges = {
    "Entry":     (60_000,  95_000),
    "Mid":       (90_000, 130_000),
    "Senior":   (125_000, 180_000),
    "Lead":     (160_000, 220_000),
    "Principal":(200_000, 280_000),
}

def generate_salary(exp_level: str) -> int:
    lo, hi = salary_ranges[exp_level]
    return int(np.random.uniform(lo, hi))

# ── 4. Date range: job postings from 2022 to late 2024 ───────────────────────
date_range = pd.date_range(start="2022-01-01", end="2024-10-31", freq="D")

# ── 5. Build the dataset row by row ──────────────────────────────────────────
print(f"Generating {N} synthetic AI job postings …")

exp_col  = np.random.choice(experience_levels, size=N, p=exp_weights)
loc_col  = np.random.choice(locations,          size=N, p=location_weights)

data = {
    "job_id":           [f"JOB{str(i).zfill(5)}" for i in range(1, N + 1)],
    "job_title":        np.random.choice(job_titles, size=N, p=title_weights),
    "company":          np.random.choice(companies,  size=N),
    "location":         loc_col,
    "experience_level": exp_col,
    "employment_type":  np.random.choice(employment_types, size=N, p=emp_weights),
    "work_mode":        np.random.choice(work_modes,  size=N, p=work_weights),
    "industry":         np.random.choice(industries,  size=N),
    "company_size":     np.random.choice(company_sizes, size=N),
    "education_level":  np.random.choice(education_levels, size=N),
    "required_skills":  [pick_skills() for _ in range(N)],
    "salary_usd":       [generate_salary(e) for e in exp_col],
    "job_posted_date":  np.random.choice(date_range, size=N),
    "applications":     np.random.randint(5, 500, size=N),
    "is_visa_sponsored": np.random.choice([True, False], size=N, p=[0.3, 0.7]),
}

df = pd.DataFrame(data)
df["job_posted_date"] = pd.to_datetime(df["job_posted_date"]).dt.strftime("%Y-%m-%d")

# ── 6. Inject ≈ 5 % noise / missing values to make cleaning realistic ─────────
noise_idx = np.random.choice(df.index, size=int(N * 0.05), replace=False)
df.loc[noise_idx, "salary_usd"]       = np.nan
df.loc[noise_idx[:30], "location"]    = None
df.loc[noise_idx[30:60], "education_level"] = None

# Add a few duplicate rows
dup_idx = np.random.choice(df.index, size=20, replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# Save
os.makedirs("data/raw", exist_ok=True)
out_path = os.path.join("data", "raw", "ai_jobs_raw.csv")
df.to_csv(out_path, index=False)

print(f"✅ Dataset saved → {out_path}")
print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"   Nulls:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
