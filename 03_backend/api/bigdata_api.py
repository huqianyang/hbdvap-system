from flask import Blueprint

from utils.response_helper import success_response


bigdata_bp = Blueprint("bigdata_api", __name__)


@bigdata_bp.get("/api/bigdata/status")
def get_bigdata_status():
    """返回 Flume、Kafka、Storm 的课程设计流程状态说明。"""
    data = {
        "flume": "已规划，负责采集CSV数据",
        "kafka": "已规划，负责消息队列缓冲",
        "storm": "已规划，负责实时清洗、预测和统计",
        "pipeline": "CSV -> Flume -> Kafka -> Storm -> MySQL -> Flask -> Web",
    }
    return success_response(data)
