REQUIRED_PREDICT_FIELDS = [
    "hotel",
    "lead_time",
    "arrival_date_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "reserved_room_type",
    "booking_changes",
    "deposit_type",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
]

INT_FIELDS = {
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "babies",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "booking_changes",
    "days_in_waiting_list",
    "required_car_parking_spaces",
    "total_of_special_requests",
}

FLOAT_FIELDS = {"children", "adr"}


def validate_predict_payload(payload):
    """检查预测接口必填字段，字段名严格来自字段规范。"""
    return [field for field in REQUIRED_PREDICT_FIELDS if field not in payload]


def _clean_value(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def _to_int(value, default=0):
    value = _clean_value(value)
    if value is None:
        return default
    return int(float(value))


def _to_float(value, default=0.0):
    value = _clean_value(value)
    if value is None:
        return default
    return float(value)


def normalize_predict_payload(payload):
    """将前端 JSON 转成模型可用的基础字段类型。"""
    normalized = {}
    for field in REQUIRED_PREDICT_FIELDS:
        value = payload.get(field)
        if field in INT_FIELDS:
            normalized[field] = _to_int(value)
        elif field in FLOAT_FIELDS:
            normalized[field] = _to_float(value)
        else:
            normalized[field] = _clean_value(value)

    if normalized["country"] is None:
        normalized["country"] = "Unknown"
    return normalized


def build_model_input(normalized_payload, feature_columns):
    """
    按 feature_columns.json 的顺序构造模型输入。
    若模型特征列多于接口输入字段，缺失列填 0，便于兼容 one-hot 特征。
    """
    row = {
        feature: normalized_payload.get(feature, 0)
        for feature in feature_columns
    }
    try:
        import pandas as pd

        return pd.DataFrame([row], columns=feature_columns)
    except ModuleNotFoundError:
        return [row]


def get_risk_level(cancel_probability):
    """根据字段规范中的阈值生成风险等级。"""
    if cancel_probability < 0.30:
        return "低风险"
    if cancel_probability <= 0.70:
        return "中风险"
    return "高风险"


def get_suggestion(risk_level):
    """根据风险等级给出课程设计展示用建议。"""
    suggestions = {
        "低风险": "客户取消概率较低，可按正常流程接待",
        "中风险": "建议关注客户预订变化，必要时提前沟通",
        "高风险": "建议酒店提前确认客户入住意愿",
    }
    return suggestions[risk_level]
