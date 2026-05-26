from collections import Counter


class RealtimeStats:
    """Storm 统计 Bolt：维护订单数、预测取消数和维度分布。"""

    def __init__(self):
        self.booking_count = 0
        self.predicted_cancel_count = 0
        self.hotel_counter = Counter()
        self.country_counter = Counter()
        self.customer_type_counter = Counter()

    def update(self, row):
        self.booking_count += 1
        if int(row.get("is_canceled_pred", 0)) == 1:
            self.predicted_cancel_count += 1

        self.hotel_counter[row.get("hotel", "Unknown")] += 1
        self.country_counter[row.get("country", "Unknown")] += 1
        self.customer_type_counter[row.get("customer_type", "Unknown")] += 1
        return self.snapshot()

    def snapshot(self):
        cancel_rate = 0
        if self.booking_count:
            cancel_rate = round(self.predicted_cancel_count / self.booking_count, 4)

        return {
            "booking_count": self.booking_count,
            "predicted_cancel_count": self.predicted_cancel_count,
            "cancel_rate": cancel_rate,
            "hotel_distribution": dict(self.hotel_counter),
            "country_distribution": dict(self.country_counter),
            "customer_type_distribution": dict(self.customer_type_counter),
        }


if __name__ == "__main__":
    stats = RealtimeStats()
    print(stats.update({"hotel": "City Hotel", "country": "PRT", "is_canceled_pred": 1}))
