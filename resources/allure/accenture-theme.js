/* Faixa "Accenture QA Report" no topo da Visão geral do Allure (injetada após o `allure generate`). */
(function () {
  function resumo() {
    var chips = [];
    var titulo = document.querySelector(".widget__title");
    var total = document.querySelector(".splash__title");
    if (total) chips.push({ texto: total.textContent.trim() + " cenários" });
    var falhas = document.querySelectorAll(".chart__arc_status_failed, .chart__arc_status_broken").length;
    chips.push(falhas
      ? { texto: "Há cenários com falha", classe: "acn-banner__chip_falha" }
      : { texto: "Todos os cenários passaram", classe: "acn-banner__chip_sucesso" });
    var subtitulo = titulo && titulo.querySelector(".widget__subtitle");
    if (subtitulo) chips.push({ texto: subtitulo.textContent.trim() });
    return chips;
  }

  function criarFaixa() {
    var faixa = document.createElement("section");
    faixa.className = "acn-banner";
    var chips = resumo().concat([
      { texto: "API + Front-end" }, { texto: "Python · Behave (BDD) · Playwright" },
    ]);
    faixa.innerHTML =
      '<div class="acn-banner__icone"></div>' +
      "<div>" +
      '<h1 class="acn-banner__titulo">Accenture QA Report</h1>' +
      '<p class="acn-banner__subtitulo">Desafio QA Automation Engineer · demoqa.com</p>' +
      '<div class="acn-banner__chips">' +
      chips.map(function (c) {
        return '<span class="acn-banner__chip ' + (c.classe || "") + '"></span>';
      }).join("") +
      "</div></div>" +
      '<div class="acn-banner__marca"></div>';
    faixa.querySelectorAll(".acn-banner__chip").forEach(function (el, i) {
      el.textContent = chips[i].texto;
    });
    return faixa;
  }

  function aplicar() {
    var grade = document.querySelector(".widgets-grid");
    if (!grade || !document.querySelector(".splash__title")) return;
    if (grade.previousElementSibling && grade.previousElementSibling.classList.contains("acn-banner")) return;
    var faixa = criarFaixa();
    grade.parentNode.insertBefore(faixa, grade);
    // a grade de widgets é "position: absolute" ocupando a área toda: desloca para baixo da faixa
    var posicionar = function () { grade.style.top = faixa.offsetTop + faixa.offsetHeight + "px"; };
    posicionar();
    if (window.ResizeObserver) new ResizeObserver(posicionar).observe(faixa);
  }

  new MutationObserver(aplicar).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener("DOMContentLoaded", aplicar);
})();
