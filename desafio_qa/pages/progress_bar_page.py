from __future__ import annotations

from playwright.sync_api import expect

from desafio_qa.pages.base_page import PaginaBase
from desafio_qa.support import terminal


class PaginaBarraProgresso(PaginaBase):
    CAMINHO = "/progress-bar"

    BOTAO_INICIAR_PARAR = "#startStopButton"
    BOTAO_RESETAR = "#resetButton"
    BARRA = "#progressBar [role='progressbar']"

    _VALOR_JS = "() => Number(document.querySelector(\"#progressBar [role='progressbar']\")" \
                ".getAttribute('aria-valuenow'))"

    def valor(self) -> int:
        return int(self.pagina.locator(self.BARRA).get_attribute("aria-valuenow"))

    def iniciar(self) -> None:
        terminal.acao(f"Clicando em 'Start' (valor atual: {self.valor()}%)")
        self.pagina.locator(self.BOTAO_INICIAR_PARAR).click()

    def parar_ao_atingir(self, limite: int) -> int:
        """Aguarda (polling por frame no browser) o valor atingir `limite` e clica em Stop.
        A barra avança ~1% a cada 100ms, então uma margem de alguns % evita a condição de corrida."""
        terminal.acao(f"Aguardando a barra atingir {limite}% para clicar em 'Stop'")
        self.pagina.wait_for_function(
            f"(t) => ({self._VALOR_JS})() >= t", arg=limite, polling="raf"
        )
        self.pagina.locator(self.BOTAO_INICIAR_PARAR).click()
        expect(self.pagina.locator(self.BOTAO_INICIAR_PARAR)).to_have_text("Start")
        # confirma que parou: o valor não muda mais
        antes = self.valor()
        self.pagina.wait_for_timeout(500)
        assert self.valor() == antes, "A barra de progresso continuou avançando após o Stop"
        terminal.acao(f"Barra parada em {antes}%")
        return antes

    def aguardar_conclusao(self, timeout_ms: int = 30000) -> None:
        terminal.acao("Aguardando a barra chegar a 100%")
        self.pagina.wait_for_function(
            f"() => ({self._VALOR_JS})() === 100", polling="raf", timeout=timeout_ms
        )

    def resetar(self) -> None:
        terminal.acao("Clicando em 'Reset'")
        botao_resetar = self.pagina.locator(self.BOTAO_RESETAR)
        expect(botao_resetar).to_be_visible()
        botao_resetar.click()
