(function ($) {
  let hotelTypeChart = null;

  function setStatus(text, isError) {
    $("#dashboardStatus")
      .text(text)
      .toggleClass("is-error", Boolean(isError));
  }

  function setMetric(id, value) {
    $("#" + id).text(value);
  }

  function renderMetrics(data) {
    setMetric("totalBookings", HBDVAP.formatNumber(data.total_bookings));
    setMetric("canceledBookings", HBDVAP.formatNumber(data.canceled_bookings));
    setMetric("cancelRate", HBDVAP.formatPercent(data.cancel_rate));
    setMetric("avgAdr", "¥" + Number(data.avg_adr || 0).toFixed(2));
    setMetric("topCountry", data.top_country || "--");
  }

  function renderHotelTypeChart(data) {
    const chartDom = document.getElementById("hotelTypeChart");
    if (!chartDom || !window.echarts) {
      return;
    }

    hotelTypeChart = hotelTypeChart || echarts.init(chartDom);
    hotelTypeChart.setOption({
      color: ["#134e4a", "#c18a2d"],
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" },
        valueFormatter: function (value) {
          return HBDVAP.formatNumber(value) + " 单";
        }
      },
      grid: {
        top: 34,
        right: 22,
        bottom: 34,
        left: 72
      },
      xAxis: {
        type: "category",
        data: ["City Hotel", "Resort Hotel"],
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "#d7c8b5" } },
        axisLabel: { color: "#475467", fontWeight: 700 }
      },
      yAxis: {
        type: "value",
        axisLabel: {
          color: "#667085",
          formatter: function (value) {
            return value >= 1000 ? value / 1000 + "k" : value;
          }
        },
        splitLine: { lineStyle: { color: "#eee3d4" } }
      },
      series: [
        {
          name: "预订量",
          type: "bar",
          barWidth: 48,
          data: [data.city_hotel_count || 0, data.resort_hotel_count || 0],
          itemStyle: { borderRadius: [8, 8, 0, 0] },
          label: {
            show: true,
            position: "top",
            color: "#18212f",
            fontWeight: 800,
            formatter: function (params) {
              return HBDVAP.formatNumber(params.value);
            }
          }
        }
      ]
    });
  }

  function loadDashboard() {
    setStatus("加载中", false);
    $("#dashboardError").attr("hidden", true);

    HBDVAP.request({
      url: HBDVAP.apiBase + "/api/dashboard",
      method: "GET"
    })
      .done(function (res) {
        if (!res || !res.success || !res.data) {
          setStatus("接口返回异常", true);
          $("#dashboardError").attr("hidden", false);
          return;
        }

        renderMetrics(res.data);
        renderHotelTypeChart(res.data);
        setStatus("已加载", false);
      })
      .fail(function () {
        setStatus("加载失败", true);
        $("#dashboardError").attr("hidden", false);
      });
  }

  $(function () {
    loadDashboard();
    $("#refreshDashboard").on("click", loadDashboard);
    $(window).on("resize", function () {
      if (hotelTypeChart) {
        hotelTypeChart.resize();
      }
    });
  });
})(jQuery);
