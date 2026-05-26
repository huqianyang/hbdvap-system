import os
from pathlib import Path


class Config:
    """后端基础配置，数据库和模型路径后续阶段继续接入。"""

    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR.parent
    SECRET_KEY = os.getenv("SECRET_KEY", "hbdvap-course-design")
    JSON_AS_ASCII = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/hbdvap_system?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        str(PROJECT_ROOT / "02_model" / "cancellation_model.pkl"),
    )
    FEATURE_COLUMNS_PATH = os.getenv(
        "FEATURE_COLUMNS_PATH",
        str(PROJECT_ROOT / "02_model" / "feature_columns.json"),
    )
