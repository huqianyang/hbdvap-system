(function ($) {
  const numericFields = new Set([
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "booking_changes",
    "days_in_waiting_list",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests"
  ]);

  function buildPayload($form) {
    const payload = {};
    $form.serializeArray().forEach(function (item) {
      payload[item.name] = numericFields.has(item.name) ? Number(item.value) : item.value;
    });
    return payload;
  }

  function setResultState(riskLevel) {
    const normalized = riskLevel || "";
    const $result = $("#predictionResult");
    $result.removeClass("risk-low risk-medium risk-high");

    if (normalized.includes("低")) {
      $result.addClass("risk-low");
    } else if (normalized.includes("中")) {
      $result.addClass("risk-medium");
    } else if (normalized.includes("高")) {
      $result.addClass("risk-high");
    }
  }

  function renderResult(data) {
    const probability = Number(data.cancel_probability || 0);
    const riskLevel = data.risk_level || "未知风险";

    setResultState(riskLevel);
    $("#riskLevel").text(riskLevel);
    $("#cancelProbability").text(HBDVAP.formatPercent(probability));
    $("#predictionLabel").text(data.is_canceled_pred === 1 ? "模型判断该订单存在取消风险。" : "模型判断该订单取消风险较低。");
    $("#suggestion").text(data.suggestion || "暂无建议");
    $("#predictionStatus").text("接口状态：预测成功");
  }

  function renderError(message) {
    setResultState("高风险");
    $("#riskLevel").text("预测失败");
    $("#cancelProbability").text("--");
    $("#predictionLabel").text("未获取到有效预测结果。");
    $("#suggestion").text(message || "请检查后端接口是否启动。");
    $("#predictionStatus").text("接口状态：请求失败");
  }

  $(function () {
    $("#predictionForm").on("submit", function (event) {
      event.preventDefault();

      const $form = $(this);
      const $button = $("#predictButton");
      const payload = buildPayload($form);

      $button.prop("disabled", true).text("预测中...");
      $("#predictionStatus").text("接口状态：正在请求 /api/predict");

      HBDVAP.request({
        url: HBDVAP.apiBase + "/api/predict",
        method: "POST",
        data: JSON.stringify(payload)
      })
        .done(function (res) {
          if (!res || !res.success || !res.data) {
            renderError(res && res.message ? res.message : "接口返回格式不符合约定。");
            return;
          }
          renderResult(res.data);
        })
        .fail(function () {
          renderError("无法连接 POST /api/predict，请确认 Flask 后端已启动。");
        })
        .always(function () {
          $button.prop("disabled", false).text("开始预测");
        });
    });
  });
})(jQuery);
