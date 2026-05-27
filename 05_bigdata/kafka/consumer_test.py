import json
import sys
from pathlib import Path


BIGDATA_DIR = Path(__file__).resolve().parents[1]
if str(BIGDATA_DIR) not in sys.path:
    sys.path.insert(0, str(BIGDATA_DIR))

from kafka.producer_simulator import iter_csv_messages  # noqa: E402


def consume_messages(limit=5):
    """消费模拟 Kafka 消息，用于检查消息格式。"""
    messages = []
    for message in iter_csv_messages(limit=limit):
        messages.append(json.loads(message))
    return messages


def main():
    for message in consume_messages():
        print(f"[Kafka Consumer 测试接收] {message}")


if __name__ == "__main__":
    main()
