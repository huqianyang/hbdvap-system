from pathlib import Path
import importlib.util

import pandas as pd

MODULE_PATH = Path(__file__).resolve().parent / "data_cleaning.py"
spec = importlib.util.spec_from_file_location("data_cleaning", MODULE_PATH)
data_cleaning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_cleaning)


def test_clean_hotel_bookings_fills_required_missing_values(tmp_path):
    raw_path = tmp_path / "hotel_bookings.csv"
    clean_path = tmp_path / "hotel_bookings_clean.csv"
    summary_path = tmp_path / "missing_values_summary.csv"

    pd.DataFrame(
        {
            "hotel": ["City Hotel"],
            "is_canceled": [1],
            "lead_time": [12],
            "arrival_date_month": ["July"],
            "stays_in_weekend_nights": [1],
            "stays_in_week_nights": [2],
            "adults": [2],
            "children": [None],
            "babies": [0],
            "meal": ["BB"],
            "country": [None],
            "market_segment": ["Online TA"],
            "distribution_channel": ["TA/TO"],
            "is_repeated_guest": [0],
            "previous_cancellations": [0],
            "previous_bookings_not_canceled": [0],
            "reserved_room_type": ["A"],
            "assigned_room_type": ["A"],
            "booking_changes": [0],
            "deposit_type": ["No Deposit"],
            "agent": [None],
            "company": [None],
            "days_in_waiting_list": [0],
            "customer_type": ["Transient"],
            "adr": [90.0],
            "required_car_parking_spaces": [0],
            "total_of_special_requests": [1],
            "reservation_status": ["Canceled"],
            "reservation_status_date": ["2015-07-01"],
        }
    ).to_csv(raw_path, index=False)

    cleaned = data_cleaning.clean_hotel_bookings(raw_path, clean_path, summary_path)

    assert cleaned.loc[0, "children"] == 0
    assert cleaned.loc[0, "country"] == "Unknown"
    assert cleaned.loc[0, "agent"] == 0
    assert cleaned.loc[0, "company"] == 0
    assert clean_path.exists()
    assert summary_path.exists()
