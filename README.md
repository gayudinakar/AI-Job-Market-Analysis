# 🤖 AI Job Market Analysis Dashboard

> **A complete end-to-end data analytics project** using Python, Pandas, Matplotlib/Seaborn, and Power BI to analyse in-demand AI skills, salary trends, remote-work patterns, and experience-level distributions across 2,000+ AI job postings.

---

## 📁 Project Structure

```
job analysis/
│
├── data/
│   ├── raw/
│   │   └── ai_jobs_raw.csv          ← Generated synthetic dataset (2,020 rows)
│   └── cleaned/
│       ├── ai_jobs_cleaned.csv      ← Main cleaned fact table (1,981 rows × 34 cols)
│       ├── ai_skills_exploded.csv   ← One skill per row (for skill freq analysis)
│       ├── salary_summary.csv       ← Salary by experience + title + year
│       ├── remote_distribution.csv  ← Work mode by industry + year
│       ├── kpi_summary.csv          ← All KPI metrics in one table
│       ├── yearly_trends.csv        ← Year-over-year trend data
│       ├── region_summary.csv       ← Salary & job count by region
│       ├── experience_summary.csv   ← Experience level breakdown
│       └── top_skills_freq.csv      ← Top 20 skills with frequency
│
├── scripts/
│   ├── 01_generate_dataset.py  ← Creates the synthetic AI jobs dataset
│   ├── 02_data_cleaning.py     ← Cleans, preprocesses & engineers features
│   ├── 03_eda_and_charts.py    ← EDA + 10 Matplotlib/Seaborn charts
│   ├── 04_kpi_export.py        ← Computes KPIs & exports Power BI CSVs
│   └── 05_run_all.py           ← 🚀 Runs all scripts in sequence
│
├── charts/
│   ├── 01_top_skills.png
│   ├── 02_salary_by_experience.png
│   ├── 03_work_mode_donut.png
│   ├── 04_postings_trend.png
│   ├── 05_salary_boxplot.png
│   ├── 06_top_companies.png
│   ├── 07_jobs_by_industry.png
│   ├── 08_salary_heatmap.png
│   ├── 09_applications_vs_salary.png
│   └── 10_skills_vs_salary.png
│
├── powerbi/
│   ├── dark_theme.json          ← Power BI dark theme file
│   └── powerbi_setup_guide.py  ← DAX measures + dashboard layout guide
│
├── requirements.txt
└── README.md                    ← You are here!
```

---

