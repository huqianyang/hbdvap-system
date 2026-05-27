(function ($) {
  const charts = {};

  function setStatus(id, text, isError) {
    $("#" + id)
      .text(text)
      .toggleClass("is-error", Boolean(isError));
  }

  function getChart(id) {
    const element = document.getElementById(id);
    if (!element || !window.echarts) {
      return null;
    }
    charts[id] = charts[id] || echarts.init(element);
    return charts[id];
  }

  function handleFailure(statusId) {
    setStatus(statusId, "加载失败", true);
    $("#analysisError").attr("hidden", false);
  }

  function loadJson(path, statusId, renderer) {
    setStatus(statusId, "加载中", false);
    return HBDVAP.request({
      url: HBDVAP.apiBase + path,
      method: "GET"
    })
      .done(function (res) {
        if (!res || !res.success || !res.data) {
          handleFailure(statusId);
          return;
        }
        renderer(res.data);
        setStatus(statusId, "已加载", false);
      })
      .fail(function () {
        handleFailure(statusId);
      });
  }

  function renderCancelRate(data) {
    const chart = getChart("cancelRateChart");
    if (!chart) return;

    chart.setOption({
      color: ["#d45532", "#134e4a"],
      tooltip: { trigger: "axis" },
      legend: { top: 0, right: 0 },
      grid: { top: 46, right: 32, bottom: 36, left: 58 },
      xAxis: {
        type: "category",
        data: data.x_axis || [],
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "#d7c8b5" } },
        axisLabel: { color: "#475467", fontWeight: 700 }
      },
      yAxis: [
        {
          type: "value",
          name: "取消率",
          axisLabel: { formatter: "{value}", color: "#667085" },
          splitLine: { lineStyle: { color: "#eee3d4" } }
        },
        {
          type: "value",
          name: "订单量",
          axisLabel: { color: "#667085" },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: "取消率",
          type: "line",
          smooth: true,
          symbolSize: 8,
          data: data.cancel_rate || [],
          tooltip: {
            valueFormatter: function (value) {
              return HBDVAP.formatPercent(value);
            }
          },
          areaStyle: { opacity: 0.12 }
        },
        {
          name: "订单量",
          type: "bar",
          yAxisIndex: 1,
          barWidth: 18,
          data: data.booking_count || [],
          tooltip: {
            valueFormatter: function (value) {
              return HBDVAP.formatNumber(value) + " 单";
            }
          }
        }
      ]
    });
  }

  function renderHotelType(data) {
    const chart = getChart("hotelTypeAnalysisChart");
    if (!chart) return;

    const hotels = data.map(function (item) { return item.hotel; });
    chart.setOption({
      color: ["#134e4a", "#d45532"],
      tooltip: { trigger: "axis" },
      legend: { top: 0, right: 0 },
      grid: { top: 48, right: 24, bottom: 34, left: 60 },
      xAxis: { type: "category", data: hotels, axisTick: { show: false } },
      yAxis: [
        { type: "value", name: "订单量", splitLine: { lineStyle: { color: "#eee3d4" } } },
        { type: "value", name: "取消率", splitLine: { show: false } }
      ],
      series: [
        {
          name: "订单量",
          type: "bar",
          data: data.map(function (item) { return item.booking_count; }),
          itemStyle: { borderRadius: [8, 8, 0, 0] }
        },
        {
          name: "取消率",
          type: "line",
          yAxisIndex: 1,
          data: data.map(function (item) { return item.cancel_rate; }),
          tooltip: {
            valueFormatter: function (value) {
              return HBDVAP.formatPercent(value);
            }
          }
        }
      ]
    });
  }

  function renderCountry(data) {
    const chart = getChart("countryChart");
    if (!chart) return;

    const topData = data.slice(0, 8);
    chart.setOption({
      color: ["#1d4ed8"],
      tooltip: {
        trigger: "axis",
        valueFormatter: function (value) {
          return HBDVAP.formatNumber(value) + " 单";
        }
      },
      grid: { top: 24, right: 22, bottom: 34, left: 72 },
      xAxis: { type: "value", splitLine: { lineStyle: { color: "#eee3d4" } } },
      yAxis: {
        type: "category",
        data: topData.map(function (item) { return item.country; }).reverse(),
        axisTick: { show: false }
      },
      series: [
        {
          name: "订单量",
          type: "bar",
          data: topData.map(function (item) { return item.booking_count; }).reverse(),
          itemStyle: { borderRadius: [0, 8, 8, 0] },
          label: { show: true, position: "right" }
        }
      ]
    });
  }

  function renderCustomerType(data) {
    const chart = getChart("customerTypeChart");
    if (!chart) return;

    chart.setOption({
      color: ["#134e4a", "#c18a2d", "#d45532", "#1d4ed8"],
      tooltip: {
        trigger: "item",
        formatter: function (params) {
          const item = data[params.dataIndex] || {};
          return params.name + "<br>订单量：" + HBDVAP.formatNumber(item.booking_count) + "<br>取消率：" + HBDVAP.formatPercent(item.cancel_rate);
        }
      },
      series: [
        {
          name: "客户类型",
          type: "pie",
          radius: ["42%", "70%"],
          center: ["50%", "54%"],
          avoidLabelOverlap: true,
          itemStyle: { borderColor: "#fffaf2", borderWidth: 3 },
          label: { formatter: "{b}\n{d}%" },
          data: data.map(function (item) {
            return { name: item.customer_type, value: item.booking_count };
          })
        }
      ]
    });
  }

  function renderBigdataStatus(data) {
    $("#flumeStatus").text(data.flume || "未返回");
    $("#kafkaStatus").text(data.kafka || "未返回");
    $("#stormStatus").text(data.storm || "未返回");
    $("#pipelineStatus").text(data.pipeline || "未返回");
  }

  function loadAnalysis() {
    $("#analysisError").attr("hidden", true);
    loadJson("/api/analysis/cancel-rate", "cancelRateStatus", renderCancelRate);
    loadJson("/api/analysis/hotel-type", "hotelTypeStatus", renderHotelType);
    loadJson("/api/analysis/country", "countryStatus", renderCountry);
    loadJson("/api/analysis/customer-type", "customerTypeStatus", renderCustomerType);
    loadJson("/api/bigdata/status", "pipelineStatus", renderBigdataStatus);
  }

  $(function () {
    loadAnalysis();
    $("#refreshAnalysis").on("click", loadAnalysis);
    $(window).on("resize", function () {
      Object.keys(charts).forEach(function (key) {
        charts[key].resize();
      });
    });
  });
})(jQuery);
