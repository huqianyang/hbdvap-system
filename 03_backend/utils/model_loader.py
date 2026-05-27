import json
import pickle
from pathlib import Path

from flask import current_app, has_app_context

from utils.data_preprocess import (
    REQUIRED_PREDICT_FIELDS,
    build_model_input,
    get_risk_level,
    get_suggestion,
    normalize_predict_payload,
)


_MODEL_CACHE = {}
_FEATURE_COLUMNS_CACHE = {}


def load_feature_columns(feature_columns_path):
    """读取 A 成员提供的 feature_columns.json；缺失时使用接口输入字段。"""
    path = Path(feature_columns_path)
    if not path.exists():
        return list(REQUIRED_PREDICT_FIELDS)

    cache_key = str(path.resolve())
    if cache_key in _FEATURE_COLUMNS_CACHE:
        return _FEATURE_COLUMNS_CACHE[cache_key]

    with path.open("r", encoding="utf-8") as file:
        feature_columns = json.load(file)
    if not isinstance(feature_columns, list) or not feature_columns:
        raise ValueError("feature_columns.json 必须是非空数组")

    _FEATURE_COLUMNS_CACHE[cache_key] = feature_columns
    return feature_columns


def load_model(model_path):
    """加载 cancellation_model.pkl，优先 joblib，失败时使用 pickle。"""
    path = Path(model_path)
    if not path.exists():
        return None

    cache_key = str(path.resolve())
    if cache_key in _MODEL_CACHE:
        return _MODEL_CACHE[cache_key]

    try:
        import joblib

        model = joblib.load(path)
    except ModuleNotFoundError:
        with path.open("rb") as file:
            model = pickle.load(file)

    _MODEL_CACHE[cache_key] = model
    return model


def get_cancel_probability(model, model_input):
    """兼容 sklearn 的 predict_proba 和 predict 两类输出。"""
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(model_input)
        return float(probabilities[0][1])

    prediction = model.predict(model_input)
    return float(prediction[0])


def _get_config_value(name, default):
    if has_app_context():
        return current_app.config.get(name, default)
    return default


def _fallback_demo_prediction(payload):
    """模型文件未提供时使用演示规则，保证前后端联调不中断。"""
    probability = 0.25

    if int(payload.get("lead_time", 0)) >= 90:
        probability += 0.25
    if payload.get("deposit_type") == "Non Refund":
        probability += 0.25
    if int(payload.get("previous_cancellations", 0)) > 0:
        probability += 0.15
    if int(payload.get("total_of_special_requests", 0)) == 0:
        probability += 0.10
    if int(payload.get("required_car_parking_spaces", 0)) > 0:
        probability -= 0.10

    return round(max(0.01, min(probability, 0.99)), 4)


def predict_cancellation(payload):
    """
    加载并调用 A 提供的模型。
    当前仓库若暂未提供模型文件，则使用演示规则保持接口字段稳定。
    """
    normalized_payload = normalize_predict_payload(payload)
    model_path = _get_config_value("MODEL_PATH", "../02_model/cancellation_model.pkl")
    feature_path = _get_config_value("FEATURE_COLUMNS_PATH", "../02_model/feature_columns.json")

    model = load_model(model_path)
    if model is None:
        cancel_probability = _fallback_demo_prediction(normalized_payload)
    else:
        feature_columns = load_feature_columns(feature_path)
        model_input = build_model_input(normalized_payload, feature_columns)
        cancel_probability = round(
            max(0.0, min(get_cancel_probability(model, model_input), 1.0)),
            4,
        )

    risk_level = get_risk_level(cancel_probability)

    return {
        "is_canceled_pred": 1 if cancel_probability > 0.50 else 0,
        "cancel_probability": cancel_probability,
        "risk_level": risk_level,
        "suggestion": get_suggestion(risk_level),
    }
