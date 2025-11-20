from datetime import datetime

import pandas as pd

ORDERS_CSV_PATH = "orders.csv"
START_DATE = datetime(2025, 1, 1)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def filter_recent_orders(df: pd.DataFrame, start_date: datetime) -> pd.DataFrame:
    return df[df["date"] >= start_date]


def calculate_revenue(df: pd.DataFrame) -> float:
    return float((df["quantity"] * df["price"]).sum())


def main():
    df = load_data(ORDERS_CSV_PATH)
    recent_orders = filter_recent_orders(df, START_DATE)
    revenue = calculate_revenue(recent_orders)
    print(f"Total recent revenue: €{revenue:.2f}")


if __name__ == "__main__":
    main()
