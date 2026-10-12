"""Hooks do Behave: impressão da execução no terminal, ciclo de vida do Playwright,
bloqueio de anúncios, evidências (Allure, screenshots, traces) e limpeza."""
import re
import sys
import time
from types import SimpleNamespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from playwright.sync_api import sync_playwright  # noqa: E402

from desafio_qa.api import ClienteBookStore  # noqa: E402
from desafio_qa.config import (  # noqa: E402
    ATRASO_ENTRE_ACOES_MS, DIRETORIO_RAIZ, DIRETORIO_SCREENSHOTS, DIRETORIO_TRACES, HEADLESS,
    NAVEGADOR, TAMANHO_JANELA, TIMEOUT_PADRAO_MS, URL_BASE,
)
from desafio_qa.support import evidence, terminal  # noqa: E402

# Anúncios do demoqa cobrem botões (Submit, Close) e deixam a página lenta
HOSTS_DE_ANUNCIO = re.compile(
    r"(googlesyndication|doubleclick|googletagservices|googletagmanager|google-analytics|"
    r"adservice\.google|amazon-adsystem|adsystem|pubmatic|criteo|taboola|outbrain|adnxs|"
    r"rubiconproject|openx|ezoic|adplus)"
)
SCRIPT_OCULTAR_ANUNCIOS = """
document.addEventListener('DOMContentLoaded', () => {
  const s = document.createElement('style');
  s.textContent = `#fixedban, footer, .adsbygoogle, iframe[id^="google_ads"], [id^="adplus"]
                   { display: none !important; }`;
  document.head.appendChild(s);
});
"""


def _slug(texto: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", texto).strip("_")[:80]


def _nome_status(status) -> str:
    return getattr(status, "name", str(status))


def _diretorios_allure(context) -> list[Path]:
    """Diretórios de saída configurados para o formatter do Allure."""
    formatos = context.config.format or []
    saidas = context.config.outfiles or []
    return [
        DIRETORIO_RAIZ / saida for formato, saida in zip(formatos, saidas) if "allure" in formato
    ]


# ---------------------------------------------------------------- execução
def before_all(context):
    terminal.preparar_terminal()
    # Objeto criado no nível raiz do contexto: o que for guardado nele sobrevive entre cenários
    context.recursos = SimpleNamespace(playwright=None, navegador=None)
    context.inicio_execucao = time.perf_counter()
    context.resultados_cenarios = []
    context.contagem_passos = {}
    tags = " ".join(str(t) for t in context.config.tags or []) or "todas"
    terminal.cabecalho(
        "DESAFIO QA AUTOMATION - demoqa.com",
        [
            f"URL base: {URL_BASE}",
            f"Navegador: {NAVEGADOR} ({'headless' if HEADLESS else 'visível'})",
            f"Filtro de tags: {tags}",
        ],
    )


def _garantir_navegador(context):
    recursos = context.recursos
    if recursos.navegador is None:
        terminal.acao(f"Iniciando o navegador {NAVEGADOR}")
        recursos.playwright = sync_playwright().start()
        lancador = getattr(recursos.playwright, NAVEGADOR)
        recursos.navegador = lancador.launch(headless=HEADLESS, slow_mo=ATRASO_ENTRE_ACOES_MS)
    return recursos.navegador


def before_feature(context, feature):
    terminal.funcionalidade(feature.name, feature.location.filename)


def before_scenario(context, scenario):
    terminal.cenario(scenario.name, sorted(scenario.effective_tags))
    context.limpezas = []
    context.inicio_cenario = time.perf_counter()
    tags = set(scenario.effective_tags)

    if "api" in tags:
        context.api = ClienteBookStore()

    if "frontend" in tags:
        navegador = _garantir_navegador(context)
        context.contexto_navegador = navegador.new_context(viewport=TAMANHO_JANELA)
        context.contexto_navegador.set_default_timeout(TIMEOUT_PADRAO_MS)
        context.contexto_navegador.route(HOSTS_DE_ANUNCIO, lambda rota: rota.abort())
        context.contexto_navegador.add_init_script(SCRIPT_OCULTAR_ANUNCIOS)
        context.contexto_navegador.tracing.start(screenshots=True, snapshots=True, sources=False)
        context.pagina = context.contexto_navegador.new_page()


def before_step(context, step):
    terminal.passo(step.keyword, step.name)
    context.inicio_passo = time.perf_counter()


def after_step(context, step):
    status = _nome_status(step.status)
    duracao = time.perf_counter() - context.inicio_passo
    context.contagem_passos[status] = context.contagem_passos.get(status, 0) + 1
    terminal.resultado_passo(status, duracao, step.error_message if status != "passed" else None)

    if status == "failed" and getattr(context, "pagina", None):
        imagem = evidence.anexar_screenshot(context.pagina, f"Falha - {step.name}")
        if imagem:
            DIRETORIO_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
            caminho = DIRETORIO_SCREENSHOTS / f"{_slug(context.scenario.name)}__{_slug(step.name)}.png"
            caminho.write_bytes(imagem)
            terminal.acao(f"Screenshot salvo em {caminho.relative_to(DIRETORIO_RAIZ)}")


def after_scenario(context, scenario):
    for limpeza in reversed(getattr(context, "limpezas", [])):
        try:
            limpeza()
        except Exception as exc:  # noqa: BLE001
            terminal.aviso(f"Limpeza falhou: {exc}")

    status = _nome_status(scenario.status)
    if getattr(context, "contexto_navegador", None):
        if status == "passed":
            evidence.anexar_screenshot(context.pagina, "Tela final")
            context.contexto_navegador.tracing.stop()
        else:
            DIRETORIO_TRACES.mkdir(parents=True, exist_ok=True)
            trace = DIRETORIO_TRACES / f"{_slug(scenario.name)}.zip"
            context.contexto_navegador.tracing.stop(path=str(trace))
            evidence.anexar_arquivo(trace, "Trace do Playwright", "zip")
            terminal.acao(f"Trace salvo em {trace.relative_to(DIRETORIO_RAIZ)} "
                          f"(abra com: playwright show-trace {trace.relative_to(DIRETORIO_RAIZ)})")
        context.contexto_navegador.close()
        context.contexto_navegador = None
        context.pagina = None

    duracao = time.perf_counter() - context.inicio_cenario
    context.resultados_cenarios.append((scenario.name, status, duracao))
    terminal.resultado_cenario(status, duracao)


def after_all(context):
    if context.recursos.navegador:
        context.recursos.navegador.close()
    if context.recursos.playwright:
        context.recursos.playwright.stop()

    for diretorio in _diretorios_allure(context):
        evidence.registrar_ambiente(diretorio)

    terminal.resumo(
        context.resultados_cenarios,
        context.contagem_passos,
        time.perf_counter() - context.inicio_execucao,
    )
