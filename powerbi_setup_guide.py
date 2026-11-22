# Power BI Dashboard Setup Guide
# AI Job Market Analysis Dashboard
# ============================================================
# This file documents the Power BI measures (DAX formulas)
# and the step-by-step setup instructions.
# ============================================================

# ── HOW TO USE THIS FILE ─────────────────────────────────────
# 1. Open Power BI Desktop
# 2. Import the CSV files from  data/cleaned/
# 3. Create the relationships described below
# 4. Add the DAX measures listed below
# 5. Build the dashboard pages as described
# ─────────────────────────────────────────────────────────────


# ============================================================
# SECTION A: FILES TO IMPORT INTO POWER BI
# ============================================================

FILES_TO_IMPORT = [
    "data/cleaned/ai_jobs_cleaned.csv",       # Main fact table
    "data/cleaned/ai_skills_exploded.csv",    # Skills dimension
    "data/cleaned/kpi_summary.csv",           # KPI metrics table
    "data/cleaned/salary_summary.csv",        # Salary aggregations
    "data/cleaned/remote_distribution.csv",   # Work mode data
    "data/cleaned/yearly_trends.csv",         # Year-over-year trends
    "data/cleaned/region_summary.csv",        # Geographic data
    "data/cleaned/top_skills_freq.csv",       # Skill frequency
    "data/cleaned/experience_summary.csv",    # Experience analysis
]


# ============================================================
# SECTION B: TABLE RELATIONSHIPS IN POWER BI
# ============================================================
#
# ai_jobs_cleaned   ──(job_id)──>  ai_skills_exploded
#                   (one-to-many: one job can have many skills)
#
# ai_jobs_cleaned is the central FACT table.
# All other tables are SUMMARY / AGGREGATED tables
# that can be used independently for specific visuals.
#
# ============================================================


# ============================================================
# SECTION C: DAX MEASURES TO ADD IN POWER BI
# ============================================================
#
# After importing data, go to:
#   Home > New Measure  (or right-click a table > New Measure)
#
# Copy-paste each formula below:
# ============================================================

DAX_MEASURES = """
// ── KPI MEASURES ──────────────────────────────────────────

Total Jobs =
    COUNTROWS(ai_jobs_cleaned)

Avg Salary USD =
    AVERAGE(ai_jobs_cleaned[salary_usd])

Median Salary USD =
    MEDIAN(ai_jobs_cleaned[salary_usd])

Max Salary USD =
    MAX(ai_jobs_cleaned[salary_usd])

Pct Remote =
    DIVIDE(
        COUNTROWS(FILTER(ai_jobs_cleaned, ai_jobs_cleaned[work_mode] = "Remote")),
        COUNTROWS(ai_jobs_cleaned),
        0
    ) * 100

Pct Hybrid =
    DIVIDE(
        COUNTROWS(FILTER(ai_jobs_cleaned, ai_jobs_cleaned[work_mode] = "Hybrid")),
        COUNTROWS(ai_jobs_cleaned),
        0
    ) * 100

Pct Onsite =
    DIVIDE(
        COUNTROWS(FILTER(ai_jobs_cleaned, ai_jobs_cleaned[work_mode] = "Onsite")),
        COUNTROWS(ai_jobs_cleaned),
        0
    ) * 100

Avg Applications =
    AVERAGE(ai_jobs_cleaned[applications])

Pct Visa Sponsored =
    DIVIDE(
        COUNTROWS(FILTER(ai_jobs_cleaned, ai_jobs_cleaned[is_visa_sponsored] = TRUE())),
        COUNTROWS(ai_jobs_cleaned),
        0
    ) * 100

// ── SALARY MEASURES ────────────────────────────────────────

Salary Growth YoY =
    VAR CurrentYear =
        CALCULATE(AVERAGE(ai_jobs_cleaned[salary_usd]))
    VAR PreviousYear =
        CALCULATE(
            AVERAGE(ai_jobs_cleaned[salary_usd]),
            DATEADD(ai_jobs_cleaned[job_posted_date], -1, YEAR)
        )
    RETURN
        DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100

Top Paying Role =
    FIRSTNONBLANK(
        TOPN(1,
            SUMMARIZE(ai_jobs_cleaned, ai_jobs_cleaned[job_title],
                      "AvgSal", AVERAGE(ai_jobs_cleaned[salary_usd])),
            [AvgSal], DESC),
        1
    )

// ── SKILL MEASURES ─────────────────────────────────────────

Total Unique Skills =
    DISTINCTCOUNT(ai_skills_exploded[skill])

Top Skill =
    FIRSTNONBLANK(
        TOPN(1,
            SUMMARIZE(ai_skills_exploded, ai_skills_exploded[skill],
                      "Freq", COUNTROWS(ai_skills_exploded)),
            [Freq], DESC),
        1
    )

// ── JOB COUNT MEASURES ─────────────────────────────────────

Remote Jobs Count =
    COUNTROWS(FILTER(ai_jobs_cleaned, ai_jobs_cleaned[work_mode] = "Remote"))

Senior Jobs Count =
    COUNTROWS(FILTER(ai_jobs_cleaned, ai_jobs_cleaned[experience_level] = "Senior"))
"""


