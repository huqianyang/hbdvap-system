---
name: task-plan
description: 当前课程设计工作的阶段性任务计划
metadata:
  type: project
---

# 任务计划

## 当前目标
围绕《数据可视化》期末课程设计，补齐项目过程文件，随后继续完善项目内容与配置，确保后续讨论有清晰的记录基线。

## 已确认方向
- 题目采用酒店预订数据可视化分析与预测系统
- 数据集采用 Kaggle Hotel Booking Demand
- 技术路线围绕 Flask + HTML + Tailwind + jQuery + PyECharts，并结合 Flume+Kafka+Storm
- 用户当前关注点包含项目结构、过程文件与配置稳定性

## 当前阶段任务
1. 补齐过程文件：`task_plan.md`、`findings.md`、`progress.md`
2. 保持项目级 `.claude/settings.json` 为完整 29 hook 结构
3. 按用户需要继续补全课程设计相关文档

## 待确认/待推进事项
- 是否继续完善课程设计的最终文档包
- 是否需要对现有 `README.md`、`课程设计要求.md` 做统一整理
- 是否继续补充项目结构、分工说明或接口文档

## 启动包文档阶段

### 已完成
- 创建 `00_project_docs/` 和 `07_ai_prompts/` 启动包目录
- 完成项目总说明
- 完成项目目录结构
- 完成字段规范
- 完成接口文档
- 完成数据流架构说明
- 完成开发时间表
- 完成小组分工说明
- 完成成员 A/B/C 的 AI 提示词

### 启动包文件清单
- `00_project_docs/项目总说明.md`
- `00_project_docs/项目目录结构.md`
- `00_project_docs/字段规范.md`
- `00_project_docs/接口文档.md`
- `00_project_docs/数据流架构说明.md`
- `00_project_docs/开发时间表.md`
- `00_project_docs/小组分工说明.md`
- `07_ai_prompts/成员A_数据算法提示词.md`
- `07_ai_prompts/成员B_后端大数据提示词.md`
- `07_ai_prompts/成员C_前端可视化提示词.md`

### 下一步建议
1. 组长 A 先检查启动包文档内容是否符合实际想法。
2. 将数据集 `hotel_bookings.csv` 与上述文档一起打包发给 B/C。
3. A 开始执行数据清洗和模型训练。
4. B 根据后端提示词生成 Flask、MySQL、大数据模块。
5. C 根据前端提示词生成页面和图表。

## 状态
- 启动包文档已完成
- 下一阶段可进入项目目录初始化、数据清洗和模型训练
