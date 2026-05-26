import csv
import sys
from pathlib import Path


BIGDATA_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BIGDATA_DIR.parent
if str(BIGDATA_DIR) not in sys.path:
    sys.path.insert(0, str(BIGDATA_DIR))

from storm.topology import PIPELINE, process_message  # noqa: E402
from storm.bolt_stat import RealtimeStats  # noqa: E402


DEFAULT_INPUT = PROJECT_ROOT / "01_data" / "raw" / "hotel_bookings.csv"
FALLBACK_INPUT = BIGDATA_DIR / "flume" / "sample_source_data.csv"
DEFAULT_OUTPUT = BIGDATA_DIR / "scripts" / "pipeline_demo_output.csv"


def resolve_input_path(input_path=None):
    """优先使用原始数据，不存在则使用课程演示样例数据。"""
    if input_path is not None:
        return Path(input_path)
    if DEFAULT_INPUT.exists():
        return DEFAULT_INPUT
    return FALLBACK_INPUT


def run_pipeline(input_path=None, output_path=DEFAULT_OUTPUT, limit=20):
    """一键模拟 Flume -> Kafka -> Storm 的数据流。"""
    input_path = resolve_input_path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    processed_rows = []
    stats = RealtimeStats()
    with input_path.open("r", encoding="utf-8-sig", newline="") as input_file:
        reader = csv.DictReader(input_file)
        for index, row in enumerate(reader):
            if limit is not None and index >= limit:
                break
            enriched, _snapshot = process_message(row, stats)
            processed_rows.append(enriched)

    if processed_rows:
        fieldnames = list(processed_rows[0].keys())
        with output_path.open("w", encoding="utf-8-sig", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_rows)

    return {
        "pipeline": PIPELINE,
        "input_path": str(input_path),
        "output_path": str(output_path),
        "processed_count": len(processed_rows),
        "statistics": stats.snapshot(),
    }


def main():
    summary = run_pipeline()
    print("大数据单机模拟流程完成")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
