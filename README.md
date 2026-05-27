# 酒店预订数据可视化分析与预测系统

**项目简称**：HBDVAP System  
**英文名**：Hotel Booking Data Visualization Analysis & Prediction System

> 本文件是项目入口说明。详细协作规范以 `00_project_docs/` 下的文档为准；AI 提示词以 `07_ai_prompts/` 下的文档为准。

## 1. 项目概述

本项目是《数据可视化》期末课程设计，基于 Kaggle [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) 数据集构建酒店预订取消预测与可视化分析系统。系统围绕“数据采集、实时处理、机器学习预测、数据库存储、后端接口、前端可视化”形成完整流程。

核心目标：

1. 基于历史酒店预订数据训练二分类模型，预测新预订是否可能取消。
2. 使用 Flume + Kafka + Storm 描述并实现课程要求的大数据流处理架构。
3. 使用 Flask 提供后端 API。
4. 使用 HTML + Tailwind CSS + jQuery + ECharts/PyECharts 实现可视化展示。

## 2. 核心功能

1. **预订取消预测**：输入一条预订信息，输出取消概率、风险等级和建议。
2. **实时统计分析**：通过 Storm 或模拟流程统计取消率、订单量、热门地区、客户类型等指标。
3. **多维度可视化**：展示时间趋势、酒店类型、国家/地区、客户类型等图表。
4. **数据管理**：完成数据清洗、入库、查询和预测结果保存。

## 3. 技术架构

```text
01_data/raw/hotel_bookings.csv
    ↓
Flume 数据采集
    ↓
Kafka 消息队列缓冲
    ↓
Storm 实时处理
    ├── 数据清洗 Bolt
    ├── 模型预测 Bolt
    └── 实时统计 Bolt
    ↓
MySQL 数据库存储
    ↓
Flask API 后端接口
    ↓
Web 前端可视化页面
```

## 4. 技术栈

| 层级 | 技术 | 说明 |
|---|---|---|
| 数据处理 | Python、Pandas、NumPy | 数据清洗、特征工程、EDA |
| 机器学习 | Scikit-learn | 预订取消二分类模型 |
| 大数据框架 | Flume、Kafka、Storm | 课程要求的数据采集、消息队列、实时处理架构 |
| 数据库 | MySQL | 存储清洗数据、统计结果、预测记录 |
| 后端 | Flask、SQLAlchemy | API 接口、模型调用、数据库查询 |
| 前端 | HTML、Tailwind CSS、jQuery | 页面结构、样式和交互 |
| 可视化 | ECharts / PyECharts | 图表展示 |

## 5. 项目目录

正式目录结构以 `00_project_docs/项目目录结构.md` 为准，当前推荐结构如下：

```text
hotel_booking_visualization_prediction/
├── README.md
├── requirements.txt
├── .gitignore
├── 00_project_docs/        # 项目说明、字段规范、接口文档、分工、时间表
├── 01_data/                # 原始数据、清洗后数据、EDA、数据处理脚本
├── 02_model/               # 模型训练、评估、模型文件、预测示例
├── 03_backend/             # Flask 后端、数据库、API、模型调用
├── 04_frontend/            # HTML 页面、CSS、JS、图表
├── 05_bigdata/             # Flume、Kafka、Storm 配置与模拟流程
├── 06_reports/             # 课程报告、PPT、截图
└── 07_ai_prompts/          # A/B/C 成员使用的 AI 提示词
```

## 6. 数据文件位置

原始数据集文件统一放在：

```text
01_data/raw/hotel_bookings.csv
```

说明：

1. 不要把 `hotel_bookings.csv` 放到项目根目录。
2. 不要把原始 CSV 提交到 Git；仓库通过 `.gitignore` 忽略数据文件。
3. 每位成员在本地按上述路径放置数据集，保证数据清洗和大数据演示脚本可以直接运行。
4. 如果成员缺少数据集，从 Kaggle [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) 下载后重命名为 `hotel_bookings.csv`。

## 7. 安装与启动

以下命令默认在项目根目录执行。Windows 环境建议使用 PowerShell 或 Git Bash。

### 7.1 创建 Python 环境

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

Git Bash：

```bash
source .venv/Scripts/activate
```

### 7.2 安装依赖

当前依赖文件位于后端目录：

```bash
pip install -r 03_backend/requirements.txt
```

如果后续补充根目录 `requirements.txt`，也可以统一改为从根目录安装。

### 7.3 准备数据集

1. 从 Kaggle [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) 下载数据集。
2. 解压后确认 CSV 文件名为 `hotel_bookings.csv`。
3. 放到以下路径：

```text
01_data/raw/hotel_bookings.csv
```

### 7.4 生成清洗数据和特征数据

```bash
python 01_data/scripts/data_cleaning.py
python 01_data/scripts/eda_analysis.py
python 01_data/scripts/feature_engineering.py
```

