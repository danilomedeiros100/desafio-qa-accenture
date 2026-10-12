# language: pt
@frontend @janelas
Funcionalidade: Janelas do navegador (Browser Windows)
  Como usuário do demoqa
  Quero abrir uma nova janela a partir da página
  Para validar o conteúdo exibido nela

  Contexto:
    Dado que eu acesso o site demoqa
    E eu escolho a opção "Alerts, Frame & Windows" na página inicial
    E eu clico no submenu "Browser Windows"

  Cenário: Abrir uma nova janela, validar a mensagem e fechá-la
    Quando eu clico no botão "New Window"
    Então uma nova janela deve ser aberta
    E a nova janela deve exibir a mensagem "This is a sample page"
    Quando eu fecho a nova janela
    Então apenas a janela original deve permanecer aberta
