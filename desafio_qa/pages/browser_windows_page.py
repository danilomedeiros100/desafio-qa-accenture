from __future__ import annotations

from playwright.sync_api import Page

from desafio_qa.pages.base_page import PaginaBase
from desafio_qa.support import terminal

BOTOES = {
    "New Tab": "#tabButton",
    "New Window": "#windowButton",
    "New Window Message": "#messageWindowButton",
}


class PaginaJanelasNavegador(PaginaBase):
    CAMINHO = "/browser-windows"

    def abrir_nova_janela(self, botao: str = "New Window") -> Page:
        terminal.acao(f"Clicando no botão '{botao}' e aguardando a nova janela")
        with self.pagina.context.expect_page() as info_nova_pagina:
            self.pagina.locator(BOTOES[botao]).click()
        nova_pagina = info_nova_pagina.value
        nova_pagina.wait_for_load_state("domcontentloaded")
        terminal.acao(f"Nova janela aberta em {nova_pagina.url}")
        return nova_pagina


class PaginaExemplo(PaginaBase):
    CAMINHO = "/sample"

    @property
    def titulo(self):
        return self.pagina.locator("#sampleHeading")
