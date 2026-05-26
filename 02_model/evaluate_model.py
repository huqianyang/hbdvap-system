import json
from pathlib import Path

METRICS_PATH = Path(__file__).resolve().parent / "model_metrics.json"


def print_metrics() -> None:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    print("模型评估结果")
    print(f"模型：{metrics['model']}")
    print(f"训练集行数：{metrics['train_rows']}")
    print(f"测试集行数：{metrics['test_rows']}")
    print(f"特征数量：{metrics['feature_count']}")
    print(f"准确率 Accuracy：{metrics['accuracy']:.4f}")
    print(f"精确率 Precision：{metrics['precision']:.4f}")
    print(f"召回率 Recall：{metrics['recall']:.4f}")
    print(f"F1 值：{metrics['f1']:.4f}")
    print(f"混淆矩阵：{metrics['confusion_matrix']}")


if __name__ == "__main__":
    print_metrics()
