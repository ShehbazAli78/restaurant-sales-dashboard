

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import streamlit as st

from utils.data_loader import load_data, has_columns
from utils.styling import (
    inject_global_css,
    section_header,
    soft_divider,
    kpi_card,
    chart_card_start,
    chart_card_end,
)

st.set_page_config(
    page_title="Restaurant Customer Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()

PALETTE = ["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E", "#55EFC4", "#74B9FF", "#E17055"]


def money(x: float) -> str:
    return f"${x:,.0f}" if pd.notna(x) else "—"


# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
df = load_data()

if df.empty:
    st.error("⚠️ Could not find `data/clean_data.csv`. Make sure the file exists in the `data/` folder.")
    st.stop()

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
header_l, header_r = st.columns([3, 1])
with header_l:
    st.markdown("# 🍽️ <span class='gradient-text'>Restaurant Customer Intelligence</span>", unsafe_allow_html=True)
    st.caption(
        "A business intelligence view of customer behavior, restaurant performance, "
        "order trends, and satisfaction — updated live from the underlying dataset."
    )
with header_r:
    st.write("")
    if has_columns(df, ["order_date"]) and df["order_date"].notna().any():
        st.metric("Data as of", df["order_date"].max().strftime("%b %d, %Y"))

soft_divider()

# ------------------------------------------------------------------
# Sidebar — global filters
# ------------------------------------------------------------------
st.sidebar.markdown("## 🔎 Filters")
st.sidebar.caption("Filters apply across every tab in the dashboard.")

filtered = df.copy()

if has_columns(df, ["order_date"]) and df["order_date"].notna().any():
    min_d, max_d = df["order_date"].min().date(), df["order_date"].max().date()
    date_range = st.sidebar.date_input(
        "Order date range", value=(min_d, max_d), min_value=min_d, max_value=max_d
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["order_date"].dt.date >= start) & (filtered["order_date"].dt.date <= end)
        ]

if "city" in df.columns:
    cities = st.sidebar.multiselect("City", sorted(df["city"].dropna().unique()), default=[])
    if cities:
        filtered = filtered[filtered["city"].isin(cities)]

if "restaurant_name" in df.columns:
    restaurants = st.sidebar.multiselect("Restaurant", sorted(df["restaurant_name"].dropna().unique()), default=[])
    if restaurants:
        filtered = filtered[filtered["restaurant_name"].isin(restaurants)]

if "category" in df.columns:
    categories = st.sidebar.multiselect("Category", sorted(df["category"].dropna().unique()), default=[])
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

if "gender" in df.columns:
    genders = st.sidebar.multiselect("Gender", sorted(df["gender"].dropna().unique()), default=[])
    if genders:
        filtered = filtered[filtered["gender"].isin(genders)]

st.sidebar.divider()
st.sidebar.caption(f"Showing **{len(filtered):,}** of **{len(df):,}** total order records.")
if st.sidebar.button("↺ Reset all filters", width="stretch"):
    st.rerun()

if filtered.empty:
    st.warning("No records match the selected filters. Try widening your selection.")
    st.stop()

# ------------------------------------------------------------------
# Top-line KPIs (always visible, above the tabs)
# ------------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    kpi_card("Total Revenue", money(filtered["price"].sum()), "💰")
with k2:
    kpi_card("Total Orders", f"{filtered['order_id'].nunique():,}", "📦")
with k3:
    kpi_card("Unique Customers", f"{filtered['customer_id'].nunique():,}", "👥")
with k4:
    kpi_card("Avg Order Value", money(filtered["price"].mean()), "📊")
with k5:
    if "rating" in filtered.columns:
        kpi_card("Avg Rating", f"{filtered['rating'].mean():.2f} / 5", "⭐")
    else:
        kpi_card("Avg Rating", "—", "⭐")

soft_divider()

# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tab_overview, tab_customers, tab_restaurants, tab_orders, tab_ratings, tab_data = st.tabs(
    ["📊 Overview", "👥 Customers", "🏪 Restaurants", "📦 Orders & Payments", "⭐ Ratings", "🗂️ Raw Data"]
)