# ============================================================
# SECTION D: DASHBOARD PAGE LAYOUT GUIDE
# ============================================================

DASHBOARD_PAGES = {
    "Page 1 — Executive Overview": {
        "visuals": [
            "KPI Card: Total Jobs",
            "KPI Card: Avg Salary ($)",
            "KPI Card: % Remote",
            "KPI Card: Pct Visa Sponsored",
            "Bar Chart: Top 10 Job Titles by Count",
            "Donut Chart: Work Mode Distribution",
            "Line Chart: Monthly Job Postings Trend",
            "Slicer: Year | Experience Level | Work Mode",
        ],
        "theme": "Dark",
        "accent": "#7C5CBF",
    },

    "Page 2 — Salary Analysis": {
        "visuals": [
            "Clustered Bar: Avg Salary by Experience Level",
            "Box-and-Whisker: Salary Distribution by Job Title",
            "Heatmap Matrix: Salary by Experience × Title",
            "Line Chart: Avg Salary Trend by Year",
            "Table: Top 10 Highest Paying Roles (with avg salary)",
            "Slicer: Experience Level | Industry | Region",
        ],
        "theme": "Dark",
    },

    "Page 3 — Skills Intelligence": {
        "visuals": [
            "Horizontal Bar: Top 15 In-Demand Skills",
            "Treemap: Skills by Category",
            "Scatter: Skill Count vs Salary",
            "Bar: Skills by Experience Level (stacked)",
            "Table: Top Skills with Job Count and Avg Salary",
            "Slicer: Skill | Year | Experience Level",
        ],
        "theme": "Dark",
    },

    "Page 4 — Remote Work & Geography": {
        "visuals": [
            "Donut: Remote / Hybrid / Onsite split",
            "Stacked Bar: Work Mode by Industry",
            "Bar: Jobs by Region",
            "Line: Remote % Trend Over Time",
            "Table: Region Salary Comparison",
            "Slicer: Region | Year | Work Mode",
        ],
        "theme": "Dark",
    },

    "Page 5 — Company & Industry Intel": {
        "visuals": [
            "Bar: Top 10 Hiring Companies",
            "Treemap: Companies by Industry",
            "Bar: Jobs by Company Size",
            "Scatter: Applications vs Salary by Work Mode",
            "Bar: Visa Sponsorship by Company Size",
            "Slicer: Industry | Company Size | Year",
        ],
        "theme": "Dark",
    },
}


# ============================================================
# SECTION E: POWER BI THEME JSON (copy into theme file)
# ============================================================

POWER_BI_THEME_JSON = '''
{
  "name": "AI Dashboard Dark Theme",
  "dataColors": [
    "#7C5CBF", "#00C9A7", "#F7971E", "#FF6B6B",
    "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"
  ],
  "background": "#0F1117",
  "foreground": "#FFFFFF",
  "tableAccent": "#7C5CBF",
  "visualStyles": {
    "*": {
      "*": {
        "background": [{"color": {"solid": {"color": "#0F1117"}}}],
        "fontColor":  [{"color": {"solid": {"color": "#FFFFFF"}}}]
      }
    },
    "card": {
      "*": {
        "calloutValue": [{"fontSize": 28, "fontFamily": "Segoe UI Semibold"}],
        "label":        [{"fontSize": 11, "color": {"solid": {"color": "#AAAAAA"}}}]
      }
    }
  }
}
'''

print("Power BI setup guide loaded.")
print("Save the POWER_BI_THEME_JSON above as:  powerbi/dark_theme.json")
print("Then in Power BI: View > Themes > Browse for themes > select that file.")
