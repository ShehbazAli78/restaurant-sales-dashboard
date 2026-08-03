"""Robust, cached data loading and cleaning for the dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "clean_data.csv"

# Tolerate both "snake_case" and "Human Readable" headers.
_COLUMN_ALIASES = {
    "customer id": "customer_id",
    "signup date": "signup_date",
    "order id": "order_id",
    "order date": "order_date",
    "restaurant name": "restaurant_name",
    "dish name": "dish_name",
    "payment method": "payment_method",
    "order frequency": "order_frequency",
    "last order date": "last_order_date",
    "loyalty points": "loyalty_points",
    "rating date": "rating_date",
    "delivery status": "delivery_status",
}

_DATE_COLUMNS = ["signup_date", "order_date", "last_order_date", "rating_date"]


@st.cache_data(show_spinner=False)
def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and clean the restaurant orders dataset."""
    if not Path(path).exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns=_COLUMN_ALIASES)

    for col in _DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in ["quantity", "price", "order_frequency", "loyalty_points", "rating"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def has_columns(df: pd.DataFrame, columns: list[str]) -> bool:
    return all(col in df.columns for col in columns)
