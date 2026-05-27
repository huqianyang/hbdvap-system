import csv
import sys
import tempfile
import unittest
from pathlib import Path


BIGDATA_DIR = Path(__file__).resolve().parents[1]
if str(BIGDATA_DIR) not in sys.path:
    sys.path.insert(0, str(BIGDATA_DIR))


class BigdataContractTestCase(unittest.TestCase):
    def test_required_bigdata_files_exist(self):
        required_files = [
            "README.md",
            "flume/flume_hotel_booking.conf",
            "kafka/producer_simulator.py",
            "kafka/consumer_test.py",
            "storm/topology.py",
            "storm/bolt_clean.py",
            "storm/bolt_predict.py",
            "storm/bolt_stat.py",
            "scripts/run_pipeline_demo.py",
        ]

        for relative_path in required_files:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((BIGDATA_DIR / relative_path).exists())

    def test_clean_bolt_normalizes_booking_fields(self):
        from storm.bolt_clean import clean_booking_row

        cleaned = clean_booking_row({
            "hotel": "City Hotel",
            "is_canceled": "1",
            "lead_time": "120",
            "arrival_date_month": "July",
            "children": "",
            "country": "",
            "adr": "90.5",
            "total_of_special_requests": "1",
        })

        self.assertEqual(cleaned["children"], 0.0)
        self.assertEqual(cleaned["country"], "Unknown")
        self.assertEqual(cleaned["lead_time"], 120)
        self.assertEqual(cleaned["adr"], 90.5)

    def test_predict_bolt_returns_documented_prediction_fields(self):
        from storm.bolt_predict import predict_booking

        prediction = predict_booking({
            "lead_time": 120,
            "deposit_type": "No Deposit",
            "previous_cancellations": 0,
            "total_of_special_requests": 1,
            "required_car_parking_spaces": 0,
        })

        self.assertEqual(set(prediction.keys()), {
            "is_canceled_pred",
            "cancel_probability",
            "risk_level",
            "suggestion",
        })

    def test_pipeline_demo_processes_sample_csv(self):
        from scripts.run_pipeline_demo import run_pipeline

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "sample.csv"
            output_path = Path(tmpdir) / "result.csv"
            with input_path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "hotel",
                    "is_canceled",
                    "lead_time",
                    "arrival_date_month",
                    "children",
                    "country",
                    "deposit_type",
                    "previous_cancellations",
                    "total_of_special_requests",
                    "required_car_parking_spaces",
                    "adr",
                ])
                writer.writeheader()
                writer.writerow({
                    "hotel": "City Hotel",
                    "is_canceled": "0",
                    "lead_time": "120",
                    "arrival_date_month": "July",
                    "children": "",
                    "country": "",
                    "deposit_type": "No Deposit",
                    "previous_cancellations": "0",
                    "total_of_special_requests": "1",
                    "required_car_parking_spaces": "0",
                    "adr": "90.5",
                })

            summary = run_pipeline(input_path, output_path, limit=1)

            self.assertEqual(summary["processed_count"], 1)
            self.assertTrue(output_path.exists())
            self.assertIn("CSV -> Flume -> Kafka -> Storm -> MySQL -> Flask -> Web", summary["pipeline"])


if __name__ == "__main__":
    unittest.main()