## 🚀 Quick Start (Run Everything in One Command)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full pipeline (generates data → cleans → charts → KPIs)
python scripts/05_run_all.py
```

---

## 📋 Step-by-Step Walkthrough (Beginner Friendly)

### Step 1 — Generate the Dataset (`01_generate_dataset.py`)

**What it does:**  
Creates a *synthetic but realistic* dataset of 2,000 AI job postings from companies like Google, OpenAI, DeepMind etc., across locations worldwide.

**Key concepts:**
- `numpy.random.seed(42)` → Makes random numbers reproducible. Same seed = same data every run.
- `np.random.choice()` → Picks random items from a list (like rolling a dice with custom odds).
- `pd.DataFrame()` → Converts Python dictionaries into a table (rows + columns).
- `df.to_csv()` → Saves the table to a CSV file.

**Intentional data issues introduced (for realism):**
- ~5% missing salary values
- ~1.5% missing locations
- 20 duplicate rows

---

### Step 2 — Data Cleaning (`02_data_cleaning.py`)

**What it does:**  
Fixes all quality issues and enriches the data with new calculated columns.

| Problem | Solution |
|---|---|
| Duplicate rows | `df.drop_duplicates()` |
| Missing salaries | Fill with *median* salary per experience level |
| Missing locations | Fill with the most common (mode) location |
| Inconsistent capitalisation | `.str.strip().str.title()` |
| Wrong data types | `pd.to_datetime()`, `.astype(float)` etc. |
| Salary outliers | IQR method (remove values > Q3 + 1.5×IQR) |

**New columns created (Feature Engineering):**

| Column | What it means |
|---|---|
| `post_year` | Year the job was posted |
| `post_quarter` | Q1 / Q2 / Q3 / Q4 |
| `region` | USA, UK, Remote, etc. |
| `salary_band` | Salary bucket e.g. `$80K–$110K` |
| `skill_count` | How many skills are required |
| `skill_python`, `skill_aws`, … | 1/0 flags for top skills |

---

### Step 3 — EDA & Charts (`03_eda_and_charts.py`)

**What it does:**  
Answers 10 key business questions with professional dark-themed charts.

| Chart | Business Question Answered |
|---|---|
| 01 Top Skills | Which AI skills are most in demand? |
| 02 Salary by Experience | How much more do seniors earn vs. entry level? |
| 03 Work Mode Donut | What % of AI jobs are remote / hybrid / onsite? |
| 04 Postings Trend | Is the AI job market growing? |
| 05 Salary Box Plot | Which roles have the highest / widest salary ranges? |
| 06 Top Companies | Who is hiring the most AI talent? |
| 07 Jobs by Industry | Which industries need AI workers most? |
| 08 Salary Heatmap | Where do salaries intersect with experience and role? |
| 09 Applications vs Salary | Do high-paying remote jobs attract more applicants? |
| 10 Skills vs Salary | Does having more skills lead to higher pay? |

---

### Step 4 — KPI Export (`04_kpi_export.py`)

**What it does:**  
Computes summary statistics and saves specialised CSVs tailored for Power BI visuals.

**KPIs computed:**
- Total job postings, unique companies, unique titles
- Average & median salary
- % Remote / Hybrid / Onsite
- % Visa sponsored
- Top job title, top skill, top company
- Yearly trends, regional breakdowns

---

## 📊 Power BI Dashboard Setup

### Import these CSV files:

| File | Use in Power BI as |
|---|---|
| `ai_jobs_cleaned.csv` | Main fact table (central table) |
| `ai_skills_exploded.csv` | Skills dimension table |
| `kpi_summary.csv` | KPI card data source |
| `salary_summary.csv` | Salary charts |
| `yearly_trends.csv` | Trend line charts |
| `region_summary.csv` | Map / regional charts |
| `top_skills_freq.csv` | Skill bar chart |

### Apply the Dark Theme:
1. Open Power BI Desktop
2. Go to **View → Themes → Browse for themes**
3. Select `powerbi/dark_theme.json`

### DAX Measures (copy from `powerbi_setup_guide.py`):
- `Total Jobs`, `Avg Salary USD`, `Median Salary USD`
- `Pct Remote`, `Pct Hybrid`, `Pct Onsite`
- `Salary Growth YoY`, `Top Skill`, `Top Paying Role`

### Recommended 5-Page Layout:

| Page | Contents |
|---|---|
| **1. Executive Overview** | KPI cards, top titles, work mode donut, trend line, slicers |
| **2. Salary Analysis** | Bar chart, box plot, heatmap, YoY trend table |
| **3. Skills Intelligence** | Top 15 skills bar, treemap, skill vs salary scatter |
| **4. Remote & Geography** | Work mode split, region bar, remote trend over time |
| **5. Company & Industry** | Top companies, industry treemap, applications scatter |

---

## 📈 Key Findings from the Data

| Metric | Value |
|---|---|
| Total AI Job Postings | **1,981** |
| Average Salary | **\$138,859** |
| Median Salary | **\$134,058** |
| Remote Jobs | **30.6%** |
| Hybrid Jobs | **35.4%** |
| Most Common Role | **Machine Learning Engineer** |
| Most In-Demand Skill | **Python / LLMs** |
| Highest Paid Level | **Principal** |
| Visa Sponsorship Rate | **~30%** |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.12** | Core programming language |
| **Pandas** | Data loading, cleaning, transformation |
| **NumPy** | Numerical operations, random data generation |
| **Matplotlib** | Base chart rendering engine |
| **Seaborn** | Statistical visualisations (heatmap, boxplot) |
| **Power BI Desktop** | Interactive dashboard & KPI cards |

---

## 📦 Requirements

```
pandas==2.2.2
numpy==1.26.4
matplotlib==3.9.0
seaborn==0.13.2
scikit-learn==1.4.2
openpyxl==3.1.2
plotly==5.22.0
kaleido==0.2.1
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🎓 Learning Outcomes

After working through this project you will understand:

- ✅ How to generate and work with realistic tabular datasets
- ✅ The full data cleaning pipeline (duplicates → nulls → outliers → types)
- ✅ Feature engineering techniques (binning, extraction, one-hot flags)
- ✅ How to create publication-quality charts with Matplotlib/Seaborn
- ✅ How to structure data exports for Power BI
- ✅ How to write DAX measures for KPI cards
- ✅ How to design a professional multi-page Power BI dashboard

---

*Built with ❤️ using Python + Power BI*