# ============================================================
# OVERVIEW
# ============================================================
with tab_overview:
    section_header("Performance", "Revenue & Order Trends")
    c1, c2 = st.columns([2, 1])

    with c1:
        chart_card_start("Revenue Over Time")
        if has_columns(filtered, ["order_date"]) and filtered["order_date"].notna().any():
            trend = (
                filtered.dropna(subset=["order_date"])
                .groupby(filtered["order_date"].dt.to_period("M"))["price"]
                .sum()
                .reset_index()
            )
            trend["order_date"] = trend["order_date"].dt.to_timestamp()
            fig = px.area(trend, x="order_date", y="price", color_discrete_sequence=[PALETTE[0]])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0), height=320,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="", yaxis_title="Revenue ($)",
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Order date not available.")
        chart_card_end()

    with c2:
        chart_card_start("Revenue by Category")
        cat_rev = filtered.groupby("category", as_index=False)["price"].sum().sort_values("price", ascending=False)
        fig = px.pie(cat_rev, values="price", names="category", hole=0.55, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent", textfont_size=11)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=320, showlegend=True,
                           paper_bgcolor="rgba(0,0,0,0)", legend=dict(font=dict(size=10)))
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    c3, c4 = st.columns(2)
    with c3:
        chart_card_start("Top 10 Restaurants by Revenue")
        top_rest = (
            filtered.groupby("restaurant_name", as_index=False)["price"]
            .sum()
            .sort_values("price", ascending=False)
            .head(10)
        )
        chart = (
            alt.Chart(top_rest)
            .mark_bar(color="#6C5CE7", cornerRadiusEnd=4)
            .encode(
                x=alt.X("price:Q", title="Revenue ($)"),
                y=alt.Y("restaurant_name:N", sort="-x", title=""),
                tooltip=["restaurant_name", "price"],
            )
            .properties(height=320)
        )
        st.altair_chart(chart, width="stretch")
        chart_card_end()

    with c4:
        chart_card_start("Orders by City")
        city_orders = filtered.groupby("city", as_index=False)["order_id"].nunique().sort_values(
            "order_id", ascending=False
        )
        fig = px.bar(city_orders, x="city", y="order_id", color_discrete_sequence=[PALETTE[1]])
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0), height=320,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="", yaxis_title="Orders",
        )
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    top_restaurant_name = top_rest.iloc[0]["restaurant_name"] if not top_rest.empty else "N/A"
    st.markdown(
        f"<div class='insight-box'>💡 <b>{top_restaurant_name}</b> generated the highest revenue in the "
        f"selected period, and the busiest city by order volume is "
        f"<b>{city_orders.iloc[0]['city'] if not city_orders.empty else 'N/A'}</b>.</div>",
        unsafe_allow_html=True,
    )

