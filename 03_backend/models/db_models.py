try:
    from flask_sqlalchemy import SQLAlchemy
except ModuleNotFoundError:
    SQLAlchemy = None


HOTEL_BOOKING_COLUMNS = [
    "id",
    "hotel",
    "is_canceled",
    "lead_time",
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "reserved_room_type",
    "assigned_room_type",
    "booking_changes",
    "deposit_type",
    "agent",
    "company",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
    "reservation_status",
    "reservation_status_date",
]
PREDICTION_RECORD_COLUMNS = [
    "id",
    "input_json",
    "is_canceled_pred",
    "cancel_probability",
    "risk_level",
    "suggestion",
    "created_at",
]
REALTIME_STATISTIC_COLUMNS = [
    "id",
    "stat_name",
    "stat_value",
    "stat_dimension",
    "created_at",
]


if SQLAlchemy is None:
    class _NoopSession:
        def bulk_save_objects(self, objects):
            raise RuntimeError("请先安装 Flask-SQLAlchemy 后再执行数据库导入")

        def commit(self):
            raise RuntimeError("请先安装 Flask-SQLAlchemy 后再执行数据库导入")


    class _NoopDb:
        Model = object
        session = _NoopSession()

        def init_app(self, app):
            return None

        def create_all(self):
            raise RuntimeError("请先安装 Flask-SQLAlchemy 后再创建数据库表")


    class _ColumnMeta:
        def __init__(self, name):
            self.name = name


    class _ColumnCollection(list):
        def keys(self):
            return [column.name for column in self]


    class _TableMeta:
        def __init__(self, columns):
            self.columns = _ColumnCollection(_ColumnMeta(name) for name in columns)


    db = _NoopDb()


    class HotelBooking:
        """清洗后的酒店预订数据，字段名严格参考字段规范。"""

        __tablename__ = "hotel_bookings"
        __table__ = _TableMeta(HOTEL_BOOKING_COLUMNS)

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)


    class PredictionRecord:
        """预测记录表模型，保存前端请求和模型输出。"""

        __tablename__ = "prediction_records"
        __table__ = _TableMeta(PREDICTION_RECORD_COLUMNS)


    class RealtimeStatistic:
        """大数据流程统计结果表模型。"""

        __tablename__ = "realtime_statistics"
        __table__ = _TableMeta(REALTIME_STATISTIC_COLUMNS)
else:
    db = SQLAlchemy()


    class HotelBooking(db.Model):
        """清洗后的酒店预订数据，字段名严格参考字段规范。"""

        __tablename__ = "hotel_bookings"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        hotel = db.Column(db.String(50), nullable=False)
        is_canceled = db.Column(db.Integer, nullable=True)
        lead_time = db.Column(db.Integer, nullable=True)
        arrival_date_year = db.Column(db.Integer, nullable=True)
        arrival_date_month = db.Column(db.String(20), nullable=True)
        arrival_date_week_number = db.Column(db.Integer, nullable=True)
        arrival_date_day_of_month = db.Column(db.Integer, nullable=True)
        stays_in_weekend_nights = db.Column(db.Integer, nullable=True)
        stays_in_week_nights = db.Column(db.Integer, nullable=True)
        adults = db.Column(db.Integer, nullable=True)
        children = db.Column(db.Float, nullable=True)
        babies = db.Column(db.Integer, nullable=True)
        meal = db.Column(db.String(20), nullable=True)
        country = db.Column(db.String(20), nullable=True)
        market_segment = db.Column(db.String(50), nullable=True)
        distribution_channel = db.Column(db.String(50), nullable=True)
        is_repeated_guest = db.Column(db.Integer, nullable=True)
        previous_cancellations = db.Column(db.Integer, nullable=True)
        previous_bookings_not_canceled = db.Column(db.Integer, nullable=True)
        reserved_room_type = db.Column(db.String(10), nullable=True)
        assigned_room_type = db.Column(db.String(10), nullable=True)
        booking_changes = db.Column(db.Integer, nullable=True)
        deposit_type = db.Column(db.String(50), nullable=True)
        agent = db.Column(db.Float, nullable=True)
        company = db.Column(db.Float, nullable=True)
        days_in_waiting_list = db.Column(db.Integer, nullable=True)
        customer_type = db.Column(db.String(50), nullable=True)
        adr = db.Column(db.Float, nullable=True)
        required_car_parking_spaces = db.Column(db.Integer, nullable=True)
        total_of_special_requests = db.Column(db.Integer, nullable=True)
        reservation_status = db.Column(db.String(50), nullable=True)
        reservation_status_date = db.Column(db.Date, nullable=True)


    class PredictionRecord(db.Model):
        """预测记录表模型，保存前端请求和模型输出。"""

        __tablename__ = "prediction_records"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        input_json = db.Column(db.JSON, nullable=False)
        is_canceled_pred = db.Column(db.Integer, nullable=False)
        cancel_probability = db.Column(db.Float, nullable=False)
        risk_level = db.Column(db.String(20), nullable=False)
        suggestion = db.Column(db.String(255), nullable=False)
        created_at = db.Column(db.DateTime, server_default=db.func.now())


    class RealtimeStatistic(db.Model):
        """大数据流程统计结果表模型。"""

        __tablename__ = "realtime_statistics"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        stat_name = db.Column(db.String(100), nullable=False)
        stat_value = db.Column(db.Float, nullable=False)
        stat_dimension = db.Column(db.String(100), nullable=True)
        created_at = db.Column(db.DateTime, server_default=db.func.now())
