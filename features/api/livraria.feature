# language: pt
@api
Funcionalidade: API da Book Store - aluguel de livros
  Como consumidor da API da Book Store
  Quero criar um usuário, autorizá-lo e alugar livros
  Para validar a jornada completa de ponta a ponta numa única execução

  Cenário: Criar usuário, gerar token, alugar dois livros e consultar os detalhes do usuário
    Dado que eu crio um novo usuário com credenciais válidas
    Então o usuário deve ser criado com sucesso
    E o usuário ainda não deve estar autorizado
    Quando eu gero um token de acesso para o usuário
    Então o token deve ser gerado com sucesso
    E o usuário deve estar autorizado
    Quando eu listo os livros disponíveis
    Então a lista de livros não deve estar vazia
    Quando eu alugo 2 livros escolhidos da lista
    Então os livros devem ser adicionados à coleção do usuário
    Quando eu consulto os detalhes do usuário
    Então os detalhes do usuário devem conter os livros alugados
