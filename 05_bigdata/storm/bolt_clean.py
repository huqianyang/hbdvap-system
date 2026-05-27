INT_FIELDS = {
    "is_canceled",
    "lead_time",
    "arrival_date_year",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
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

FLOAT_FIELDS = {"children", "agent", "company", "adr"}


def clean_value(value):
    """清理 CSV/Kafka 消息中的空值。"""
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def to_int(value, default=0):
    value = clean_value(value)
    if value is None:
        return default
    return int(float(value))


def to_float(value, default=0.0):
    value = clean_value(value)
    if value is None:
        return default
    return float(value)


def clean_booking_row(row):
    """Storm 清洗 Bolt：标准化字段类型并处理缺失值。"""
    cleaned = {}
    for field, value in row.items():
        if field in INT_FIELDS:
            cleaned[field] = to_int(value)
        elif field in FLOAT_FIELDS:
            cleaned[field] = to_float(value)
        else:
            cleaned[field] = clean_value(value)

    if cleaned.get("children") is None:
        cleaned["children"] = 0.0
    if cleaned.get("country") is None:
        cleaned["country"] = "Unknown"
    return cleaned


if __name__ == "__main__":
    demo = {"hotel": "City Hotel", "lead_time": "120", "children": "", "country": ""}
    print(clean_booking_row(demo))
