import re

from behave import step
from playwright.sync_api import expect

from desafio_qa.pages import MenuLateral, PaginaInicial
from desafio_qa.support import terminal

URLS_DOS_SUBMENUS = {
    "Practice Form": "/automation-practice-form",
    "Browser Windows": "/browser-windows",
    "Web Tables": "/webtables",
    "Progress Bar": "/progress-bar",
    "Sortable": "/sortable",
}


@step("que eu acesso o site demoqa")
def step_acessar_site(context):
    context.pagina_inicial = PaginaInicial(context.pagina).abrir()


@step('eu escolho a opção "{card}" na página inicial')
def step_escolher_card(context, card):
    context.pagina_inicial.escolher_card(card)


@step('eu clico no submenu "{item}"')
def step_clicar_submenu(context, item):
    MenuLateral(context.pagina).clicar_item(item)
    if item in URLS_DOS_SUBMENUS:
        caminho = URLS_DOS_SUBMENUS[item]
        expect(context.pagina).to_have_url(re.compile(re.escape(caminho) + r"$"))
        terminal.acao(f"URL validada: {context.pagina.url}")
