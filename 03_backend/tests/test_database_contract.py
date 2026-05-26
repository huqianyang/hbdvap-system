import sys
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from database.import_data import clean_csv_value, row_to_booking_dict  # noqa: E402
from models.db_models import HotelBooking, PredictionRecord, RealtimeStatistic  # noqa: E402


class DatabaseContractTestCase(unittest.TestCase):
    def test_hotel_booking_model_contains_required_fields(self):
        columns = set(HotelBooking.__table__.columns.keys())
        required_columns = {
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
        }

        self.assertTrue(required_columns.issubset(columns))

    def test_prediction_and_realtime_tables_have_course_design_fields(self):
        prediction_columns = set(PredictionRecord.__table__.columns.keys())
        realtime_columns = set(RealtimeStatistic.__table__.columns.keys())

        self.assertTrue({
            "input_json",
            "is_canceled_pred",
            "cancel_probability",
            "risk_level",
            "suggestion",
            "created_at",
        }.issubset(prediction_columns))
        self.assertTrue({
            "stat_name",
            "stat_value",
            "stat_dimension",
            "created_at",
        }.issubset(realtime_columns))

    def test_import_script_converts_csv_row_to_model_dict(self):
        row = {
            "hotel": "City Hotel",
            "is_canceled": "1",
            "lead_time": "120",
            "arrival_date_year": "2017",
            "arrival_date_month": "July",
            "arrival_date_week_number": "27",
            "arrival_date_day_of_month": "1",
            "stays_in_weekend_nights": "1",
            "stays_in_week_nights": "3",
            "adults": "2",
            "children": "",
            "babies": "0",
            "meal": "BB",
            "country": "",
            "market_segment": "Online TA",
            "distribution_channel": "TA/TO",
            "is_repeated_guest": "0",
            "previous_cancellations": "0",
            "previous_bookings_not_canceled": "0",
            "reserved_room_type": "A",
            "assigned_room_type": "A",
            "booking_changes": "0",
            "deposit_type": "No Deposit",
            "agent": "",
            "company": "",
            "days_in_waiting_list": "0",
            "customer_type": "Transient",
            "adr": "90.5",
            "required_car_parking_spaces": "0",
            "total_of_special_requests": "1",
            "reservation_status": "Check-Out",
            "reservation_status_date": "2017-07-02",
        }

        booking = row_to_booking_dict(row)

        self.assertEqual(booking["children"], 0.0)
        self.assertEqual(booking["country"], "Unknown")
        self.assertIsNone(booking["agent"])
        self.assertEqual(booking["lead_time"], 120)
        self.assertEqual(booking["adr"], 90.5)

    def test_clean_csv_value_handles_blank_values(self):
        self.assertIsNone(clean_csv_value(""))
        self.assertIsNone(clean_csv_value("   "))
        self.assertEqual(clean_csv_value("PRT"), "PRT")


if __name__ == "__main__":
    unittest.main()
