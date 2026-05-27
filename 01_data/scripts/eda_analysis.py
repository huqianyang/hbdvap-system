from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
CLEAN_DATA_PATH = ROOT_DIR / "01_data" / "processed" / "hotel_bookings_clean.csv"
MONTHLY_CANCEL_RATE_PATH = ROOT_DIR / "01_data" / "eda" / "cancellation_rate_by_month.csv"
COUNTRY_TOP_STATS_PATH = ROOT_DIR / "01_data" / "eda" / "country_top_stats.csv"
HOTEL_TYPE_STATS_PATH = ROOT_DIR / "01_data" / "eda" / "hotel_type_stats.csv"
CUSTOMER_TYPE_STATS_PATH = ROOT_DIR / "01_data" / "eda" / "customer_type_stats.csv"


def run_eda() -> None:
    df = pd.read_csv(CLEAN_DATA_PATH)

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    monthly = (
        df.groupby("arrival_date_month")
        .agg(booking_count=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
        .reindex(month_order)
        .reset_index()
        .rename(columns={"arrival_date_month": "month"})
    )
    monthly.to_csv(MONTHLY_CANCEL_RATE_PATH, index=False, encoding="utf-8-sig")

    country = (
        df.groupby("country")
        .agg(booking_count=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
        .sort_values("booking_count", ascending=False)
        .head(20)
        .reset_index()
    )
    country.to_csv(COUNTRY_TOP_STATS_PATH, index=False, encoding="utf-8-sig")

    hotel_type = (
        df.groupby("hotel")
        .agg(booking_count=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"), avg_adr=("adr", "mean"))
        .reset_index()
    )
    hotel_type.to_csv(HOTEL_TYPE_STATS_PATH, index=False, encoding="utf-8-sig")

    customer_type = (
        df.groupby("customer_type")
        .agg(booking_count=("is_canceled", "size"), cancel_rate=("is_canceled", "mean"))
        .sort_values("booking_count", ascending=False)
        .reset_index()
    )
    customer_type.to_csv(CUSTOMER_TYPE_STATS_PATH, index=False, encoding="utf-8-sig")

    print("EDA 输出完成")
    print(f"月度取消率：{MONTHLY_CANCEL_RATE_PATH}")
    print(f"国家/地区统计：{COUNTRY_TOP_STATS_PATH}")
    print(f"酒店类型统计：{HOTEL_TYPE_STATS_PATH}")
    print(f"客户类型统计：{CUSTOMER_TYPE_STATS_PATH}")


if __name__ == "__main__":
    run_eda()
