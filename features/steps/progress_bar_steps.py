from behave import then, when
from playwright.sync_api import expect

from desafio_qa.config import ATRASO_ENTRE_ACOES_MS
from desafio_qa.pages import PaginaBarraProgresso
from desafio_qa.support import terminal

# Margem de segurança: a barra sobe ~1% a cada 100ms. Parar 5% antes do limite cobre a latência
# do clique; com SLOW_MO (navegador visível) o clique atrasa mais, então a margem cresce junto.
MARGEM_SEGURANCA = 5 + ATRASO_ENTRE_ACOES_MS // 100


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
    context.valor_apos_reset = _barra(context).resetar()


@then("o valor da barra de progresso deve ser {valor:d}%")
def step_validar_valor_exato(context, valor):
    barra = _barra(context)
    assert context.valor_apos_reset == valor, (
        f"Após o Reset a barra foi para {context.valor_apos_reset}%, esperado {valor}%"
    )
    expect(barra.pagina.locator(barra.BOTAO_INICIAR_PARAR)).to_have_text("Start")
    terminal.acao(f"A barra foi para {valor}% no Reset e o botão voltou para 'Start'")
