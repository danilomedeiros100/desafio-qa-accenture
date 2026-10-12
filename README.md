# Desafio QA Automation Engineer

Automação do desafio de QA (API + Frontend) sobre o [demoqa.com](https://demoqa.com), em **Python + Behave (BDD/Gherkin em português) + Playwright**, organizada em **Page Objects** e com **Allure Report** local e no CI.

O enunciado original está em [`docs/Desafio_QA_004.pdf`](docs/Desafio_QA_004.pdf) (e o `.pptx` original ao lado).

## Sumário

- [Stack](#stack)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação) ([Linux](#linux) · [macOS](#macos) · [Windows](#windows))
- [Executando os testes](#executando-os-testes)
- [Saída no terminal](#saída-no-terminal)
- [Allure Report](#allure-report)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Evidências e outros relatórios](#evidências-e-outros-relatórios)
- [CI (GitHub Actions)](#ci-github-actions)
- [Cobertura do desafio](#cobertura-do-desafio)
- [Decisões técnicas](#decisões-técnicas)
- [Problemas comuns](#problemas-comuns)

## Stack

| Camada | Ferramenta |
|---|---|
| BDD | Behave (equivalente ao Cucumber em Python), Gherkin em português |
| UI | Playwright (API síncrona) |
| API | requests |
| Massa de dados | Faker (dados aleatórios a cada execução) |
| Relatórios | Allure Report, impressão detalhada no terminal, HTML, screenshot e trace do Playwright em caso de falha |
| CI | GitHub Actions + GitHub Pages (Allure com histórico) |

> O enunciado cita Selenium WebDriver ou Cypress. A escolha pelo Playwright foi deliberada: ele dá suporte nativo a múltiplas janelas, drag and drop HTML5, auto-wait e trace de execução, sem precisar de driver separado.

## Estrutura do projeto

Arquivos e pastas seguem a convenção em inglês (`pages`, `steps`, `factories`). Classes, métodos, variáveis, features e steps estão em português.

```
.
├── desafio_qa/                     # código de automação (reutilizável)
│   ├── config.py                   # URLs, navegador, timeouts (via variáveis de ambiente)
│   ├── api/
│   │   └── bookstore_client.py     # ClienteBookStore: criar_usuario, gerar_token, alugar_livros...
│   ├── data/
│   │   └── factories.py            # massa aleatória: novo_usuario_api, novo_estudante, novo_funcionario
│   ├── pages/                      # Page Objects
│   │   ├── base_page.py            # PaginaBase: abrir, clicar_com_seguranca
│   │   ├── home_page.py            # PaginaInicial (escolher_card) e MenuLateral (clicar_item)
│   │   ├── practice_form_page.py   # PaginaFormularioPratica: preencher, submeter, fechar_popup...
│   │   ├── browser_windows_page.py # PaginaJanelasNavegador: abrir_nova_janela
│   │   ├── web_tables_page.py      # PaginaTabelasWeb: adicionar/editar/excluir_registro...
│   │   ├── progress_bar_page.py    # PaginaBarraProgresso: iniciar, parar_ao_atingir, resetar...
│   │   └── sortable_page.py        # PaginaOrdenavel: embaralhar, ordenar_crescente...
│   └── support/
│       ├── terminal.py             # impressão da execução no terminal
│       └── evidence.py             # anexos e ambiente do Allure
├── features/
│   ├── api/livraria.feature
│   ├── frontend/*.feature
│   ├── steps/*_steps.py            # step definitions (finos: delegam aos Page Objects)
│   └── environment.py              # hooks: navegador, terminal, anúncios, evidências, limpeza
├── resources/upload/arquivo_upload.txt   # arquivo .txt usado no upload do formulário
├── docs/                           # enunciado do desafio
├── behave.ini                      # configuração do Behave (Allure como formatter padrão)
├── requirements.txt
├── Makefile                        # atalhos para Linux/macOS
└── .github/workflows/tests.yml     # pipeline de CI
```

## Pré-requisitos

| Ferramenta | Versão | Para quê |
|---|---|---|
| Python | 3.10 ou superior | executar os testes |
| Git | qualquer | clonar o repositório |
| Java (JRE/JDK) | 8 ou superior | apenas para gerar o Allure Report localmente |
| Allure CLI | 2.x | apenas para gerar o Allure Report localmente |

Os testes rodam sem Java/Allure CLI; eles só são necessários para **visualizar** o relatório Allure na sua máquina.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/danilomedeiros100/desafio-qa-accenture.git
cd desafio-qa-accenture
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

> `--with-deps` instala as bibliotecas de sistema que o Chromium precisa (pode pedir `sudo`). Em Debian/Ubuntu, se o `venv` não existir: `sudo apt install python3-venv`.

Allure CLI (opcional, para o relatório local):

```bash
sudo apt install default-jre        # Java
# Opção 1 - pacote .deb oficial (troque a versão pela mais recente em github.com/allure-framework/allure2/releases)
wget https://github.com/allure-framework/allure2/releases/download/2.30.0/allure_2.30.0-1_all.deb
sudo dpkg -i allure_2.30.0-1_all.deb
# Opção 2 - via npm
npm install -g allure-commandline
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Allure CLI (opcional):

```bash
brew install allure     # instala o Java como dependência, se necessário
```

Também é possível usar o `Makefile`: `make install`.

### Windows

No **PowerShell**:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

> Se o PowerShell bloquear a ativação do venv, rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
> No **Prompt de Comando (cmd)**, a ativação é `.venv\Scripts\activate.bat`.

Allure CLI (opcional), com [Scoop](https://scoop.sh) ou npm:

```powershell
scoop install allure          # requer Java: scoop bucket add java; scoop install openjdk
# ou
npm install -g allure-commandline
```

## Executando os testes

Com o ambiente virtual **ativado**, os comandos do `behave` são iguais em Linux, macOS e Windows:

```bash
behave                          # tudo (API + Frontend) numa única execução
behave --tags=@api              # só a Parte 1 (API)
behave --tags=@frontend         # só a Parte 2 (Frontend)
behave --tags=@bonus            # bônus dos 12 registros
behave --tags=@formulario       # um cenário específico
```

Tags disponíveis: `@api`, `@frontend`, `@formulario`, `@janelas`, `@tabelas_web`, `@bonus`, `@barra_progresso`, `@ordenavel`.

Para **ver o navegador** executando, defina as variáveis de ambiente conforme o terminal:

| Terminal | Comando |
|---|---|
| Linux / macOS (bash, zsh) | `HEADLESS=false SLOW_MO=300 behave --tags=@frontend` |
| Windows PowerShell | `$env:HEADLESS="false"; $env:SLOW_MO="300"; behave --tags=@frontend` |
| Windows cmd | `set HEADLESS=false && set SLOW_MO=300 && behave --tags=@frontend` |

> No PowerShell e no cmd as variáveis ficam definidas até fechar o terminal. Para voltar ao modo headless: `$env:HEADLESS="true"` (PowerShell) ou `set HEADLESS=true` (cmd).

Atalhos do `Makefile` (Linux/macOS): `make test`, `make api`, `make frontend`, `make bonus`, `make headed`, `make report`, `make allure`, `make allure-serve`, `make clean`.

## Saída no terminal

A execução é impressa em tempo real: funcionalidade, cenário, cada step com seu resultado e tempo, as ações executadas dentro do step (cliques, campos preenchidos, requisições HTTP com status e tempo) e um resumo final.

```
==============================================================================
 DESAFIO QA AUTOMATION - demoqa.com
 URL base: https://demoqa.com
 Navegador: chromium (headless)
 Filtro de tags: @api
==============================================================================

Funcionalidade: API da Book Store - aluguel de livros  # features/api/livraria.feature

  Cenário: Criar usuário, gerar token, alugar dois livros e consultar os detalhes do usuário  @api
    Dado que eu crio um novo usuário com credenciais válidas
        - Usuário gerado: qa_1791844330705514
        - POST /Account/v1/User -> 201 (1.89s)
      [PASSOU] 1.89s
    ...
    Quando eu alugo 2 livros escolhidos da lista
        - Escolhido: 'Designing Evolvable Web APIs with ASP.NET' (ISBN 9781449337711)
        - Escolhido: 'Programming JavaScript Applications' (ISBN 9781491950296)
        - POST /BookStore/v1/Books -> 201 (0.40s)
      [PASSOU] 0.40s
    ...
  => Cenário [PASSOU] em 7.03s

==============================================================================
 RESUMO DA EXECUÇÃO
==============================================================================
 Cenários: 1 executados | 1 [PASSOU]
 Steps:    12 executados | 12 [PASSOU]
 Duração:  7.06s

 RESULTADO: SUCESSO
==============================================================================
```

Quando um step falha, a mensagem de erro aparece logo abaixo dele, junto com o caminho do screenshot e do trace salvos. A saída usa cores ANSI quando o terminal suporta (defina `NO_COLOR=1` para desligar) e marcadores ASCII, para funcionar também no console do Windows.

Isso é feito pelos hooks em [`features/environment.py`](features/environment.py) e pelo módulo [`desafio_qa/support/terminal.py`](desafio_qa/support/terminal.py). A captura de saída do Behave fica desligada no `behave.ini` para as mensagens aparecerem na hora.

## Allure Report

Todo `behave` grava os resultados do Allure em `reports/allure-results` (o formatter do Allure é o padrão no `behave.ini`). O relatório inclui:

- cada step com as ações executadas como sub-steps;
- requisição e resposta de cada chamada da API, em JSON (senhas mascaradas);
- screenshot da tela final de cada cenário de frontend e da tela no momento de uma falha;
- trace do Playwright anexado aos cenários que falharam;
- dados do ambiente (URL, navegador, Python, sistema operacional).

### Gerar e abrir localmente

Depois de rodar os testes (o Allure CLI precisa estar instalado, ver [Instalação](#instalação)):

```bash
allure serve reports/allure-results
```

Isso gera o relatório numa pasta temporária e abre no navegador. Para gerar uma pasta estática e abrir depois:

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

Os comandos são os mesmos em Linux, macOS e Windows. No Linux/macOS há os atalhos `make allure-serve` e `make allure`.

> Os resultados se acumulam a cada execução. Para começar um relatório limpo, apague a pasta `reports` antes de rodar (`make clean`, ou `Remove-Item -Recurse reports` no PowerShell, ou `rmdir /s /q reports` no cmd).
> Abrir o `index.html` direto pelo explorador de arquivos não funciona (o navegador bloqueia o carregamento dos dados); use `allure open` ou `allure serve`.

### No CI

A cada push na `main`, o GitHub Actions gera o Allure Report com **histórico das últimas 20 execuções** e publica no GitHub Pages:

**https://danilomedeiros100.github.io/desafio-qa-accenture/**

O relatório também fica disponível como artefato `relatorios` em cada execução do workflow (aba *Actions*).

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `BASE_URL` | `https://demoqa.com` | URL alvo |
| `BROWSER` | `chromium` | `chromium`, `firefox` ou `webkit` (instale com `python -m playwright install <navegador>`) |
| `HEADLESS` | `true` | `false` abre o navegador na tela |
| `SLOW_MO` | `0` | atraso (ms) entre ações do navegador |
| `DEFAULT_TIMEOUT_MS` | `15000` | timeout padrão do Playwright |
| `API_TIMEOUT_S` | `30` | timeout das requisições da API |
| `NO_COLOR` | (vazio) | qualquer valor desliga as cores no terminal |

## Evidências e outros relatórios

| Caminho | Conteúdo |
|---|---|
| `reports/allure-results/` | resultados brutos do Allure |
| `reports/allure-report/` | Allure Report gerado (`allure generate`) |
| `reports/report.html` | relatório HTML simples (`behave -f html -o reports/report.html`) |
| `reports/screenshots/` | screenshot da página no step que falhou |
| `reports/traces/` | trace do Playwright do cenário que falhou. Abra com `playwright show-trace reports/traces/<arquivo>.zip` |
| `reports/junit/` | XML JUnit, só quando executado com `behave --junit` |

## CI (GitHub Actions)

O workflow [`.github/workflows/tests.yml`](.github/workflows/tests.yml) roda em todo push e pull request (e manualmente pela aba *Actions*):

1. instala Python 3.12, as dependências e o Chromium;
2. executa todos os cenários;
3. busca o histórico na branch `gh-pages` e gera o Allure Report;
4. publica o relatório no GitHub Pages (apenas na `main`);
5. anexa `reports/` como artefato;
6. marca o job como falho se algum cenário falhou (o relatório é publicado mesmo assim).

Na primeira execução o workflow cria a branch `gh-pages`. Para o link do relatório funcionar, o GitHub Pages do repositório deve estar configurado em *Settings > Pages > Source: Deploy from a branch > `gh-pages` / root*.

## Cobertura do desafio

### Parte 1: API (`@api`)

Um único cenário encadeia todos os passos, numa única execução:

1. Criar usuário (`POST /Account/v1/User`): nome único e senha que atende à política da API
2. Validar que **ainda não** está autorizado (`POST /Account/v1/Authorized` → `false`)
3. Gerar token (`POST /Account/v1/GenerateToken`) → `status: Success`
4. Confirmar autorização (`Authorized` → `true`)
5. Listar livros (`GET /BookStore/v1/Books`)
6. Alugar 2 livros escolhidos aleatoriamente (`POST /BookStore/v1/Books` com Bearer token)
7. Consultar o usuário (`GET /Account/v1/User/{userID}`) e validar ISBNs e títulos

O usuário criado é **removido ao final** (`DELETE /Account/v1/User/{userID}`), para não deixar lixo no ambiente.

### Parte 2: Frontend (`@frontend`)

| Feature | O que valida |
|---|---|
| Formulário de estudante (Practice Form) | Preenche **todos** os campos com dados aleatórios (incluindo datepicker, autocomplete, State/City e upload do `.txt` versionado), submete, valida que o popup abriu **e que exibe exatamente os dados enviados**, fecha o popup |
| Janelas do navegador (Browser Windows) | Abre a nova janela, valida "This is a sample page", fecha e garante que só a janela original ficou aberta |
| Tabela de registros (Web Tables) | Cria, edita (valida os novos dados e a ausência dos antigos) e deleta um registro |
| Tabela de registros `@bonus` | Cria 12 registros dinâmicos, valida todos, deleta todos e garante que os registros originais continuam intactos |
| Barra de progresso (Progress Bar) | Para antes de 25% e valida `<= 25%`, retoma até 100%, reseta e valida 0% |
| Lista ordenável (Sortable) | Embaralha a lista e depois a ordena em ordem crescente com drag and drop |

## Decisões técnicas

- **Anúncios bloqueados:** os banners do demoqa cobrem botões como Submit e Close e deixam a página lenta. O `environment.py` aborta as requisições de domínios de anúncio e esconde o rodapé. O `PaginaBase.clicar_com_seguranca` tem uma alternativa para quando algum overlay ainda intercepta o clique.
- **Navegação pelo fluxo real:** cada cenário entra pela home, clica no card e depois no submenu, como pede o enunciado, e valida a URL de destino. O clique é feito no link do menu: o item `<li>` é mais largo que o link e um clique no centro dele não navega.
- **Comportamentos do demoqa atual tratados e registrados no terminal:**
  - o botão **Close** do popup do formulário não fecha o modal; o teste clica em Close e, se o modal continuar aberto, fecha com ESC;
  - na tabela, **excluir um registro novo remove junto os outros registros criados**. No bônus, o teste exclui os que ainda estão na tabela e informa os que a aplicação já removeu; a validação final continua exigindo que nenhum criado permaneça e que os originais estejam intactos.
- **Progress Bar sem instabilidade:** o polling roda dentro do navegador (`wait_for_function` a cada frame) e para em 20%, uma margem de 5% sobre o limite de 25%. A barra avança cerca de 1% a cada 100ms, então essa margem cobre a latência. Depois do Stop, o teste confirma que o valor parou de mudar.
- **Sortable:** a lista **já carrega em ordem crescente**, então executar só "ordenar" não provaria nada. O cenário primeiro embaralha a lista (também por drag and drop) e depois ordena com um selection sort, um movimento por vez, validando cada movimento. A lista usa react-dnd com backend HTML5: o `drag_to` nativo do Playwright é a primeira opção, e há uma alternativa disparando a sequência de `DragEvent`s.
- **Web Tables bônus:** com 3 registros originais mais 12 novos, a tabela passaria de 10 linhas e paginaria. O cenário ajusta para 50 linhas por página antes de criar. Os 12 registros são gerados dinamicamente (Faker) a partir da quantidade informada no Gherkin, e localizados pelo e-mail, não pelo índice da linha.
- **Popup do formulário validado por conteúdo:** além de verificar que o popup abriu, o teste compara cada campo exibido com o que foi enviado.
- **Steps finos:** os steps só orquestram. Seletores e regras de interação ficam nos Page Objects, e a massa de dados nas factories.
- **Isolamento:** cada cenário roda num `BrowserContext` novo. O navegador só é iniciado se houver cenário `@frontend`, então `behave --tags=@api` não abre navegador.

## Problemas comuns

| Sintoma | Solução |
|---|---|
| `Executable doesn't exist ... chromium` | Rode `python -m playwright install chromium` com o venv ativado |
| Linux: erro de biblioteca ausente ao abrir o Chromium | `python -m playwright install --with-deps chromium` |
| `behave: command not found` / `'behave' não é reconhecido` | Ative o venv (`source .venv/bin/activate` ou `.\.venv\Scripts\Activate.ps1`) |
| `allure: command not found` | Instale o Allure CLI e o Java (ver [Instalação](#instalação)) |
| Timeouts ao carregar o demoqa | O site às vezes fica lento; tente de novo ou aumente `DEFAULT_TIMEOUT_MS` |
| Caracteres estranhos no lugar de cores (Windows antigo) | Defina `NO_COLOR=1` |
