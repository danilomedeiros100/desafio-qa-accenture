from behave import then, when
from playwright.sync_api import expect

from desafio_qa.pages import PaginaExemplo, PaginaJanelasNavegador
from desafio_qa.support import terminal


@when('eu clico no botão "{botao}"')
def step_clicar_nova_janela(context, botao):
    context.janelas_antes = len(context.contexto_navegador.pages)
    context.nova_janela = PaginaJanelasNavegador(context.pagina).abrir_nova_janela(botao)


@then("uma nova janela deve ser aberta")
def step_validar_nova_janela(context):
    assert len(context.contexto_navegador.pages) == context.janelas_antes + 1
    assert context.nova_janela.url.endswith(PaginaExemplo.CAMINHO), context.nova_janela.url
    terminal.acao(f"Janelas abertas: {len(context.contexto_navegador.pages)}")


@then('a nova janela deve exibir a mensagem "{mensagem}"')
def step_validar_mensagem(context, mensagem):
    expect(PaginaExemplo(context.nova_janela).titulo).to_have_text(mensagem)
    terminal.acao(f"Mensagem exibida: '{mensagem}'")


@when("eu fecho a nova janela")
def step_fechar_nova_janela(context):
    terminal.acao(f"Fechando a janela {context.nova_janela.url}")
    context.nova_janela.close()


@then("apenas a janela original deve permanecer aberta")
def step_validar_somente_original(context):
    janelas = context.contexto_navegador.pages
    assert len(janelas) == context.janelas_antes, f"Janelas abertas: {[j.url for j in janelas]}"
    assert context.nova_janela.is_closed()
    assert janelas[0] == context.pagina
    terminal.acao(f"Janela restante: {janelas[0].url}")