# ============================================================
# CUSTOMERS
# ============================================================
with tab_customers:
    section_header("Audience", "Customer Demographics & Engagement")

    churn_flags = filtered["churned"].astype(str).str.lower()
    churn_rate = churn_flags.isin(["inactive", "churned", "yes", "true", "1"]).mean() * 100

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Avg Loyalty Points", f"{filtered['loyalty_points'].mean():.0f}", "🎖️")
    with c2:
        kpi_card("Churn Rate", f"{churn_rate:.1f}%", "📉")
    with c3:
        kpi_card("Avg Orders / Customer", f"{filtered.groupby('customer_id')['order_id'].nunique().mean():.1f}", "🔁")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        chart_card_start("Age Group Distribution")
        if pd.api.types.is_numeric_dtype(filtered["age"]):
            fig = px.histogram(filtered, x="age", nbins=20, color_discrete_sequence=[PALETTE[0]])
        else:
            counts = filtered["age"].value_counts().reset_index()
            counts.columns = ["age_group", "count"]
            fig = px.bar(counts, x="age_group", y="count", color_discrete_sequence=[PALETTE[0]])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    with c2:
        chart_card_start("Gender Split")
        gcounts = filtered.groupby("gender")["customer_id"].nunique().reset_index()
        fig = px.pie(gcounts, values="customer_id", names="gender", hole=0.55, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    soft_divider()
    section_header("Loyalty", "Top Customers")
    top_customers = (
        filtered.groupby("customer_id")
        .agg(orders=("order_id", "nunique"), total_spent=("price", "sum"), loyalty_points=("loyalty_points", "max"))
        .sort_values("total_spent", ascending=False)
        .head(10)
        .reset_index()
    )
    top_customers["total_spent"] = top_customers["total_spent"].map(money)
    st.dataframe(top_customers, width="stretch", hide_index=True)

# ============================================================
# RESTAURANTS
# ============================================================
with tab_restaurants:
    section_header("Performance", "Restaurant & Menu Analysis")

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Active Restaurants", f"{filtered['restaurant_name'].nunique():,}", "🏪")
    with c2:
        kpi_card("Avg Revenue / Restaurant", money(filtered.groupby("restaurant_name")["price"].sum().mean()), "💵")
    with c3:
        best = filtered.groupby("restaurant_name")["price"].sum().idxmax()
        kpi_card("Top Performer", best, "🏆")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        chart_card_start("Top 10 Dishes by Revenue")
        dish = (
            filtered.groupby("dish_name", as_index=False)["price"]
            .sum()
            .sort_values("price", ascending=False)
            .head(10)
        )
        chart = (
            alt.Chart(dish)
            .mark_bar(color="#00CEC9", cornerRadiusEnd=4)
            .encode(x=alt.X("price:Q", title="Revenue ($)"), y=alt.Y("dish_name:N", sort="-x", title=""),
                    tooltip=["dish_name", "price"])
            .properties(height=340)
        )
        st.altair_chart(chart, width="stretch")
        chart_card_end()

    with c2:
        chart_card_start("Category Revenue Share by Restaurant (Top 8)")
        top8 = filtered.groupby("restaurant_name")["price"].sum().nlargest(8).index
        heat_df = filtered[filtered["restaurant_name"].isin(top8)]
        pivot = heat_df.groupby(["restaurant_name", "category"])["price"].sum().reset_index()
        fig = px.density_heatmap(
            pivot, x="category", y="restaurant_name", z="price",
            color_continuous_scale=["#161A23", "#6C5CE7", "#00CEC9"],
        )
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=340,
                           paper_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    soft_divider()
    st.markdown("**Full Restaurant × Category Revenue Matrix**")
    pivot_full = filtered.groupby(["restaurant_name", "category"])["price"].sum().reset_index()
    pivot_full = pivot_full.pivot(index="restaurant_name", columns="category", values="price").fillna(0)
    st.dataframe(pivot_full.style.format("${:,.0f}").background_gradient(cmap="Purples"), width="stretch")

# ============================================================
# ORDERS & PAYMENTS
# ============================================================
with tab_orders:
    section_header("Transactions", "Order & Payment Behavior")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Avg Quantity / Order", f"{filtered['quantity'].mean():.1f}", "🔢")
    with c2:
        kpi_card("Avg Order Value", money(filtered["price"].mean()), "💳")
    with c3:
        if "delivery_status" in filtered.columns:
            on_time = (filtered["delivery_status"].str.lower() == "delivered").mean() * 100
            kpi_card("Delivered On Time", f"{on_time:.1f}%", "✅")
    with c4:
        if "order_frequency" in filtered.columns:
            kpi_card("Avg Order Frequency", f"{filtered['order_frequency'].mean():.1f}", "📈")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        chart_card_start("Payment Method Split")
        pc = filtered["payment_method"].value_counts().reset_index()
        pc.columns = ["payment_method", "count"]
        fig = px.pie(pc, values="count", names="payment_method", hole=0.55, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    with c2:
        chart_card_start("Delivery Status Breakdown")
        dc = filtered["delivery_status"].value_counts().reset_index()
        dc.columns = ["delivery_status", "count"]
        fig = px.bar(dc, x="delivery_status", y="count", color="delivery_status", color_discrete_sequence=PALETTE)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, showlegend=False,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    if "order_frequency" in filtered.columns:
        soft_divider()
        chart_card_start("Order Frequency Distribution")
        fc = filtered["order_frequency"].value_counts().sort_index().reset_index()
        fc.columns = ["order_frequency", "count"]
        fig = px.bar(fc, x="order_frequency", y="count", color_discrete_sequence=[PALETTE[3]])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=280,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Orders per Customer", yaxis_title="")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

# ============================================================
# RATINGS
# ============================================================
with tab_ratings:
    section_header("Satisfaction", "Ratings & Customer Feedback")

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Average Rating", f"{filtered['rating'].mean():.2f} / 5", "⭐")
    with c2:
        kpi_card("Total Ratings", f"{filtered['rating'].count():,}", "📝")
    with c3:
        best_rated = filtered.groupby("restaurant_name")["rating"].mean().idxmax()
        kpi_card("Best Rated Restaurant", best_rated, "🏆")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        chart_card_start("Rating Distribution")
        fig = px.histogram(filtered, x="rating", nbins=5, color_discrete_sequence=[PALETTE[0]])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, bargap=0.15,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Rating", yaxis_title="Count")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

    with c2:
        chart_card_start("Average Rating by Restaurant (Top 10)")
        rbr = (
            filtered.groupby("restaurant_name", as_index=False)["rating"]
            .mean()
            .sort_values("rating", ascending=False)
            .head(10)
        )
        chart = (
            alt.Chart(rbr)
            .mark_bar(color="#FDCB6E", cornerRadiusEnd=4)
            .encode(x=alt.X("rating:Q", scale=alt.Scale(domain=[0, 5]), title="Avg Rating"),
                    y=alt.Y("restaurant_name:N", sort="-x", title=""), tooltip=["restaurant_name", "rating"])
            .properties(height=300)
        )
        st.altair_chart(chart, width="stretch")
        chart_card_end()

    if "rating_date" in filtered.columns and filtered["rating_date"].notna().any():
        soft_divider()
        chart_card_start("Rating Trend Over Time")
        trend = (
            filtered.dropna(subset=["rating_date"])
            .groupby(filtered["rating_date"].dt.to_period("M"))["rating"]
            .mean()
            .reset_index()
        )
        trend["rating_date"] = trend["rating_date"].dt.to_timestamp()
        fig = px.line(trend, x="rating_date", y="rating", markers=True, color_discrete_sequence=[PALETTE[0]])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=280,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="Avg Rating")
        st.plotly_chart(fig, width="stretch")
        chart_card_end()

# ============================================================
# RAW DATA
# ============================================================
with tab_data:
    section_header("Explore", "Filtered Raw Data")
    st.caption(f"{len(filtered):,} rows match the current filters (of {len(df):,} total).")
    st.dataframe(filtered, width="stretch", hide_index=True, height=460)

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download filtered data as CSV",
        data=csv_bytes,
        file_name=f"restaurant_orders_filtered_{date.today().isoformat()}.csv",
        mime="text/csv",
    )

st.markdown("<div class='site-footer'>Restaurant Customer Intelligence Dashboard · Built with Streamlit</div>", unsafe_allow_html=True)
