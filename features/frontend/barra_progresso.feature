# language: pt
@frontend @barra_progresso
Funcionalidade: Barra de progresso (Progress Bar)
  Como usuário do demoqa
  Quero controlar a barra de progresso
  Para validar parada, conclusão e reset

  Contexto:
    Dado que eu acesso o site demoqa
    E eu escolho a opção "Widgets" na página inicial
    E eu clico no submenu "Progress Bar"

  Cenário: Parar a barra antes de 25%, concluir e resetar
    Quando eu inicio a barra de progresso
    E eu paro a barra de progresso antes de atingir 25%
    Então o valor da barra de progresso deve ser menor ou igual a 25%
    Quando eu inicio a barra de progresso novamente
    E a barra de progresso chega a 100%
    E eu reseto a barra de progresso
    Então o valor da barra de progresso deve ser 0%
