import json
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
CLEAN_DATA_PATH = ROOT_DIR / "01_data" / "processed" / "hotel_bookings_clean.csv"
FEATURE_DATA_PATH = ROOT_DIR / "01_data" / "processed" / "model_features.csv"
FEATURE_COLUMNS_PATH = ROOT_DIR / "02_model" / "feature_columns.json"

TARGET_COLUMN = "is_canceled"
CATEGORICAL_COLUMNS = [
    "hotel",
    "arrival_date_month",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "reserved_room_type",
    "deposit_type",
    "customer_type",
]
NUMERIC_COLUMNS = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "booking_changes",
    "days_in_waiting_list",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
    "total_stay_nights",
    "total_guests",
    "has_special_request",
]


def build_model_features() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_DATA_PATH)
    selected_columns = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS + [TARGET_COLUMN]
    model_df = df[selected_columns].copy()

    for column in NUMERIC_COLUMNS:
        model_df[column] = model_df[column].fillna(model_df[column].median())

    for column in CATEGORICAL_COLUMNS:
        model_df[column] = model_df[column].fillna("Unknown").astype(str)

    feature_df = pd.get_dummies(
        model_df,
        columns=CATEGORICAL_COLUMNS,
        drop_first=False,
        dtype=int,
    )

    target = feature_df.pop(TARGET_COLUMN)
    feature_df[TARGET_COLUMN] = target

    FEATURE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    feature_df.to_csv(FEATURE_DATA_PATH, index=False, encoding="utf-8-sig")

    feature_columns = [column for column in feature_df.columns if column != TARGET_COLUMN]
    FEATURE_COLUMNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEATURE_COLUMNS_PATH.write_text(
        json.dumps(feature_columns, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return feature_df


if __name__ == "__main__":
    features = build_model_features()
    print(f"特征工程完成：{features.shape[0]} 行，{features.shape[1]} 列")
    print(f"特征数据：{FEATURE_DATA_PATH}")
    print(f"特征列清单：{FEATURE_COLUMNS_PATH}")
