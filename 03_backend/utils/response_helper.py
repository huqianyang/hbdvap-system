from flask import jsonify


def success_response(data=None, message="请求成功", status_code=200):
    """按接口文档返回统一成功 JSON。"""
    return jsonify({
        "success": True,
        "message": message,
        "data": {} if data is None else data,
    }), status_code


def error_response(message, status_code=400):
    """按接口文档返回统一失败 JSON。"""
    return jsonify({
        "success": False,
        "message": message,
        "data": None,
    }), status_code
