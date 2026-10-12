from behave import then, when
from playwright.sync_api import expect

from desafio_qa.pages import PaginaBarraProgresso
from desafio_qa.support import terminal

# Margem de segurança: a barra sobe ~1% a cada 100ms; parar em 20% garante ficar <= 25%
MARGEM_SEGURANCA = 5


def _barra(context) -> PaginaBarraProgresso:
    if not hasattr(context, "barra_progresso") or context.barra_progresso.pagina is not context.pagina:
        context.barra_progresso = PaginaBarraProgresso(context.pagina)
    return context.barra_progresso


@when("eu inicio a barra de progresso")
@when("eu inicio a barra de progresso novamente")
def step_iniciar_barra(context):
    _barra(context).iniciar()


@when("eu paro a barra de progresso antes de atingir {limite:d}%")
def step_parar_barra_antes_de(context, limite):
    context.valor_parada = _barra(context).parar_ao_atingir(limite - MARGEM_SEGURANCA)


@then("o valor da barra de progresso deve ser menor ou igual a {limite:d}%")
def step_validar_valor_maximo(context, limite):
    valor = _barra(context).valor()
    assert 0 < valor <= limite, f"Valor {valor}% fora do esperado (<= {limite}%)"
    terminal.acao(f"Valor da barra: {valor}% (<= {limite}%)")


@when("a barra de progresso chega a 100%")
def step_aguardar_conclusao(context):
    _barra(context).aguardar_conclusao()
    assert _barra(context).valor() == 100
    terminal.acao("Barra concluída: 100%")


@when("eu reseto a barra de progresso")
def step_resetar_barra(context):
    _barra(context).resetar()


@then("o valor da barra de progresso deve ser {valor:d}%")
def step_validar_valor_exato(context, valor):
    barra = _barra(context)
    expect(barra.pagina.locator(barra.BARRA)).to_have_attribute("aria-valuenow", str(valor))
    expect(barra.pagina.locator(barra.BOTAO_INICIAR_PARAR)).to_have_text("Start")
    terminal.acao(f"Valor da barra: {valor}% e botão voltou para 'Start'")
