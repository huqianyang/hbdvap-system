import json
from pathlib import Path

import joblib
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "02_model" / "cancellation_model.pkl"
FEATURE_COLUMNS_PATH = ROOT_DIR / "02_model" / "feature_columns.json"


def risk_level(probability: float) -> str:
    if probability < 0.3:
        return "低风险"
    if probability <= 0.7:
        return "中风险"
    return "高风险"


def suggestion(level: str) -> str:
    if level == "高风险":
        return "建议酒店提前确认客户入住意愿，并关注押金和历史取消情况。"
    if level == "中风险":
        return "建议保持正常跟进，可在入住前发送提醒。"
    return "取消风险较低，可按常规流程处理。"


def build_sample_feature_row() -> pd.DataFrame:
    feature_columns = json.loads(FEATURE_COLUMNS_PATH.read_text(encoding="utf-8"))
    row = pd.DataFrame([{column: 0 for column in feature_columns}])

    sample_values = {
        "lead_time": 120,
        "stays_in_weekend_nights": 1,
        "stays_in_week_nights": 3,
        "adults": 2,
        "children": 0,
        "babies": 0,
        "is_repeated_guest": 0,
        "previous_cancellations": 0,
        "previous_bookings_not_canceled": 0,
        "booking_changes": 0,
        "days_in_waiting_list": 0,
        "adr": 90.0,
        "required_car_parking_spaces": 0,
        "total_of_special_requests": 1,
        "total_stay_nights": 4,
        "total_guests": 2,
        "has_special_request": 1,
        "hotel_City Hotel": 1,
        "arrival_date_month_July": 1,
        "meal_BB": 1,
        "country_PRT": 1,
        "market_segment_Online TA": 1,
        "distribution_channel_TA/TO": 1,
        "reserved_room_type_A": 1,
        "deposit_type_No Deposit": 1,
        "customer_type_Transient": 1,
    }

    for column, value in sample_values.items():
        if column in row.columns:
            row.loc[0, column] = value

    return row


def predict_demo() -> dict:
    model = joblib.load(MODEL_PATH)
    sample = build_sample_feature_row()
    pred = int(model.predict(sample)[0])
    probability = float(model.predict_proba(sample)[0][1])
    level = risk_level(probability)
    return {
        "is_canceled_pred": pred,
        "cancel_probability": round(probability, 4),
        "risk_level": level,
        "suggestion": suggestion(level),
    }


if __name__ == "__main__":
    result = predict_demo()
    print(json.dumps(result, ensure_ascii=False, indent=2))
