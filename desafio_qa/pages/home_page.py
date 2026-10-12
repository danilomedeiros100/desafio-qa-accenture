from __future__ import annotations

from desafio_qa.pages.base_page import PaginaBase
from desafio_qa.support import terminal


class PaginaInicial(PaginaBase):
    CAMINHO = "/"

    def escolher_card(self, nome: str) -> None:
        terminal.acao(f"Clicando no card '{nome}'")
        card = self.pagina.locator(".card").filter(has=self.pagina.get_by_text(nome, exact=True))
        self.clicar_com_seguranca(card.first)


class MenuLateral(PaginaBase):
    """Menu lateral presente em todas as páginas internas."""

    def clicar_item(self, nome: str) -> None:
        terminal.acao(f"Clicando no item '{nome}' do menu lateral")
        # clica no link: o <li> é mais largo que o <a> e o clique no centro dele não navega
        link = self.pagina.locator(".element-list li a").filter(
            has=self.pagina.get_by_text(nome, exact=True)
        )
        self.clicar_com_seguranca(link.first)
