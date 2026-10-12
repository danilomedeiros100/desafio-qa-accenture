"""Impressão da execução no terminal: funcionalidade, cenário, passos, ações e resumo final.

Usa apenas caracteres ASCII nos marcadores para funcionar em qualquer terminal
(Linux, macOS e Windows), e cores ANSI somente quando a saída é um terminal interativo.
Defina NO_COLOR=1 para desligar as cores ou FORCE_COLOR=1 para forçá-las (ex.: saída redirecionada).
"""
from __future__ import annotations

import os
import sys

import allure

_CORES = {
    "negrito": "1",
    "cinza": "90",
    "vermelho": "31",
    "verde": "32",
    "amarelo": "33",
    "azul": "34",
    "magenta": "35",
    "ciano": "36",
}

_ROTULOS_STATUS = {
    "passed": ("PASSOU", "verde"),
    "failed": ("FALHOU", "vermelho"),
    "error": ("ERRO", "vermelho"),
    "hook_error": ("ERRO NO HOOK", "vermelho"),
    "skipped": ("PULADO", "amarelo"),
    "undefined": ("NAO IMPLEMENTADO", "amarelo"),
    "untested": ("NAO EXECUTADO", "amarelo"),
}

_usar_cores = False


def preparar_terminal() -> None:
    """Ajusta o stdout para não quebrar com acentos e habilita cores quando suportado."""
    global _usar_cores
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if os.name == "nt":
        os.system("")  # habilita sequências ANSI no console do Windows 10+
    _usar_cores = (sys.stdout.isatty() or bool(os.getenv("FORCE_COLOR"))) and not os.getenv("NO_COLOR")


def colorir(texto: str, *cores: str) -> str:
    if not _usar_cores:
        return texto
    codigos = ";".join(_CORES[c] for c in cores)
    return f"\033[{codigos}m{texto}\033[0m"


def escrever(texto: str = "") -> None:
    print(texto, flush=True)


def rotulo_status(nome_status: str) -> str:
    rotulo, cor = _ROTULOS_STATUS.get(nome_status, (nome_status.upper(), "amarelo"))
    return colorir(f"[{rotulo}]", "negrito", cor)


# ---------------------------------------------------------------- blocos da execução
def cabecalho(titulo: str, detalhes: list[str]) -> None:
    linha = "=" * 78
    escrever(colorir(linha, "azul"))
    escrever(colorir(f" {titulo}", "negrito", "azul"))
    for detalhe in detalhes:
        escrever(colorir(f" {detalhe}", "cinza"))
    escrever(colorir(linha, "azul"))


def funcionalidade(nome: str, arquivo: str) -> None:
    escrever()
    escrever(colorir(f"Funcionalidade: {nome}", "negrito", "magenta") + colorir(f"  # {arquivo}", "cinza"))


def cenario(nome: str, tags: list[str]) -> None:
    escrever()
    marcadores = " ".join(f"@{t}" for t in tags)
    escrever("  " + colorir(f"Cenário: {nome}", "negrito", "ciano") + colorir(f"  {marcadores}", "cinza"))


def passo(palavra_chave: str, texto: str) -> None:
    escrever(f"    {colorir(palavra_chave, 'negrito')} {texto}")


def acao(mensagem: str) -> None:
    """Ação executada dentro de um passo (Page Object, chamada de API, validação).
    Também vira um sub-passo no Allure Report."""
    escrever(colorir(f"        - {mensagem}", "cinza"))
    with allure.step(mensagem):
        pass


def info(mensagem: str) -> None:
    """Informação só para o terminal (ex.: onde uma evidência foi salva); não vira step no Allure."""
    escrever(colorir(f"        - {mensagem}", "cinza"))


def resultado_passo(nome_status: str, duracao: float, erro: str | None = None) -> None:
    escrever(f"      {rotulo_status(nome_status)} {colorir(f'{duracao:.2f}s', 'cinza')}")
    if erro:
        for linha in erro.strip().splitlines()[:15]:
            escrever(colorir(f"        {linha}", "vermelho"))


def resultado_cenario(nome_status: str, duracao: float) -> None:
    escrever(f"  => Cenário {rotulo_status(nome_status)} {colorir(f'em {duracao:.2f}s', 'cinza')}")


def aviso(mensagem: str) -> None:
    escrever(colorir(f"  [AVISO] {mensagem}", "amarelo"))


def resumo(cenarios: list[tuple[str, str, float]], passos: dict[str, int], duracao_total: float) -> None:
    """`cenarios` é uma lista de (nome, status, duração)."""
    contagem: dict[str, int] = {}
    for _, status, _ in cenarios:
        contagem[status] = contagem.get(status, 0) + 1
    falhos = [(nome, status) for nome, status, _ in cenarios if status not in ("passed", "skipped")]

    escrever()
    escrever(colorir("=" * 78, "azul"))
    escrever(colorir(" RESUMO DA EXECUÇÃO", "negrito", "azul"))
    escrever(colorir("=" * 78, "azul"))
    escrever(f" Cenários: {len(cenarios)} executados | " + _formatar_contagem(contagem))
    escrever(f" Steps:    {sum(passos.values())} executados | " + _formatar_contagem(passos))
    escrever(f" Duração:  {duracao_total:.2f}s")
    if falhos:
        escrever()
        escrever(colorir(" Cenários com falha:", "negrito", "vermelho"))
        for nome, status in falhos:
            escrever(f"   {rotulo_status(status)} {nome}")
    escrever()
    if not cenarios:
        escrever(colorir(" NENHUM CENÁRIO EXECUTADO (verifique as tags informadas)", "negrito", "amarelo"))
    elif falhos:
        escrever(colorir(" RESULTADO: FALHOU", "negrito", "vermelho"))
    else:
        escrever(colorir(" RESULTADO: SUCESSO", "negrito", "verde"))
    escrever(colorir("=" * 78, "azul"))


def _formatar_contagem(contagem: dict[str, int]) -> str:
    partes = [f"{qtd} {rotulo_status(status)}" for status, qtd in contagem.items() if qtd]
    return ", ".join(partes) or "0"
