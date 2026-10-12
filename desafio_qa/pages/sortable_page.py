from __future__ import annotations

import random

from playwright.sync_api import expect

from desafio_qa.pages.base_page import PaginaBase
from desafio_qa.support import terminal

NUMEROS_POR_EXTENSO = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6}

# Alternativa: a lista usa react-dnd com backend HTML5. Caso o drag nativo do Playwright
# não seja reconhecido, disparamos a sequência de DragEvents diretamente.
_ARRASTAR_HTML5_JS = """
async ([seletor, de, para]) => {
  const itens = () => [...document.querySelectorAll(seletor)];
  const origem = itens()[de], destino = itens()[para];
  const dt = new DataTransfer();
  const ro = origem.getBoundingClientRect(), rd = destino.getBoundingClientRect();
  const y = para > de ? rd.y + rd.height - 5 : rd.y + 5;
  const disparar = (el, tipo, r, cy) => el.dispatchEvent(new DragEvent(tipo, {
      bubbles: true, cancelable: true, dataTransfer: dt,
      clientX: r.x + r.width / 2, clientY: cy }));
  const esperar = ms => new Promise(r => setTimeout(r, ms));
  disparar(origem, 'dragstart', ro, ro.y + ro.height / 2); await esperar(50);
  disparar(destino, 'dragenter', rd, y); disparar(destino, 'dragover', rd, y); await esperar(50);
  disparar(destino, 'drop', rd, y); disparar(origem, 'dragend', ro, y); await esperar(100);
}
"""


class PaginaOrdenavel(PaginaBase):
    CAMINHO = "/sortable"
    ITENS = "#demo-tabpane-list .list-group-item"

    def aguardar_lista(self) -> None:
        """A lista é renderizada pelo React depois da navegação: aguarda os 6 itens."""
        expect(self.pagina.locator(self.ITENS)).to_have_count(len(NUMEROS_POR_EXTENSO))

    def textos(self) -> list[str]:
        return [t.strip() for t in self.pagina.locator(self.ITENS).all_inner_texts()]

    def mover(self, de: int, para: int) -> None:
        if de == para:
            return
        rotulo = self.textos()[de]
        itens = self.pagina.locator(self.ITENS)
        destino = itens.nth(para)
        caixa = destino.bounding_box()
        # descendo: solta perto da borda inferior; subindo: perto da borda superior
        y = caixa["height"] - 5 if para > de else 5
        itens.nth(de).drag_to(destino, target_position={"x": caixa["width"] / 2, "y": y})

        if self.textos()[para] != rotulo:
            self.pagina.evaluate(_ARRASTAR_HTML5_JS, [self.ITENS, de, para])

        atual = self.textos()
        assert atual[para] == rotulo, f"Falha ao mover '{rotulo}' para a posição {para}: {atual}"
        terminal.acao(f"Arrastou '{rotulo}' da posição {de + 1} para {para + 1}: {atual}")

    def organizar(self, ordem_desejada: list[str]) -> None:
        """Selection sort usando drag and drop: coloca cada item na sua posição final."""
        for i, rotulo in enumerate(ordem_desejada):
            j = self.textos().index(rotulo)
            if j != i:
                self.mover(j, i)

    def embaralhar(self) -> list[str]:
        self.aguardar_lista()
        atual = self.textos()
        crescente = sorted(atual, key=NUMEROS_POR_EXTENSO.get)
        ordem = atual[:]
        while ordem == crescente:
            random.shuffle(ordem)
        terminal.acao(f"Embaralhando a lista para a ordem {ordem}")
        self.organizar(ordem)
        return ordem

    def ordenar_crescente(self) -> None:
        self.aguardar_lista()
        terminal.acao(f"Ordenando a lista {self.textos()} em ordem crescente")
        self.organizar(sorted(self.textos(), key=NUMEROS_POR_EXTENSO.get))

    def esta_em_ordem_crescente(self) -> bool:
        valores = [NUMEROS_POR_EXTENSO[t] for t in self.textos()]
        return valores == sorted(valores)
