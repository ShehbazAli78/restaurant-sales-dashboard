# 🍽️ Restaurant Sales & Customer Intelligence

End-to-end analytics project on 6,000 restaurant orders — from raw, messy
data to a cleaned dataset, exploratory analysis, a Power BI report, and an
interactive Streamlit dashboard.
## 🚀 Live Dashboard

[Click Here to View Live Dashboard](https://restaurant-sales-dashboard-av67g64wqlu94nxv3har5q.streamlit.app/)
## 🗂️ Project Structure

```
restaurant-sales-dashboard/
├── data/
│   ├── raw/                    # Original, uncleaned dataset
│   │   └── restaurant_data_dirty.csv
│   └── processed/              # Cleaned dataset used downstream
│       └── clean_data.csv
├── notebooks/
│   ├── 01_data_cleaning.ipynb  # Raw -> clean data pipeline
│   └── 02_eda.ipynb            # Exploratory data analysis
├── reports/
│   └── Restaurant_Analytics_Report.pdf   # Written analytics report
├── powerbi/
│   └── salesData.pbix          # Power BI dashboard
├── dashboard/                  # Streamlit web app
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md               # Dashboard-specific docs
│   ├── .streamlit/config.toml
│   ├── utils/
│   │   ├── data_loader.py
│   │   └── styling.py
│   └── data/clean_data.csv
├── requirements.txt             # Env for notebooks / full pipeline
├── LICENSE
└── README.md                    # You are here
```

## 🚀 Components

| Component | Description | Where |
|---|---|---|
| **Data cleaning** | Handles missing values, duplicates, type fixes | `notebooks/01_data_cleaning.ipynb` |
| **EDA** | Trends, distributions, correlations | `notebooks/02_eda.ipynb` |
| **Report** | Summary write-up of findings | `reports/Restaurant_Analytics_Report.pdf` |
| **Power BI dashboard** | Interactive `.pbix` report | `powerbi/salesData.pbix` |
| **Streamlit dashboard** | Live, filterable web app | `dashboard/` |

## 🛠️ Getting Started

### Streamlit dashboard

```bash
cd dashboard
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`. See `dashboard/README.md` for full details
(features, dataset schema, deployment).

### Notebooks (data cleaning / EDA)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/
```

### Power BI report

Open `powerbi/salesData.pbix` in [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
(Windows only).

## 📊 Dataset

`data/processed/clean_data.csv` — 6,000 restaurant order records:
`customer_id, gender, age, city, signup_date, order_id, order_date,
restaurant_name, dish_name, category, quantity, price, payment_method,
order_frequency, last_order_date, loyalty_points, churned, rating,
rating_date, delivery_status`.

## ☁️ Deploying the Dashboard

**Streamlit Community Cloud (free):**
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo
3. Set the main file path to `dashboard/app.py` and deploy

## 📄 License

MIT — free to use and adapt. See [LICENSE](LICENSE).
