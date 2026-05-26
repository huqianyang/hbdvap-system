# 成员B_后端大数据提示词

下面内容请成员 B 直接复制到 Claude、Codex、豆包或 ChatGPT 中使用。生成代码前，必须同时提供以下文档给 AI：

1. `项目总说明.md`
2. `项目目录结构.md`
3. `字段规范.md`
4. `接口文档.md`
5. `数据流架构说明.md`

---

## 提示词 1：生成 Flask 后端基础结构

```text
你现在是 Flask 后端开发工程师，请基于《酒店预订数据可视化分析与预测系统》生成后端代码。

项目背景：
- 项目名称：酒店预订数据可视化分析与预测系统
- 数据集：Kaggle Hotel Booking Demand
- 目标：提供酒店预订取消预测、数据看板、多维分析接口
- 技术栈：Flask + SQLAlchemy + MySQL

我负责的目录：
03_backend/
05_bigdata/

必须遵守：
1. 严格按照接口文档开发，不要自己改接口地址。
2. 严格按照字段规范使用字段名，不要自己造字段。
3. 不要训练模型，只负责加载 02_model/cancellation_model.pkl。
4. 所有接口返回 JSON，格式必须是：success、message、data。
5. 代码要有中文注释。
6. 给出每个文件的完整代码和运行步骤。

请生成 03_backend 目录下的基础 Flask 项目结构，包括：
- app.py
- config.py
- requirements.txt
- api/__init__.py
- api/dashboard_api.py
- api/predict_api.py
- api/analysis_api.py
- api/bigdata_api.py
- models/db_models.py
- utils/model_loader.py
- utils/data_preprocess.py
- utils/response_helper.py

接口必须包含：
GET /api/dashboard
POST /api/predict
GET /api/analysis/cancel-rate
GET /api/analysis/hotel-type
GET /api/analysis/country
GET /api/analysis/customer-type
GET /api/bigdata/status
```

---

## 提示词 2：生成数据库建表和导入脚本

```text
你现在是 MySQL 数据库开发工程师，请为《酒店预订数据可视化分析与预测系统》设计数据库表结构和数据导入脚本。

项目要求：
- 后端使用 Flask + SQLAlchemy + MySQL
- 数据来自 01_data/processed/hotel_bookings_clean.csv
- 需要支持首页看板、取消率分析、国家分析、客户类型分析和预测记录保存

请生成：
1. 03_backend/database/schema.sql
2. 03_backend/database/import_data.py
3. SQLAlchemy 模型类 models/db_models.py

至少包含以下表：
1. hotel_bookings：存储清洗后的酒店预订数据
2. prediction_records：存储每次预测的输入、输出、预测时间
3. realtime_statistics：存储大数据流程产生的统计结果，可简化

要求：
- 字段名必须参考字段规范.md
- 不要使用中文字段名
- 主键自增
- 适合课程设计，不要过度复杂
- 给出完整 SQL 和 Python 导入脚本
```

---

## 提示词 3：生成模型调用接口

```text
你现在是 Flask + 机器学习模型部署工程师，请帮我实现酒店预订取消预测接口。

已有模型文件：02_model/cancellation_model.pkl
已有特征列文件：02_model/feature_columns.json
接口地址：POST /api/predict
接口输入和输出必须严格遵守接口文档.md

要求：
1. 在 03_backend/utils/model_loader.py 中封装模型加载逻辑。
2. 在 03_backend/utils/data_preprocess.py 中封装输入 JSON 到模型特征的转换逻辑。
3. 在 03_backend/api/predict_api.py 中实现 /api/predict。
4. 返回字段必须包含：is_canceled_pred、cancel_probability、risk_level、suggestion。
5. 风险等级规则：概率 <0.3 为低风险，0.3-0.7 为中风险，>0.7 为高风险。
6. 代码要能处理输入字段缺失的情况，并返回清晰错误信息。
7. 给出完整代码和测试 JSON。

注意：不要重新训练模型，只调用已有模型。
```

---

## 提示词 4：生成大数据模块

```text
你现在是大数据课程设计开发工程师，请为《酒店预订数据可视化分析与预测系统》生成 Flume + Kafka + Storm 模块。

课程要求：必须体现 Flume、Kafka、Storm。
项目数据流：
hotel_bookings.csv -> Flume -> Kafka -> Storm -> MySQL -> Flask -> Web

请在 05_bigdata/ 目录下生成：
1. README.md：说明大数据模块作用和运行方式
2. flume/flume_hotel_booking.conf：Flume 采集配置
3. kafka/producer_simulator.py：Kafka 生产者模拟脚本
4. kafka/consumer_test.py：Kafka 消费测试脚本
5. storm/topology.py：Storm 拓扑入口
6. storm/bolt_clean.py：数据清洗 Bolt
7. storm/bolt_predict.py：模型预测 Bolt
8. storm/bolt_stat.py：实时统计 Bolt
9. scripts/run_pipeline_demo.py：一键模拟完整数据流

要求：
- 适合 Windows 单机课程设计环境
- 如果真实 Flume/Kafka/Storm 不易运行，要提供 Python 模拟流程
- 代码要有中文注释
- 文档中解释 Flume、Kafka、Storm 分别负责什么
- 不要修改字段规范和接口文档
```

---

## 成员 B 自检清单

完成后请检查：

```text
[ ] Flask 能启动
[ ] /api/dashboard 能返回 JSON
[ ] /api/predict 能接收 JSON 并返回预测结果
[ ] /api/analysis/cancel-rate 能返回图表数据
[ ] /api/bigdata/status 能返回大数据流程说明
[ ] 数据库表能创建
[ ] 清洗后数据能导入数据库
[ ] 代码没有私自改字段名
[ ] 接口返回格式和接口文档一致
```
