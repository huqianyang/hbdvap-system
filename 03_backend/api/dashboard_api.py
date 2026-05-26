from flask import Blueprint

from utils.response_helper import success_response


dashboard_bp = Blueprint("dashboard_api", __name__)


@dashboard_bp.get("/api/dashboard")
def get_dashboard():
    """首页看板汇总数据，阶段 2 接入 MySQL 后改为数据库统计。"""
    data = {
        "total_bookings": 119390,
        "canceled_bookings": 44224,
        "cancel_rate": 0.3704,
        "avg_adr": 101.83,
        "city_hotel_count": 79330,
        "resort_hotel_count": 40060,
        "top_country": "PRT",
    }
    return success_response(data)
