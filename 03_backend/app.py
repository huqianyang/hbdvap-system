from flask import Flask
from flask_cors import CORS

from api import register_blueprints
from config import Config
from models import db


def create_app():
    """创建 Flask 应用，并集中注册所有 API 蓝图。"""
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    register_blueprints(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
