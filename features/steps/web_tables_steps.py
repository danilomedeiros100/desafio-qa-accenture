from behave import given, then, when
from playwright.sync_api import expect

from desafio_qa.data.factories import novo_funcionario
from desafio_qa.pages import PaginaTabelasWeb
from desafio_qa.support import terminal


def _tabela(context) -> PaginaTabelasWeb:
    if not hasattr(context, "tabelas_web") or context.tabelas_web.pagina is not context.pagina:
        context.tabelas_web = PaginaTabelasWeb(context.pagina)
    return context.tabelas_web


# ---------------------------------------------------------------- CRUD de um registro
@when("eu crio um novo registro com dados aleatórios")
def step_criar_registro(context):
    context.funcionario = novo_funcionario()
    _tabela(context).adicionar_registro(context.funcionario)


@then("o registro deve ser exibido na tabela")
def step_validar_registro_exibido(context):
    assert _tabela(context).dados_da_linha(context.funcionario.email) == context.funcionario.como_linha()
    terminal.acao(f"Registro encontrado na tabela: {context.funcionario}")


@when("eu edito o registro criado com novos dados")
def step_editar_registro(context):
    context.email_anterior = context.funcionario.email
    context.funcionario = novo_funcionario()
    _tabela(context).editar_registro(context.email_anterior, context.funcionario)


@then("a tabela deve exibir os dados atualizados")
def step_validar_registro_atualizado(context):
    tabela = _tabela(context)
    assert tabela.dados_da_linha(context.funcionario.email) == context.funcionario.como_linha()
    expect(tabela.linha_por_email(context.email_anterior)).to_have_count(0)
    terminal.acao(f"Dados atualizados e <{context.email_anterior}> não aparece mais")


@when("eu deleto o registro criado")
def step_deletar_registro(context):
    _tabela(context).excluir_registro(context.funcionario.email)


@then("o registro não deve mais ser exibido na tabela")
def step_validar_registro_deletado(context):
    expect(_tabela(context).linha_por_email(context.funcionario.email)).to_have_count(0)
    terminal.acao(f"Registro <{context.funcionario.email}> removido da tabela")


# ---------------------------------------------------------------- Bônus: N registros
@given("que a tabela exibe {quantidade:d} registros por página")
def step_definir_tamanho_pagina(context, quantidade):
    tabela = _tabela(context)
    tabela.definir_registros_por_pagina(quantidade)
    context.emails_originais = tabela.emails()
    terminal.acao(f"Registros originais: {context.emails_originais}")


@when("eu crio {quantidade:d} novos registros com dados aleatórios")
def step_criar_varios_registros(context, quantidade):
    context.funcionarios_criados = [novo_funcionario() for _ in range(quantidade)]
    for numero, funcionario in enumerate(context.funcionarios_criados, start=1):
        terminal.acao(f"Registro {numero}/{quantidade}")
        _tabela(context).adicionar_registro(funcionario)


@then("os {quantidade:d} novos registros devem ser exibidos na tabela")
def step_validar_varios_registros(context, quantidade):
    tabela = _tabela(context)
    emails = tabela.emails()
    ausentes = [f.email for f in context.funcionarios_criados if f.email not in emails]
    assert len(context.funcionarios_criados) == quantidade
    assert not ausentes, f"Registros não exibidos: {ausentes}"
    for funcionario in context.funcionarios_criados:
        assert tabela.dados_da_linha(funcionario.email) == funcionario.como_linha()
    terminal.acao(f"Os {quantidade} registros estão na tabela (total de linhas: {len(emails)})")


@when("eu deleto todos os registros criados")
def step_deletar_varios_registros(context):
    tabela = _tabela(context)
    for funcionario in context.funcionarios_criados:
        if tabela.linha_por_email(funcionario.email).count():
            tabela.excluir_registro(funcionario.email)
        else:
            # Na versão atual do demoqa, excluir um registro novo remove junto os outros criados
            terminal.acao(f"<{funcionario.email}> já foi removido pela aplicação junto com o anterior")


@then("nenhum dos registros criados deve ser exibido na tabela")
def step_validar_nenhum_registro(context):
    emails = _tabela(context).emails()
    restantes = [f.email for f in context.funcionarios_criados if f.email in emails]
    assert not restantes, f"Registros não deletados: {restantes}"
    terminal.acao("Nenhum dos registros criados permanece na tabela")


@then("os registros originais da tabela devem ser mantidos")
def step_validar_registros_originais(context):
    emails = _tabela(context).emails()
    assert emails == context.emails_originais, f"{emails} != {context.emails_originais}"
    terminal.acao(f"Registros originais intactos: {emails}")
