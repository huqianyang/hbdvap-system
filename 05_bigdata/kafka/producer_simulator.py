import csv
import json
import time
from pathlib import Path


BIGDATA_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = BIGDATA_DIR / "flume" / "sample_source_data.csv"


def iter_csv_messages(csv_path=DEFAULT_SOURCE, limit=None):
    """逐行读取 CSV，模拟 Flume 将消息送入 Kafka。"""
    with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader):
            if limit is not None and index >= limit:
                break
            yield json.dumps(row, ensure_ascii=False)


def main():
    for message in iter_csv_messages():
        print(f"[Kafka Producer 模拟发送] {message}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
