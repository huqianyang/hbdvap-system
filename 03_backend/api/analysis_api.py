from flask import Blueprint

from utils.response_helper import success_response


analysis_bp = Blueprint("analysis_api", __name__)


@analysis_bp.get("/api/analysis/cancel-rate")
def get_cancel_rate():
    """按月份返回取消率趋势，阶段 2 接入数据库聚合。"""
    data = {
        "x_axis": ["January", "February", "March", "April"],
        "cancel_rate": [0.31, 0.34, 0.36, 0.38],
        "booking_count": [5000, 6200, 7100, 8300],
    }
    return success_response(data)


@analysis_bp.get("/api/analysis/hotel-type")
def get_hotel_type():
    """返回酒店类型维度的订单数量和取消率。"""
    data = [
        {"hotel": "City Hotel", "booking_count": 79330, "cancel_rate": 0.42},
        {"hotel": "Resort Hotel", "booking_count": 40060, "cancel_rate": 0.28},
    ]
    return success_response(data)


@analysis_bp.get("/api/analysis/country")
def get_country():
    """返回主要客源国家/地区订单数量。"""
    data = [
        {"country": "PRT", "booking_count": 48590},
        {"country": "GBR", "booking_count": 12129},
        {"country": "FRA", "booking_count": 10415},
    ]
    return success_response(data)


@analysis_bp.get("/api/analysis/customer-type")
def get_customer_type():
    """返回客户类型维度的订单数量和取消率。"""
    data = [
        {"customer_type": "Transient", "booking_count": 89613, "cancel_rate": 0.41},
        {"customer_type": "Contract", "booking_count": 4076, "cancel_rate": 0.31},
        {"customer_type": "Group", "booking_count": 577, "cancel_rate": 0.10},
    ]
    return success_response(data)
