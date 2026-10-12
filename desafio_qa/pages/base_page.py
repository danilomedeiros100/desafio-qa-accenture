from __future__ import annotations

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from desafio_qa.config import URL_BASE
from desafio_qa.support import terminal


class PaginaBase:
    CAMINHO = "/"

    def __init__(self, pagina: Page):
        self.pagina = pagina

    def abrir(self):
        url = f"{URL_BASE}{self.CAMINHO}"
        terminal.acao(f"Acessando {url}")
        self.pagina.goto(url, wait_until="domcontentloaded")
        return self

    @staticmethod
    def clicar_com_seguranca(elemento: Locator, timeout: int = 5000) -> None:
        """Clique normal; se algum overlay (anúncio/rodapé) interceptar, dispara o evento direto."""
        elemento.scroll_into_view_if_needed()
        try:
            elemento.click(timeout=timeout)
        except PlaywrightTimeoutError:
            terminal.acao("Clique interceptado por overlay; disparando o evento de clique diretamente")
            elemento.dispatch_event("click")
