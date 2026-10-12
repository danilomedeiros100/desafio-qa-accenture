# language: pt
@frontend @tabelas_web
Funcionalidade: Tabela de registros (Web Tables)
  Como usuário do demoqa
  Quero gerenciar registros na tabela
  Para validar criação, edição e exclusão

  Contexto:
    Dado que eu acesso o site demoqa
    E eu escolho a opção "Elements" na página inicial
    E eu clico no submenu "Web Tables"

  Cenário: Criar, editar e deletar um registro
    Quando eu crio um novo registro com dados aleatórios
    Então o registro deve ser exibido na tabela
    Quando eu edito o registro criado com novos dados
    Então a tabela deve exibir os dados atualizados
    Quando eu deleto o registro criado
    Então o registro não deve mais ser exibido na tabela

  @bonus
  Cenário: Criar 12 registros dinamicamente e deletar todos
    Dado que a tabela exibe 50 registros por página
    Quando eu crio 12 novos registros com dados aleatórios
    Então os 12 novos registros devem ser exibidos na tabela
    Quando eu deleto todos os registros criados
    Então nenhum dos registros criados deve ser exibido na tabela
    E os registros originais da tabela devem ser mantidos
