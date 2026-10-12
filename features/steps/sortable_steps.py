from behave import given, then, when

from desafio_qa.pages import PaginaOrdenavel
from desafio_qa.support import terminal

ORDEM_CRESCENTE = ["One", "Two", "Three", "Four", "Five", "Six"]


def _lista(context) -> PaginaOrdenavel:
    if not hasattr(context, "ordenavel") or context.ordenavel.pagina is not context.pagina:
        context.ordenavel = PaginaOrdenavel(context.pagina)
    return context.ordenavel


@given("que os elementos da lista estão fora de ordem")
def step_embaralhar_lista(context):
    _lista(context).embaralhar()
    assert not _lista(context).esta_em_ordem_crescente()
    terminal.acao(f"Lista fora de ordem: {_lista(context).textos()}")


@when("eu ordeno os elementos em ordem crescente utilizando drag and drop")
def step_ordenar_lista(context):
    _lista(context).ordenar_crescente()


@then("os elementos devem estar em ordem crescente")
def step_validar_ordem_crescente(context):
    textos = _lista(context).textos()
    assert textos == ORDEM_CRESCENTE, textos
    terminal.acao(f"Lista final: {textos}")
