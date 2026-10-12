# language: pt
@frontend @ordenavel
Funcionalidade: Lista ordenável (Sortable)
  Como usuário do demoqa
  Quero reordenar os elementos da lista com drag and drop
  Para deixá-los em ordem crescente

  Contexto:
    Dado que eu acesso o site demoqa
    E eu escolho a opção "Interactions" na página inicial
    E eu clico no submenu "Sortable"

  # A lista já carrega em ordem crescente (One..Six). Para o teste ter valor,
  # ela é embaralhada primeiro (também via drag and drop) e depois ordenada.
  Cenário: Ordenar os elementos em ordem crescente usando drag and drop
    Dado que os elementos da lista estão fora de ordem
    Quando eu ordeno os elementos em ordem crescente utilizando drag and drop
    Então os elementos devem estar em ordem crescente