运行后会生成：

```text
01_data/processed/hotel_bookings_clean.csv
01_data/processed/model_features.csv
01_data/eda/*.csv
02_model/feature_columns.json
```

### 7.5 训练和验证模型

```bash
python 02_model/train_model.py
python 02_model/evaluate_model.py
python 02_model/predict_demo.py
```

运行后会生成：

```text
02_model/cancellation_model.pkl
02_model/model_metrics.json
```

### 7.6 启动 Flask 后端

```bash
python 03_backend/app.py
```

默认服务地址：

```text
http://127.0.0.1:5000
```

### 7.7 运行大数据流程演示

```bash
cd 05_bigdata
python scripts/run_pipeline_demo.py
```

该脚本会模拟 CSV → Flume → Kafka → Storm 的处理流程。真实 Flume、Kafka、Storm 配置见 `05_bigdata/README.md`。

## 8. 小组分工

| 成员 | 角色 | 负责目录 | 主要任务 |
|---|---|---|---|
| A | 组长 + 数据算法工程师 | `00_project_docs/`、`01_data/`、`02_model/`、`07_ai_prompts/` | 数据清洗、特征工程、模型训练、规范文档、整体协调 |
| B | 后端 + 大数据工程师 | `03_backend/`、`05_bigdata/` | Flask、MySQL、API、模型调用、Flume/Kafka/Storm 模块 |
| C | 前端 + 可视化工程师 | `04_frontend/` | 页面、图表、预测表单、接口调用 |

## 9. 启动包阅读顺序

组员拿到项目后，按以下顺序阅读：

1. `README.md`：了解项目入口。
2. `00_project_docs/项目总说明.md`：了解项目背景、功能和技术路线。
3. `00_project_docs/项目目录结构.md`：确认自己负责哪个目录。
4. `00_project_docs/字段规范.md`：统一字段名，避免前后端和模型冲突。
5. `00_project_docs/接口文档.md`：统一 API 地址、请求格式和返回格式。
6. `00_project_docs/小组分工说明.md`：确认 A/B/C 职责边界。
7. `07_ai_prompts/成员B_后端大数据提示词.md` 或 `07_ai_prompts/成员C_前端可视化提示词.md`：复制给 AI 生成对应模块。

## 10. 详细文档入口

| 文档 | 用途 |
|---|---|
| `00_project_docs/项目总说明.md` | 项目完整说明 |
| `00_project_docs/项目目录结构.md` | 唯一正式目录结构 |
| `00_project_docs/字段规范.md` | 数据、模型、接口、前端字段统一规范 |
| `00_project_docs/接口文档.md` | Flask API 契约 |
| `00_project_docs/数据流架构说明.md` | Flume + Kafka + Storm 架构说明 |
| `00_project_docs/开发时间表.md` | 阶段计划和交付物 |
| `00_project_docs/小组分工说明.md` | 成员职责边界 |
| `07_ai_prompts/成员A_数据算法提示词.md` | A 的数据算法开发提示词 |
| `07_ai_prompts/成员B_后端大数据提示词.md` | B 的后端和大数据开发提示词 |
| `07_ai_prompts/成员C_前端可视化提示词.md` | C 的前端可视化开发提示词 |

## 11. 当前开发顺序

1. 组长 A 检查启动包文档。
2. 将 `hotel_bookings.csv` 放到 `01_data/raw/hotel_bookings.csv`；原始 CSV 不提交到 Git，只随说明发给 B/C。
3. A 完成数据清洗、特征工程、模型训练。
4. B 按接口文档生成 Flask 后端、大数据模块和数据库脚本。
5. C 按接口文档生成前端页面和图表。
6. A/B/C 联调预测接口、图表接口和大数据流程说明。
7. 汇总报告、PPT 和运行截图。

## 12. 大数据组件说明

Flume、Kafka、Storm 是课程要求的一部分，不能作为可选模块删除。本项目中：

- Flume：负责采集 CSV 或日志形式的酒店预订数据。
- Kafka：负责消息队列缓冲。
- Storm：负责实时清洗、预测和统计。

如果真实组件配置困难，可以先实现 `05_bigdata/` 下的配置文件和 Python 模拟流程，但报告和答辩中必须体现完整 Flume → Kafka → Storm 架构。

## 13. 协作规则

1. 以 `00_project_docs/项目目录结构.md` 为唯一正式目录标准。
2. 字段改动必须先更新 `00_project_docs/字段规范.md`。
3. 接口改动必须先更新 `00_project_docs/接口文档.md`。
4. B/C 只修改自己负责的目录。
5. 可以使用不同 AI 工具，但必须使用统一提示词。

## 14. 许可证

本项目仅供课程学习与展示使用。

**最后更新**：2026-05-26
