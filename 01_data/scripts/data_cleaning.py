from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT_DIR / "hotel_bookings.csv"
CLEAN_DATA_PATH = ROOT_DIR / "01_data" / "processed" / "hotel_bookings_clean.csv"
MISSING_SUMMARY_PATH = ROOT_DIR / "01_data" / "eda" / "missing_values_summary.csv"


def clean_hotel_bookings() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_PATH)

    missing_summary = (
        df.isna()
        .sum()
        .reset_index()
        .rename(columns={"index": "field", 0: "missing_count"})
    )
    missing_summary["missing_rate"] = missing_summary["missing_count"] / len(df)
    MISSING_SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    missing_summary.to_csv(MISSING_SUMMARY_PATH, index=False, encoding="utf-8-sig")

    df["children"] = df["children"].fillna(0)
    df["country"] = df["country"].fillna("Unknown")
    df["agent"] = df["agent"].fillna(0)
    df["company"] = df["company"].fillna(0)

    integer_columns = ["children", "agent", "company"]
    for column in integer_columns:
        df[column] = df[column].astype(int)

    df = df[df["adr"] >= 0].copy()
    df["total_stay_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df["total_guests"] = df["adults"] + df["children"] + df["babies"]
    df["has_special_request"] = (df["total_of_special_requests"] > 0).astype(int)

    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    cleaned = clean_hotel_bookings()
    print(f"清洗完成：{cleaned.shape[0]} 行，{cleaned.shape[1]} 列")
    print(f"输出文件：{CLEAN_DATA_PATH}")
    print(f"缺失值统计：{MISSING_SUMMARY_PATH}")
