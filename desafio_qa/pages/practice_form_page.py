from __future__ import annotations

from datetime import date
from pathlib import Path

from playwright.sync_api import expect

from desafio_qa.data.factories import Estudante
from desafio_qa.pages.base_page import PaginaBase
from desafio_qa.support import terminal

INDICE_GENERO = {"Male": 1, "Female": 2, "Other": 3}
INDICE_HOBBY = {"Sports": 1, "Reading": 2, "Music": 3}


class PaginaFormularioPratica(PaginaBase):
    CAMINHO = "/automation-practice-form"

    TITULO_POPUP = "#example-modal-sizes-title-lg"
    BOTAO_FECHAR_POPUP = "#closeLargeModal"
    LINHAS_POPUP = ".modal-body tbody tr"
    OPCAO_AUTOCOMPLETE = "[id^='react-select'][id*='-option-']"

    def preencher(self, estudante: Estudante, arquivo_upload: Path) -> None:
        p = self.pagina
        self._preencher_campo("#firstName", "First Name", estudante.nome)
        self._preencher_campo("#lastName", "Last Name", estudante.sobrenome)
        self._preencher_campo("#userEmail", "Email", estudante.email)
        terminal.acao(f"Selecionando o gênero '{estudante.genero}'")
        # o input do radio fica escondido: clica no label
        p.locator(f"label[for='gender-radio-{INDICE_GENERO[estudante.genero]}']").click()
        self._preencher_campo("#userNumber", "Mobile", estudante.celular)
        self._selecionar_data_nascimento(estudante.data_nascimento)
        for materia in estudante.materias:
            terminal.acao(f"Adicionando a matéria '{materia}'")
            self._autocompletar("#subjectsInput", materia)
        for hobby in estudante.hobbies:
            terminal.acao(f"Marcando o hobby '{hobby}'")
            p.locator(f"label[for='hobbies-checkbox-{INDICE_HOBBY[hobby]}']").click()
        terminal.acao(f"Enviando o arquivo '{arquivo_upload.name}'")
        p.set_input_files("#uploadPicture", str(arquivo_upload))
        self._preencher_campo("#currentAddress", "Current Address", estudante.endereco)
        terminal.acao(f"Selecionando o estado '{estudante.estado}' e a cidade '{estudante.cidade}'")
        self._autocompletar("#state input", estudante.estado)
        self._autocompletar("#city input", estudante.cidade)

    def submeter(self) -> None:
        terminal.acao("Clicando em 'Submit'")
        self.clicar_com_seguranca(self.pagina.locator("#submit"))

    # ---------------- popup ----------------
    def validar_popup_aberto(self) -> None:
        expect(self.pagina.locator(self.TITULO_POPUP)).to_have_text("Thanks for submitting the form")
        terminal.acao("Popup 'Thanks for submitting the form' exibido")

    def valores_exibidos_no_popup(self) -> dict[str, str]:
        valores = {}
        for linha in self.pagina.locator(self.LINHAS_POPUP).all():
            celulas = linha.locator("td").all_inner_texts()
            if len(celulas) == 2:
                valores[celulas[0].strip()] = celulas[1].strip()
        return valores

    def fechar_popup(self) -> None:
        terminal.acao("Clicando em 'Close' no popup")
        self.clicar_com_seguranca(self.pagina.locator(self.BOTAO_FECHAR_POPUP))
        try:
            expect(self.pagina.locator(self.TITULO_POPUP)).to_have_count(0, timeout=2000)
        except AssertionError:
            # Na versão atual do demoqa o botão Close não fecha o modal; ESC fecha.
            terminal.acao("O botão 'Close' não fechou o popup (comportamento do demoqa); pressionando ESC")
            self.pagina.keyboard.press("Escape")

    def validar_popup_fechado(self) -> None:
        expect(self.pagina.locator(self.TITULO_POPUP)).to_have_count(0)
        terminal.acao("Popup fechado")

    # ---------------- privados ----------------
    def _preencher_campo(self, seletor: str, rotulo: str, valor: str) -> None:
        terminal.acao(f"Preenchendo '{rotulo}' com '{valor}'")
        self.pagina.fill(seletor, valor)

    def _selecionar_data_nascimento(self, data: date) -> None:
        terminal.acao(f"Selecionando a data de nascimento {data:%d/%m/%Y} no calendário")
        p = self.pagina
        p.click("#dateOfBirthInput")
        p.select_option(".react-datepicker__month-select", str(data.month - 1))
        p.select_option(".react-datepicker__year-select", str(data.year))
        p.locator(
            f".react-datepicker__day--{data.day:03d}:not(.react-datepicker__day--outside-month)"
        ).first.click()

    def _autocompletar(self, seletor: str, valor: str) -> None:
        campo = self.pagina.locator(seletor)
        campo.click()
        campo.press_sequentially(valor, delay=20)
        self.pagina.locator(self.OPCAO_AUTOCOMPLETE).first.wait_for()
        campo.press("Enter")
