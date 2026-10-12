from behave import then, when

from desafio_qa.config import ARQUIVO_UPLOAD
from desafio_qa.data.factories import novo_estudante
from desafio_qa.pages import PaginaFormularioPratica
from desafio_qa.support import terminal


@when("eu preencho todo o formulário com valores aleatórios")
def step_preencher_formulario(context):
    context.formulario = PaginaFormularioPratica(context.pagina)
    context.estudante = novo_estudante(imagem=ARQUIVO_UPLOAD.name)
    context.formulario.preencher(context.estudante, ARQUIVO_UPLOAD)


@when("eu submeto o formulário")
def step_submeter_formulario(context):
    context.formulario.submeter()


@then("um popup de confirmação deve ser aberto")
def step_validar_popup_aberto(context):
    context.formulario.validar_popup_aberto()


@then("o popup deve exibir os dados informados")
def step_validar_dados_popup(context):
    e = context.estudante
    esperado = {
        "Student Name": e.nome_completo,
        "Student Email": e.email,
        "Gender": e.genero,
        "Mobile": e.celular,
        "Date of Birth": e.data_nascimento_formatada,
        "Subjects": ", ".join(e.materias),
        "Hobbies": ", ".join(e.hobbies),
        "Picture": e.imagem,
        "Address": e.endereco,
        "State and City": f"{e.estado} {e.cidade}",
    }
    exibido = context.formulario.valores_exibidos_no_popup()
    divergencias = {k: (v, exibido.get(k)) for k, v in esperado.items() if exibido.get(k) != v}
    assert not divergencias, f"Divergências (esperado, exibido): {divergencias}"
    for campo, valor in exibido.items():
        terminal.acao(f"{campo}: {valor}")


@when("eu fecho o popup")
def step_fechar_popup(context):
    context.formulario.fechar_popup()


@then("o popup não deve estar mais visível")
def step_validar_popup_fechado(context):
    context.formulario.validar_popup_fechado()
