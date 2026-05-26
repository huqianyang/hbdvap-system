import json
import sys
import tempfile
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from utils.data_preprocess import (  # noqa: E402
    build_model_input,
    normalize_predict_payload,
)
from utils.model_loader import (  # noqa: E402
    get_cancel_probability,
    load_feature_columns,
)


class FakeProbabilityModel:
    def predict_proba(self, model_input):
        return [[0.2, 0.8]]


class FakePredictOnlyModel:
    def predict(self, model_input):
        return [1]


class ModelCallContractTestCase(unittest.TestCase):
    def sample_payload(self):
        return {
            "hotel": "City Hotel",
            "lead_time": "120",
            "arrival_date_month": "July",
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
            "booking_changes": "0",
            "deposit_type": "No Deposit",
            "days_in_waiting_list": "0",
            "customer_type": "Transient",
            "adr": "90.0",
            "required_car_parking_spaces": "0",
            "total_of_special_requests": "1",
        }

    def test_normalize_predict_payload_converts_types_and_defaults(self):
        normalized = normalize_predict_payload(self.sample_payload())

        self.assertEqual(normalized["lead_time"], 120)
        self.assertEqual(normalized["children"], 0.0)
        self.assertEqual(normalized["country"], "Unknown")
        self.assertEqual(normalized["adr"], 90.0)

    def test_load_feature_columns_reads_json_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            feature_path = Path(tmpdir) / "feature_columns.json"
            feature_path.write_text(
                json.dumps(["hotel", "lead_time", "adr"]),
                encoding="utf-8",
            )

            self.assertEqual(
                load_feature_columns(feature_path),
                ["hotel", "lead_time", "adr"],
            )

    def test_build_model_input_keeps_feature_column_order(self):
        normalized = normalize_predict_payload(self.sample_payload())
        model_input = build_model_input(normalized, ["adr", "hotel", "unknown_flag"])

        if hasattr(model_input, "columns"):
            self.assertEqual(list(model_input.columns), ["adr", "hotel", "unknown_flag"])
            self.assertEqual(model_input.iloc[0]["unknown_flag"], 0)
        else:
            self.assertEqual(list(model_input[0].keys()), ["adr", "hotel", "unknown_flag"])
            self.assertEqual(model_input[0]["unknown_flag"], 0)

    def test_get_cancel_probability_uses_predict_proba_when_available(self):
        probability = get_cancel_probability(FakeProbabilityModel(), [{"lead_time": 120}])
        self.assertEqual(probability, 0.8)

    def test_get_cancel_probability_falls_back_to_predict(self):
        probability = get_cancel_probability(FakePredictOnlyModel(), [{"lead_time": 120}])
        self.assertEqual(probability, 1.0)


if __name__ == "__main__":
    unittest.main()
