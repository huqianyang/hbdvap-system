# 成员A_数据算法提示词

下面提示词给成员 A（组长）自己使用，可以复制到 Claude/Codex/豆包等 AI 工具中，让 AI 帮助完成数据清洗、特征工程和模型训练。

---

## 提示词 1：数据探索与清洗

```text
你现在是数据分析与机器学习工程师，请帮我完成《酒店预订数据可视化分析与预测系统》的数据清洗工作。

项目背景：
- 数据集：Kaggle Hotel Booking Demand
- 文件名：hotel_bookings.csv
- 目标字段：is_canceled，0=未取消，1=取消
- 项目目标：预测酒店预订是否会取消，并为 Flask 后端和前端可视化提供数据

要求：
1. 使用 Python + Pandas 编写脚本。
2. 读取 01_data/raw/hotel_bookings.csv。
3. 输出数据基本信息：行数、列数、字段类型、缺失值统计。
4. 处理缺失值：children 填 0，country 填 Unknown，agent/company 可填 0 或删除 company。
5. 不要使用 reservation_status 和 reservation_status_date 作为模型特征，因为它们会泄露预测结果。
6. 生成清洗后数据：01_data/processed/hotel_bookings_clean.csv。
7. 代码保存为：01_data/scripts/data_cleaning.py。
8. 代码要有中文注释，适合课程设计展示。

请给出完整代码和运行方法。
```

---

## 提示词 2：特征工程

```text
你现在是机器学习特征工程师，请基于清洗后的酒店预订数据完成特征工程。

输入文件：01_data/processed/hotel_bookings_clean.csv
目标字段：is_canceled
禁止用于模型的字段：reservation_status、reservation_status_date

建议使用字段：
hotel, lead_time, arrival_date_month, stays_in_weekend_nights, stays_in_week_nights,
adults, children, babies, meal, country, market_segment, distribution_channel,
is_repeated_guest, previous_cancellations, previous_bookings_not_canceled,
reserved_room_type, booking_changes, deposit_type, days_in_waiting_list,
customer_type, adr, required_car_parking_spaces, total_of_special_requests

要求：
1. 对分类字段做 One-Hot 编码或适合 scikit-learn 的编码。
2. 对数值字段进行必要的缺失值处理。
3. 拆分 X 和 y。
4. 保存特征处理后的数据为 01_data/processed/model_features.csv。
5. 保存模型实际使用的特征列到 02_model/feature_columns.json。
6. 代码保存为 01_data/scripts/feature_engineering.py。
7. 代码要有中文注释。

请给出完整代码和运行方法。
```

---

## 提示词 3：模型训练与评估

```text
你现在是机器学习工程师，请为《酒店预订数据可视化分析与预测系统》训练一个预订取消预测模型。

输入文件：01_data/processed/model_features.csv
目标字段：is_canceled
任务类型：二分类

要求：
1. 使用 Python + Scikit-learn。
2. 划分训练集和测试集。
3. 至少训练一个可解释、稳定的模型，比如 RandomForestClassifier 或 LogisticRegression。
4. 输出准确率、召回率、F1 值、混淆矩阵。
5. 保存模型为 02_model/cancellation_model.pkl。
6. 保存评估结果为 02_model/model_metrics.json。
7. 编写 02_model/predict_demo.py，演示如何加载模型并预测一条新预订数据。
8. 代码要有中文注释。

请给出完整代码和运行方法。
```
