def get_risk_level(cancel_probability):
    """按字段规范中的阈值生成风险等级。"""
    if cancel_probability < 0.30:
        return "低风险"
    if cancel_probability <= 0.70:
        return "中风险"
    return "高风险"


def get_suggestion(risk_level):
    suggestions = {
        "低风险": "客户取消概率较低，可按正常流程接待",
        "中风险": "建议关注客户预订变化，必要时提前沟通",
        "高风险": "建议酒店提前确认客户入住意愿",
    }
    return suggestions[risk_level]


def predict_booking(row):
    """
    Storm 预测 Bolt。
    课程单机演示中使用规则模拟；真实部署时可改为加载 02_model/cancellation_model.pkl。
    """
    probability = 0.25
    if int(row.get("lead_time", 0)) >= 90:
        probability += 0.25
    if row.get("deposit_type") == "Non Refund":
        probability += 0.25
    if int(row.get("previous_cancellations", 0)) > 0:
        probability += 0.15
    if int(row.get("total_of_special_requests", 0)) == 0:
        probability += 0.10
    if int(row.get("required_car_parking_spaces", 0)) > 0:
        probability -= 0.10

    cancel_probability = round(max(0.01, min(probability, 0.99)), 4)
    risk_level = get_risk_level(cancel_probability)
    return {
        "is_canceled_pred": 1 if cancel_probability > 0.50 else 0,
        "cancel_probability": cancel_probability,
        "risk_level": risk_level,
        "suggestion": get_suggestion(risk_level),
    }


if __name__ == "__main__":
    print(predict_booking({"lead_time": 120, "deposit_type": "No Deposit"}))
