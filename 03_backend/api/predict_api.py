from flask import Blueprint, request

from utils.data_preprocess import validate_predict_payload
from utils.model_loader import predict_cancellation
from utils.response_helper import error_response, success_response


predict_bp = Blueprint("predict_api", __name__)


@predict_bp.post("/api/predict")
def predict():
    """预订取消预测接口，模型文件存在时调用真实模型。"""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return error_response("请求体必须是 JSON 对象", status_code=400)

    missing_fields = validate_predict_payload(payload)
    if missing_fields:
        return error_response(
            "缺少必填字段：" + ", ".join(missing_fields),
            status_code=400,
        )

    prediction = predict_cancellation(payload)
    return success_response(prediction, message="预测成功")
