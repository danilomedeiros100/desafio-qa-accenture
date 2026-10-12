from __future__ import annotations

from playwright.sync_api import Locator, expect

from desafio_qa.data.factories import Funcionario
from desafio_qa.pages.base_page import PaginaBase
from desafio_qa.support import terminal

COLUNAS = ["nome", "sobrenome", "idade", "email", "salario", "departamento"]


class PaginaTabelasWeb(PaginaBase):
    CAMINHO = "/webtables"

    BOTAO_ADICIONAR = "#addNewRecordButton"
    MODAL = ".modal-content"
    LINHAS = "table tbody tr"
    SELETOR_TAMANHO_PAGINA = ".pagination select"

    # ---------------- ações ----------------
    def adicionar_registro(self, funcionario: Funcionario) -> None:
        terminal.acao(f"Adicionando o registro {funcionario}")
        self.clicar_com_seguranca(self.pagina.locator(self.BOTAO_ADICIONAR))
        self._preencher_modal(funcionario)

    def editar_registro(self, email_atual: str, novos_dados: Funcionario) -> None:
        terminal.acao(f"Editando o registro <{email_atual}> para {novos_dados}")
        self.clicar_com_seguranca(self.linha_por_email(email_atual).locator("span[id^='edit-record']"))
        self._preencher_modal(novos_dados)

    def excluir_registro(self, email: str) -> None:
        terminal.acao(f"Excluindo o registro <{email}>")
        linha = self.linha_por_email(email)
        self.clicar_com_seguranca(linha.locator("span[id^='delete-record']"))
        expect(linha).to_have_count(0)

    def definir_registros_por_pagina(self, quantidade: int) -> None:
        terminal.acao(f"Exibindo {quantidade} registros por página")
        self.pagina.locator(self.SELETOR_TAMANHO_PAGINA).select_option(str(quantidade))

    # ---------------- leitura ----------------
    def linha_por_email(self, email: str) -> Locator:
        return self.pagina.locator(self.LINHAS).filter(has_text=email)

    def dados_da_linha(self, email: str) -> dict:
        celulas = self.linha_por_email(email).first.locator("td").all_inner_texts()
        return {coluna: celulas[i].strip() for i, coluna in enumerate(COLUNAS)}

    def emails(self) -> list[str]:
        resultado = []
        for linha in self.pagina.locator(self.LINHAS).all():
            celulas = linha.locator("td").all_inner_texts()
            if len(celulas) > 3 and celulas[3].strip():
                resultado.append(celulas[3].strip())
        return resultado

    # ---------------- privados ----------------
    def _preencher_modal(self, f: Funcionario) -> None:
        modal = self.pagina.locator(self.MODAL)
        expect(modal).to_be_visible()
        modal.locator("#firstName").fill(f.nome)
        modal.locator("#lastName").fill(f.sobrenome)
        modal.locator("#userEmail").fill(f.email)
        modal.locator("#age").fill(f.idade)
        modal.locator("#salary").fill(f.salario)
        modal.locator("#department").fill(f.departamento)
        modal.locator("#submit").click()
        expect(modal).to_have_count(0)
