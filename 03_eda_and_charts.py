"""
===========================================================
  SCRIPT 3: Exploratory Data Analysis (EDA) & Charts
===========================================================
PURPOSE:
  Loads the cleaned dataset and produces 10 high-quality
  Matplotlib/Seaborn charts that answer key business questions
  about the AI job market.

CHARTS GENERATED:
  1.  Top 15 AI Skills Demand (horizontal bar)
  2.  Average Salary by Experience Level (bar)
  3.  Remote vs Hybrid vs Onsite Distribution (donut)
  4.  Job Postings Trend Over Time (line)
  5.  Salary Distribution by Job Title (box plot)
  6.  Top 10 Hiring Companies (bar)
  7.  Job Count by Industry (horizontal bar)
  8.  Salary Heatmap: Experience × Job Title (heatmap)
  9.  Applications vs Salary (scatter)
  10. Skill Count vs Salary (scatter + regression)

HOW TO RUN:
  python scripts/03_eda_and_charts.py

OUTPUT:
  charts/  (10 PNG files)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ── Aesthetic settings ────────────────────────────────────────────────────────
PALETTE = "viridis"
BG      = "#0F1117"   # dark background (matches Power BI dark theme)
FG      = "#FFFFFF"
ACCENT  = "#7C5CBF"   # purple accent
GRID    = "#2A2A3E"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   FG,
    "xtick.color":       FG,
    "ytick.color":       FG,
    "text.color":        FG,
    "grid.color":        GRID,
    "legend.facecolor":  BG,
    "legend.edgecolor":  GRID,
    "font.family":       "DejaVu Sans",
})

# ── Load data ─────────────────────────────────────────────────────────────────
df       = pd.read_csv(os.path.join("data", "cleaned", "ai_jobs_cleaned.csv"))
df_skills = pd.read_csv(os.path.join("data", "cleaned", "ai_skills_exploded.csv"))

os.makedirs("charts", exist_ok=True)

def save(fig, name: str):
    path = os.path.join("charts", name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✅ Saved: {path}")

print("Generating charts …\n")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 1 — Top 15 AI Skills in Demand
# ───────────────────────────────────────────────────────────────────────────────
top_skills = (
    df_skills["skill"]
    .value_counts()
    .head(15)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 7))
colors = sns.color_palette("viridis", len(top_skills))
bars = ax.barh(top_skills.index, top_skills.values, color=colors, edgecolor=BG, linewidth=0.5)

for bar, val in zip(bars, top_skills.values):
    ax.text(val + 5, bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va="center", fontsize=9, color=FG)

ax.set_xlabel("Number of Job Postings", labelpad=10)
ax.set_title("🔧 Top 15 In-Demand AI Skills", fontsize=14, fontweight="bold", pad=15)
ax.grid(axis="x", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "01_top_skills.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 2 — Average Salary by Experience Level
# ───────────────────────────────────────────────────────────────────────────────
exp_order = ["Entry", "Mid", "Senior", "Lead", "Principal"]
sal_exp = (
    df.groupby("experience_level")["salary_usd"]
      .mean()
      .reindex(exp_order)
      .dropna()
)

fig, ax = plt.subplots(figsize=(9, 5))
colors2 = sns.color_palette("plasma", len(sal_exp))
bars2 = ax.bar(sal_exp.index, sal_exp.values, color=colors2,
               edgecolor=BG, linewidth=0.5, width=0.6)

for bar, val in zip(bars2, sal_exp.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1500,
            f"${val:,.0f}", ha="center", fontsize=10, fontweight="bold", color=FG)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax.set_title("💰 Average Salary by Experience Level", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Experience Level", labelpad=10)
ax.set_ylabel("Average Salary (USD)", labelpad=10)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "02_salary_by_experience.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 3 — Work Mode Distribution (Donut)
# ───────────────────────────────────────────────────────────────────────────────
wm_counts = df["work_mode"].value_counts()
donut_colors = ["#7C5CBF", "#00C9A7", "#F7971E"]

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    wm_counts.values,
    labels=wm_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=donut_colors[:len(wm_counts)],
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    textprops={"color": FG, "fontsize": 12},
)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")

ax.set_title("🌍 Remote vs Hybrid vs Onsite Distribution", fontsize=14,
             fontweight="bold", pad=20)
fig.tight_layout()
save(fig, "03_work_mode_donut.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 4 — Job Postings Trend Over Time (Monthly)
# ───────────────────────────────────────────────────────────────────────────────
df["job_posted_date"] = pd.to_datetime(df["job_posted_date"], errors="coerce")
monthly = (
    df.set_index("job_posted_date")
      .resample("ME")["job_id"]
      .count()
      .reset_index()
)
monthly.columns = ["month", "count"]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["month"], monthly["count"], color="#00C9A7", linewidth=2.5, marker="o",
        markersize=4, markerfacecolor="#00C9A7", markeredgecolor=BG)
ax.fill_between(monthly["month"], monthly["count"], alpha=0.15, color="#00C9A7")

ax.set_title("📈 AI Job Postings Trend Over Time", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Month", labelpad=10)
ax.set_ylabel("Number of Postings", labelpad=10)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.autofmt_xdate(rotation=30)
fig.tight_layout()
save(fig, "04_postings_trend.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 5 — Salary Distribution by Top Job Titles (Box Plot)
# ───────────────────────────────────────────────────────────────────────────────
top_titles = df["job_title"].value_counts().head(8).index.tolist()
df_box = df[df["job_title"].isin(top_titles)]

fig, ax = plt.subplots(figsize=(14, 6))
bp = ax.boxplot(
    [df_box[df_box["job_title"] == t]["salary_usd"].dropna() for t in top_titles],
    labels=[t.replace(" Engineer", "\nEngineer").replace(" Scientist", "\nScientist") for t in top_titles],
    patch_artist=True,
    medianprops=dict(color="#F7971E", linewidth=2),
    whiskerprops=dict(color=FG),
    capprops=dict(color=FG),
    flierprops=dict(marker="o", markerfacecolor=ACCENT, markersize=3, alpha=0.5),
)
box_colors = sns.color_palette("viridis", len(top_titles))
for patch, color in zip(bp["boxes"], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax.set_title("📊 Salary Distribution by Top Job Titles", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Salary (USD)", labelpad=10)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "05_salary_boxplot.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 6 — Top 10 Hiring Companies
# ───────────────────────────────────────────────────────────────────────────────
top_companies = df["company"].value_counts().head(10).sort_values()

fig, ax = plt.subplots(figsize=(10, 6))
colors6 = sns.color_palette("magma", len(top_companies))
bars6 = ax.barh(top_companies.index, top_companies.values, color=colors6,
                edgecolor=BG, linewidth=0.5)
for bar, val in zip(bars6, top_companies.values):
    ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=10, color=FG)

ax.set_title("🏢 Top 10 Hiring Companies in AI", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Number of Job Postings", labelpad=10)
ax.grid(axis="x", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "06_top_companies.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 7 — Job Count by Industry
# ───────────────────────────────────────────────────────────────────────────────
ind_counts = df["industry"].value_counts().sort_values()

fig, ax = plt.subplots(figsize=(10, 6))
colors7 = sns.color_palette("crest", len(ind_counts))
bars7 = ax.barh(ind_counts.index, ind_counts.values, color=colors7,
                edgecolor=BG, linewidth=0.5)
for bar, val in zip(bars7, ind_counts.values):
    ax.text(val + 2, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=9, color=FG)

ax.set_title("🏭 AI Job Count by Industry", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Number of Job Postings", labelpad=10)
ax.grid(axis="x", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "07_jobs_by_industry.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 8 — Salary Heatmap: Experience × Job Title
# ───────────────────────────────────────────────────────────────────────────────
top8_titles = df["job_title"].value_counts().head(8).index.tolist()
hm_data = (
    df[df["job_title"].isin(top8_titles)]
    .groupby(["experience_level", "job_title"])["salary_usd"]
    .mean()
    .unstack("job_title")
    .reindex(exp_order)
    .fillna(0)
)

short_labels = {t: t.replace("Machine Learning", "ML").replace("Engineer", "Eng.")
                     .replace("Scientist", "Sci.")
                     .replace("Computer Vision", "CV")
                for t in top8_titles}
hm_data.columns = [short_labels.get(c, c) for c in hm_data.columns]

fig, ax = plt.subplots(figsize=(13, 5))
sns.heatmap(
    hm_data / 1000, ax=ax,
    cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5,
    linecolor=BG, cbar_kws={"label": "Avg Salary ($K)"},
    annot_kws={"size": 9, "color": "black"},
)
ax.set_title("🌡️  Average Salary Heatmap (Experience × Job Title)", fontsize=13,
             fontweight="bold", pad=15)
ax.set_xlabel("")
ax.set_ylabel("Experience Level", labelpad=10)
fig.tight_layout()
save(fig, "08_salary_heatmap.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 9 — Applications vs Salary (scatter)
# ───────────────────────────────────────────────────────────────────────────────
work_mode_map = {"Onsite": "#F7971E", "Remote": "#00C9A7", "Hybrid": "#7C5CBF"}
df["wm_color"] = df["work_mode"].map(work_mode_map).fillna(FG)

fig, ax = plt.subplots(figsize=(10, 6))
for mode, color in work_mode_map.items():
    sub = df[df["work_mode"] == mode]
    ax.scatter(sub["applications"], sub["salary_usd"] / 1000,
               c=color, s=15, alpha=0.5, label=mode)

ax.set_title("📬 Applications vs Salary by Work Mode", fontsize=14,
             fontweight="bold", pad=15)
ax.set_xlabel("Number of Applications", labelpad=10)
ax.set_ylabel("Salary ($K)", labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.legend(title="Work Mode", framealpha=0.3)
ax.grid(alpha=0.2)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "09_applications_vs_salary.png")

# ───────────────────────────────────────────────────────────────────────────────
# CHART 10 — Skill Count vs Salary (scatter + trend line)
# ───────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(df["skill_count"], df["salary_usd"] / 1000,
           c=ACCENT, s=20, alpha=0.3, edgecolors="none")

# Fit a simple linear trend
z = np.polyfit(df["skill_count"].dropna(), df[df["skill_count"].notna()]["salary_usd"] / 1000, 1)
p = np.poly1d(z)
x_line = np.linspace(df["skill_count"].min(), df["skill_count"].max(), 100)
ax.plot(x_line, p(x_line), color="#F7971E", linewidth=2.5, label="Trend Line")

ax.set_title("🧪 Skills Count vs Salary (with Trend)", fontsize=14,
             fontweight="bold", pad=15)
ax.set_xlabel("Number of Required Skills", labelpad=10)
ax.set_ylabel("Salary ($K)", labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.legend(framealpha=0.3)
ax.grid(alpha=0.2)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "10_skills_vs_salary.png")

# ── Summary statistics printed to console ────────────────────────────────────
print("\n" + "═"*55)
print("  📋  KEY STATISTICS SUMMARY")
print("═"*55)
print(f"  Total Job Postings  : {len(df):,}")
print(f"  Unique Companies    : {df['company'].nunique()}")
print(f"  Unique Job Titles   : {df['job_title'].nunique()}")
print(f"  Avg Salary (USD)    : ${df['salary_usd'].mean():,.0f}")
print(f"  Median Salary (USD) : ${df['salary_usd'].median():,.0f}")
print(f"  Remote Jobs %       : {(df['work_mode']=='Remote').mean()*100:.1f}%")
print(f"  Most Common Title   : {df['job_title'].mode()[0]}")
print(f"  Highest Avg Salary  : {df.groupby('experience_level')['salary_usd'].mean().idxmax()} Level")
print("═"*55)
print("\n🎉 All 10 charts generated and saved to /charts folder!")
