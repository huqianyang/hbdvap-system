import sys
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from utils.data_preprocess import REQUIRED_PREDICT_FIELDS  # noqa: E402


class ApiContractTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def assert_common_response(self, response, success=True):
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload.get("success"), success)
        self.assertIn("message", payload)
        self.assertIn("data", payload)
        return payload

    def test_get_interfaces_return_common_json_shape(self):
        endpoints = [
            "/api/dashboard",
            "/api/analysis/cancel-rate",
            "/api/analysis/hotel-type",
            "/api/analysis/country",
            "/api/analysis/customer-type",
            "/api/bigdata/status",
        ]

        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                payload = self.assert_common_response(self.client.get(endpoint))
                self.assertIsNotNone(payload["data"])

    def test_predict_returns_documented_fields_for_valid_payload(self):
        sample_payload = {
            "hotel": "City Hotel",
            "lead_time": 120,
            "arrival_date_month": "July",
            "stays_in_weekend_nights": 1,
            "stays_in_week_nights": 3,
            "adults": 2,
            "children": 0,
            "babies": 0,
            "meal": "BB",
            "country": "PRT",
            "market_segment": "Online TA",
            "distribution_channel": "TA/TO",
            "is_repeated_guest": 0,
            "previous_cancellations": 0,
            "previous_bookings_not_canceled": 0,
            "reserved_room_type": "A",
            "booking_changes": 0,
            "deposit_type": "No Deposit",
            "days_in_waiting_list": 0,
            "customer_type": "Transient",
            "adr": 90.0,
            "required_car_parking_spaces": 0,
            "total_of_special_requests": 1,
        }

        payload = self.assert_common_response(
            self.client.post("/api/predict", json=sample_payload)
        )
        self.assertEqual(set(payload["data"].keys()), {
            "is_canceled_pred",
            "cancel_probability",
            "risk_level",
            "suggestion",
        })

    def test_predict_reports_missing_required_field(self):
        incomplete_payload = {field: 0 for field in REQUIRED_PREDICT_FIELDS}
        incomplete_payload.pop("hotel")

        response = self.client.post("/api/predict", json=incomplete_payload)
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertFalse(payload["success"])
        self.assertIsNone(payload["data"])
        self.assertIn("hotel", payload["message"])


if __name__ == "__main__":
    unittest.main()
