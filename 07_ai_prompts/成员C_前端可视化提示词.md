# 成员C_前端可视化提示词

下面内容请成员 C 直接复制到 Claude、Codex、豆包或 ChatGPT 中使用。生成代码前，必须同时提供以下文档给 AI：

1. `项目总说明.md`
2. `项目目录结构.md`
3. `字段规范.md`
4. `接口文档.md`
5. `数据流架构说明.md`

---

## 提示词 1：生成前端整体页面

```text
你现在是前端可视化开发工程师，请为《酒店预订数据可视化分析与预测系统》生成前端页面。

项目背景：
- 项目名称：酒店预订数据可视化分析与预测系统
- 核心功能：酒店预订取消预测、数据看板、多维分析、大数据流程展示
- 技术栈：HTML + Tailwind CSS + jQuery + ECharts
- 后端：Flask API

我负责的目录：
04_frontend/

必须遵守：
1. 只能开发 04_frontend 目录。
2. 所有数据必须通过接口文档中的 API 获取，不要直接读取 CSV。
3. 不要自己改接口地址、请求字段和返回字段。
4. 页面要适合课程设计答辩展示：清晰、美观、结构完整。
5. 代码要有中文注释。
6. 给出每个 HTML/CSS/JS 文件的完整代码。

请生成以下文件：
- templates/base.html
- templates/index.html
- templates/dashboard.html
- templates/prediction.html
- templates/analysis.html
- static/css/style.css
- static/js/main.js
- static/js/dashboard.js
- static/js/prediction.js
- static/js/charts.js

页面风格要求：
- 使用 Tailwind CSS
- 顶部导航栏
- 卡片式指标展示
- 图表区域清晰
- 预测结果用不同颜色展示低/中/高风险
- 响应式布局
```

---

## 提示词 2：生成首页数据看板

```text
你现在是数据可视化前端工程师，请为酒店预订数据可视化分析与预测系统生成首页看板页面。

接口：GET /api/dashboard
返回数据示例：
{
  "success": true,
  "data": {
    "total_bookings": 119390,
    "canceled_bookings": 44224,
    "cancel_rate": 0.3704,
    "avg_adr": 101.83,
    "city_hotel_count": 79330,
    "resort_hotel_count": 40060,
    "top_country": "PRT"
  }
}

要求：
1. 使用 jQuery 调用 /api/dashboard。
2. 用卡片展示总预订量、取消订单数、取消率、平均房价、主要客源国家。
3. 使用 ECharts 展示 City Hotel 和 Resort Hotel 的数量对比。
4. 页面文件为 templates/dashboard.html。
5. JS 文件为 static/js/dashboard.js。
6. 不要写死最终数据，必须通过 API 获取。
7. 代码要有中文注释。

请给出完整 HTML 和 JS 代码。
```

---

## 提示词 3：生成预测页面

```text
你现在是前端交互开发工程师，请为酒店预订取消预测功能生成预测页面。

接口：POST /api/predict
请求字段必须使用接口文档中的字段，包括：
hotel, lead_time, arrival_date_month, stays_in_weekend_nights, stays_in_week_nights,
adults, children, babies, meal, country, market_segment, distribution_channel,
is_repeated_guest, previous_cancellations, previous_bookings_not_canceled,
reserved_room_type, booking_changes, deposit_type, days_in_waiting_list,
customer_type, adr, required_car_parking_spaces, total_of_special_requests

响应字段：
is_canceled_pred, cancel_probability, risk_level, suggestion

要求：
1. 页面文件：templates/prediction.html
2. JS 文件：static/js/prediction.js
3. 使用表单收集输入字段。
4. 点击“开始预测”后，用 jQuery AJAX 调用 /api/predict。
5. 展示取消概率、风险等级、建议。
6. 风险等级用颜色区分：低风险绿色，中风险黄色，高风险红色。
7. 不要直接在前端计算预测结果，预测必须来自后端接口。
8. 代码要有中文注释。

请给出完整 HTML 和 JS 代码。
```

---

## 提示词 4：生成多维分析页面

```text
你现在是 ECharts 数据可视化工程师，请为酒店预订数据可视化分析与预测系统生成多维分析页面。

需要调用的接口：
GET /api/analysis/cancel-rate
GET /api/analysis/hotel-type
GET /api/analysis/country
GET /api/analysis/customer-type
GET /api/bigdata/status

页面文件：templates/analysis.html
JS 文件：static/js/charts.js

要求绘制：
1. 月度取消率趋势折线图
2. 酒店类型取消率柱状图
3. 国家/地区订单数量柱状图或饼图
4. 客户类型分布图
5. 大数据流程说明卡片：CSV -> Flume -> Kafka -> Storm -> MySQL -> Flask -> Web

要求：
- 使用 ECharts
- 使用 jQuery 调用接口
- 不要写死最终数据
- 页面布局清晰，适合答辩展示
- 代码要有中文注释

请给出完整 HTML 和 JS 代码。
```

---

## 成员 C 自检清单

完成后请检查：

```text
[ ] 页面能通过 Flask 正常访问
[ ] 首页指标能显示
[ ] 图表能正常渲染
[ ] 预测表单能提交
[ ] 预测结果能显示风险等级
[ ] 所有数据都来自后端 API
[ ] 没有私自改接口字段
[ ] 页面截图适合放进课程设计报告
```
