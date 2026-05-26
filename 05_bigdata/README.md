# 大数据模块说明

本目录用于课程设计中展示 Flume + Kafka + Storm 的实时数据流处理架构。项目数据源来自酒店预订 CSV，整体流程为：

```text
CSV -> Flume -> Kafka -> Storm -> MySQL -> Flask -> Web
```

## 组件职责

- Flume：负责采集 CSV 或日志形式的酒店预订数据。
- Kafka：负责消息队列缓冲，解耦采集端和实时处理端。
- Storm：负责实时清洗、预测和统计。
- MySQL：保存清洗数据、预测结果和实时统计结果。
- Flask：提供接口给前端可视化页面调用。

## Windows 单机演示

课程环境下如果不方便启动真实 Flume、Kafka、Storm，可以运行 Python 模拟流程：

```powershell
cd 05_bigdata
python scripts/run_pipeline_demo.py
```

脚本会逐行读取 CSV，模拟 Flume 采集、Kafka 发送、Storm Bolt 清洗/预测/统计，并输出结果 CSV。默认优先读取：

```text
../01_data/raw/hotel_bookings.csv
```

如果原始数据不存在，会使用 `flume/sample_source_data.csv` 作为演示数据。

## 真实组件参考命令

创建 Kafka Topic：

```powershell
kafka-topics.bat --create --topic hotel_booking_stream --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

启动 Flume：

```powershell
flume-ng agent --conf conf --conf-file flume/flume_hotel_booking.conf --name a1
```

运行模拟生产者：

```powershell
python kafka/producer_simulator.py
```

运行消费测试：

```powershell
python kafka/consumer_test.py
```

## 输出字段

预测输出与后端接口保持一致：

- `is_canceled_pred`
- `cancel_probability`
- `risk_level`
- `suggestion`

这些字段对应 `00_project_docs/字段规范.md` 和 `00_project_docs/接口文档.md`。
