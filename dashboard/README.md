# 🍽️ Restaurant Customer Intelligence Dashboard

A production-ready, interactive Business Intelligence dashboard built with
**Streamlit**, **Pandas**, **Plotly**, and **Altair** — analyzing 6,000
restaurant orders across customers, restaurants, transactions, and ratings.

## ✨ Features

- **Global sidebar filters** (date range, city, restaurant, category, gender)
  that apply consistently across every tab
- **Top-line KPI bar** — revenue, orders, unique customers, AOV, avg rating
- **6 analytical tabs:**
  - 📊 **Overview** — revenue trend, category mix, top restaurants, orders by city
  - 👥 **Customers** — demographics, churn rate, loyalty, top spenders
  - 🏪 **Restaurants** — top dishes, category revenue heatmap, full revenue matrix
  - 📦 **Orders & Payments** — payment methods, delivery performance, order frequency
  - ⭐ **Ratings** — rating distribution, top-rated restaurants, rating trend
  - 🗂️ **Raw Data** — explore and export the filtered dataset as CSV
- Custom dark theme with a cohesive color palette, card-based layout, and
  auto-generated insight callouts
- Fully defensive data loading — handles missing/renamed columns gracefully

## 🗂️ Project Structure

```
dashboard/
├── app.py                  # Main dashboard application
├── requirements.txt
├── .streamlit/
│   └── config.toml          # Theme
├── utils/
│   ├── styling.py            # Global CSS + KPI/chart-card helpers
│   └── data_loader.py        # Cached, defensive CSV loading
└── data/
    └── clean_data.csv        # Restaurant order dataset (6,000 rows)
```

## 🛠️ Getting Started

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 📊 Dataset

`data/clean_data.csv` contains 6,000 restaurant order records with columns:
`customer_id, gender, age, city, signup_date, order_id, order_date,
restaurant_name, dish_name, category, quantity, price, payment_method,
order_frequency, last_order_date, loyalty_points, churned, rating,
rating_date, delivery_status`.

To use your own dataset, replace this file — as long as column names match
(or are close variants; see `utils/data_loader.py` for the alias mapping),
the dashboard will pick it up automatically.

## ☁️ Deploying

**Streamlit Community Cloud (free):**
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo
3. Set the main file to `app.py` and deploy

## 📄 License

MIT — free to use and adapt.
