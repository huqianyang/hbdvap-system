from api.analysis_api import analysis_bp
from api.bigdata_api import bigdata_bp
from api.dashboard_api import dashboard_bp
from api.predict_api import predict_bp


def register_blueprints(app):
    """注册接口文档中约定的全部 API。"""
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(bigdata_bp)
