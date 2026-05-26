import csv
import json
from pathlib import Path

from storm.bolt_clean import clean_booking_row
from storm.bolt_predict import predict_booking
from storm.bolt_stat import RealtimeStats


PIPELINE = "CSV -> Flume -> Kafka -> Storm -> MySQL -> Flask -> Web"


def process_message(message, stats=None):
    """模拟 Storm 拓扑处理一条 Kafka 消息。"""
    stats = stats or RealtimeStats()
    row = json.loads(message) if isinstance(message, str) else message
    cleaned = clean_booking_row(row)
    prediction = predict_booking(cleaned)
    enriched = {**cleaned, **prediction}
    snapshot = stats.update(enriched)
    return enriched, snapshot


def run_topology_from_csv(csv_path, limit=None):
    """从 CSV 读取消息并执行清洗、预测、统计三个 Bolt。"""
    results = []
    stats = RealtimeStats()
    with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader):
            if limit is not None and index >= limit:
                break
            enriched, snapshot = process_message(row, stats)
            results.append({"row": enriched, "stats": snapshot})
    return results


if __name__ == "__main__":
    print(f"Storm 拓扑流程：{PIPELINE}")
