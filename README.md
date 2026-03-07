# Nassau Candy Profitability Analysis Dashboard 📈

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jasmin-analytics.streamlit.app/)

An interactive Business Intelligence (BI) dashboard built to analyze product line profitability and margin performance for **Nassau Candy Distributor**. This project transforms raw transactional data into actionable strategic insights.

## ✨ Key Features

- **Profitability Overview**: High-level metrics (Sales, Profit, Margin) across all divisions.
- **Pareto Analysis (80/20 Rule)**: Automated identification of the top 20% products driving 80% of total profit.
- **Temporal Trends**: Time-series analysis with dual-axis charts to monitor margin stability over time.
- **Geospatial Insights**: Regional profitability breakdown with interactive state-level analysis.
- **Customer Segmentation**: Profiling of top-performing customer accounts and average profit per user.
- **Forecast Engine**: 6-month sales and profit projections using Holt-Winters Exponential Smoothing.
- **"What-If" Scenario Planner**: Interactive simulation tool for modeling the impact of price and cost changes.
- **Automated Reporting**: One-click generation of comprehensive Excel reports.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Visuals**: [Plotly Express](https://plotly.com/python/plotly-express/) & Graph Objects
- **Analysis**: Pandas, NumPy, Statsmodels (Holt-Winters)
- **Reporting**: XlsxWriter
- **CI/CD**: Streamlit Cloud

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/jasmin882005/nassau-profitability-analysis.git
cd nassau-profitability-analysis
```

### 2. Set up environment
```bash
pip install -r requirements.txt
```

### 3. Run the application
**On Windows:**
```bash
.\run_app.bat
```
**Manual command:**
```bash
streamlit run app/app.py
```

## 📂 Project Structure

```text
├── analysis/              # Core logic & analytical engines
│   ├── forecasting.py      # Time-series forecasting
│   ├── insights.py         # Data aggregation & KPIs
│   ├── scenario.py         # What-if simulation logic
│   └── report_generator.py # Automated report generation
├── app/                   # Streamlit UI implementation
│   └── app.py              # Main dashboard script
├── data/                  # Source datasets (CSV)
├── research-paper/        # Academic report & static figures
│   ├── research_paper.md   # Detailed internship report
│   └── figures/            # Exported charts for the paper
├── requirements.txt       # Project dependencies
└── run_app.bat            # Windows startup script
```

## 📝 Research & Findings

A comprehensive research paper detailing the project's methodology, findings, and strategic recommendations is available in the [research-paper/](research-paper/research_paper.md) directory.

**Key Insight**: The analysis revealed that just **26.7%** of the product portfolio generates **80%** of the company's total gross profit, primarily driven by the 'Chocolate' division.

---
**Author**: [Jasmin Jamadar](https://github.com/jasmin882005)
**Department**: Data Analyst Intern
**Organization**: Nassau Candy Distributor
