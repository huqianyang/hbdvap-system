import csv
import sys
from datetime import datetime
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from models import db  # noqa: E402
from models.db_models import HotelBooking  # noqa: E402


DEFAULT_CSV_PATH = PROJECT_ROOT / "01_data" / "processed" / "hotel_bookings_clean.csv"

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

TEXT_FIELDS = {
    "hotel",
    "arrival_date_month",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "reserved_room_type",
    "assigned_room_type",
    "deposit_type",
    "customer_type",
    "reservation_status",
}

BOOKING_FIELDS = [
    "hotel",
    "is_canceled",
    "lead_time",
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
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
    "assigned_room_type",
    "booking_changes",
    "deposit_type",
    "agent",
    "company",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
    "reservation_status",
    "reservation_status_date",
]


def clean_csv_value(value):
    """把 CSV 中的空字符串统一转成 None。"""
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def to_int(value, default=None):
    value = clean_csv_value(value)
    if value is None:
        return default
    return int(float(value))


def to_float(value, default=None):
    value = clean_csv_value(value)
    if value is None:
        return default
    return float(value)


def to_date(value):
    value = clean_csv_value(value)
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def row_to_booking_dict(row):
    """将一行 CSV 数据转换为 HotelBooking 可接收的字典。"""
    booking = {}
    for field in BOOKING_FIELDS:
        raw_value = row.get(field)
        if field in INT_FIELDS:
            booking[field] = to_int(raw_value)
        elif field in FLOAT_FIELDS:
            booking[field] = to_float(raw_value)
        elif field == "reservation_status_date":
            booking[field] = to_date(raw_value)
        else:
            booking[field] = clean_csv_value(raw_value)

    # 字段规范要求 children 缺失填 0，country 缺失填 Unknown。
    if booking["children"] is None:
        booking["children"] = 0.0
    if booking["country"] is None:
        booking["country"] = "Unknown"
    return booking


def import_csv(csv_path=DEFAULT_CSV_PATH, batch_size=1000):
    """导入清洗后的酒店预订数据到 MySQL。"""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"未找到清洗后数据文件：{csv_path}")

    app = create_app()
    total_count = 0
    with app.app_context():
        db.create_all()
        with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            batch = []
            for row in reader:
                batch.append(HotelBooking(**row_to_booking_dict(row)))
                if len(batch) >= batch_size:
                    db.session.bulk_save_objects(batch)
                    db.session.commit()
                    total_count += len(batch)
                    batch.clear()

            if batch:
                db.session.bulk_save_objects(batch)
                db.session.commit()
                total_count += len(batch)

    return total_count


if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV_PATH
    count = import_csv(path_arg)
    print(f"导入完成，共导入 {count} 条酒店预订数据。")
