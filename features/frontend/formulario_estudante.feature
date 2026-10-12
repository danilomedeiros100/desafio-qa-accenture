# language: pt
@frontend @formulario
Funcionalidade: Formulário de estudante (Practice Form)
  Como usuário do demoqa
  Quero preencher e submeter o formulário de estudante
  Para confirmar que os dados são recebidos corretamente

  Contexto:
    Dado que eu acesso o site demoqa
    E eu escolho a opção "Forms" na página inicial
    E eu clico no submenu "Practice Form"

  Cenário: Preencher todo o formulário com valores aleatórios e submeter
    Quando eu preencho todo o formulário com valores aleatórios
    E eu submeto o formulário
    Então um popup de confirmação deve ser aberto
    E o popup deve exibir os dados informados
    Quando eu fecho o popup
    Então o popup não deve estar mais visível
