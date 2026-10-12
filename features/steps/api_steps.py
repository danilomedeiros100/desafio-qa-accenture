import random

from behave import given, then, when

from desafio_qa.data.factories import novo_usuario_api
from desafio_qa.support import terminal


@given("que eu crio um novo usuário com credenciais válidas")
def step_criar_usuario(context):
    context.usuario = novo_usuario_api()
    terminal.acao(f"Usuário gerado: {context.usuario.nome_usuario}")
    context.resposta = context.api.criar_usuario(context.usuario.nome_usuario, context.usuario.senha)


@then("o usuário deve ser criado com sucesso")
def step_validar_usuario_criado(context):
    r = context.resposta
    assert r.status_code == 201, f"Esperado 201, recebido {r.status_code}: {r.text}"
    corpo = r.json()
    assert corpo["username"] == context.usuario.nome_usuario
    assert corpo["userID"], "userID não retornado"
    assert corpo["books"] == []
    context.id_usuario = corpo["userID"]
    terminal.acao(f"userID: {context.id_usuario}")


@then("o usuário ainda não deve estar autorizado")
def step_validar_nao_autorizado(context):
    r = context.api.verificar_autorizacao(context.usuario.nome_usuario, context.usuario.senha)
    assert r.status_code == 200, r.text
    assert r.json() is False, f"Usuário já autorizado antes do token: {r.text}"
    terminal.acao("Authorized = false")


@when("eu gero um token de acesso para o usuário")
def step_gerar_token(context):
    context.resposta = context.api.gerar_token(context.usuario.nome_usuario, context.usuario.senha)


@then("o token deve ser gerado com sucesso")
def step_validar_token(context):
    r = context.resposta
    assert r.status_code == 200, r.text
    corpo = r.json()
    assert corpo["status"] == "Success", corpo
    assert corpo["result"] == "User authorized successfully.", corpo
    assert corpo["token"], "token vazio"
    context.token = corpo["token"]
    terminal.acao(f"Token gerado: {context.token[:20]}... (expira em {corpo['expires']})")
    # o usuário criado no teste é removido ao final do cenário
    context.limpezas.append(lambda: context.api.excluir_usuario(context.id_usuario, context.token))


@then("o usuário deve estar autorizado")
def step_validar_autorizado(context):
    r = context.api.verificar_autorizacao(context.usuario.nome_usuario, context.usuario.senha)
    assert r.status_code == 200, r.text
    assert r.json() is True, f"Usuário não autorizado: {r.text}"
    terminal.acao("Authorized = true")


@when("eu listo os livros disponíveis")
def step_listar_livros(context):
    context.resposta = context.api.listar_livros()


@then("a lista de livros não deve estar vazia")
def step_validar_lista_livros(context):
    r = context.resposta
    assert r.status_code == 200, r.text
    context.livros = r.json()["books"]
    assert len(context.livros) >= 2, f"Livros insuficientes: {len(context.livros)}"
    for livro in context.livros:
        assert {"isbn", "title", "author"} <= livro.keys(), livro
    terminal.acao(f"{len(context.livros)} livros disponíveis")


@when("eu alugo {quantidade:d} livros escolhidos da lista")
def step_alugar_livros(context, quantidade):
    escolhidos = random.sample(context.livros, k=quantidade)
    context.isbns_alugados = sorted(livro["isbn"] for livro in escolhidos)
    context.titulos_alugados = {livro["isbn"]: livro["title"] for livro in escolhidos}
    for livro in escolhidos:
        terminal.acao(f"Escolhido: '{livro['title']}' (ISBN {livro['isbn']})")
    context.resposta = context.api.alugar_livros(context.id_usuario, context.isbns_alugados, context.token)


@then("os livros devem ser adicionados à coleção do usuário")
def step_validar_livros_alugados(context):
    r = context.resposta
    assert r.status_code == 201, f"Esperado 201, recebido {r.status_code}: {r.text}"
    isbns = sorted(livro["isbn"] for livro in r.json()["books"])
    assert isbns == context.isbns_alugados, f"{isbns} != {context.isbns_alugados}"


@when("eu consulto os detalhes do usuário")
def step_consultar_usuario(context):
    context.resposta = context.api.consultar_usuario(context.id_usuario, context.token)


@then("os detalhes do usuário devem conter os livros alugados")
def step_validar_detalhes_usuario(context):
    r = context.resposta
    assert r.status_code == 200, r.text
    corpo = r.json()
    assert corpo["userId"] == context.id_usuario
    assert corpo["username"] == context.usuario.nome_usuario
    isbns = sorted(livro["isbn"] for livro in corpo["books"])
    assert isbns == context.isbns_alugados, f"{isbns} != {context.isbns_alugados}"
    for livro in corpo["books"]:
        assert livro["title"] == context.titulos_alugados[livro["isbn"]]
    terminal.acao(f"Usuário {corpo['username']} com os livros: {[b['title'] for b in corpo['books']]}")
