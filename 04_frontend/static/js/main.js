(function ($) {
  const API_BASE = "";

  // 统一封装接口请求，后续页面复用，确保只调用接口文档规定的 API。
  window.HBDVAP = {
    apiBase: API_BASE,
    request: function (options) {
      return $.ajax(
        Object.assign(
          {
            dataType: "json",
            contentType: "application/json",
            timeout: 6000
          },
          options
        )
      );
    },
    formatPercent: function (value) {
      const number = Number(value || 0);
      return (number * 100).toFixed(2) + "%";
    },
    formatNumber: function (value) {
      return Number(value || 0).toLocaleString("zh-CN");
    }
  };

  function markActiveNav() {
    const path = window.location.pathname.replace(/\/$/, "") || "/";
    $(".nav-links a").each(function () {
      const href = $(this).attr("href").replace(/\/$/, "") || "/";
      $(this).toggleClass("is-active", href === path);
    });
  }

  function checkApiStatus() {
    const $status = $("#apiStatus");

    HBDVAP.request({
      url: API_BASE + "/api/bigdata/status",
      method: "GET"
    })
      .done(function (res) {
        if (res && res.success) {
          $status.text("API 已连接").addClass("is-online").removeClass("is-offline");
          if (res.data && res.data.pipeline) {
            $("#pipelineSummary").text(res.data.pipeline);
          }
          return;
        }
        $status.text("API 返回异常").addClass("is-offline").removeClass("is-online");
      })
      .fail(function () {
        // 后端未启动时保留清晰占位，不伪造最终业务数据。
        $status.text("API 未连接").addClass("is-offline").removeClass("is-online");
      });
  }

  $(function () {
    markActiveNav();
    checkApiStatus();
  });
})(jQuery);
