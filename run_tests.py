"""Executa os testes e abre o Allure Report em português, com um único comando.

Funciona igual no Linux, macOS e Windows, pelo terminal ou pela IDE:

    python run_tests.py                         # tudo (API + Front-end) + relatório
    python run_tests.py --tags @api             # só API
    python run_tests.py --tags @frontend        # só Front-end
    python run_tests.py --visivel               # mostra o navegador executando
    python run_tests.py --sem-relatorio         # só executa os testes
    python run_tests.py --servidor              # abre o relatório via 'allure open' (com histórico)
    python run_tests.py --somente-relatorio     # só gera/abre o relatório da última execução
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from desafio_qa.support.allure_branding import NOME_RELATORIO, personalizar_relatorio

DIRETORIO_RAIZ = Path(__file__).resolve().parent
RESULTADOS = DIRETORIO_RAIZ / "reports" / "allure-results"
RELATORIO = DIRETORIO_RAIZ / "reports" / "allure-report"
ARQUIVO_LOG = DIRETORIO_RAIZ / "reports" / "execucao.log"
CODIGOS_DE_COR = re.compile(r"\x1b\[[0-9;]*m")
LINHAS_IGNORADAS = ("USING RUNNER:",)  # ruído impresso sempre pelo behave 1.3
IDIOMA_RELATORIO = "br"  # português (Brasil)


def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Executa os testes e gera o Allure Report.")
    parser.add_argument("--tags", action="append", default=[],
                        help="filtro de tags do behave (pode repetir), ex.: --tags @api")
    parser.add_argument("--visivel", action="store_true",
                        help="abre o navegador na tela (HEADLESS=false, SLOW_MO=300)")
    parser.add_argument("--sem-relatorio", action="store_true", help="não gera o Allure Report")
    parser.add_argument("--servidor", action="store_true",
                        help="abre o relatório com 'allure open' (servidor local) em vez de arquivo único")
    parser.add_argument("--manter-resultados", action="store_true",
                        help="não apaga os resultados das execuções anteriores")
    parser.add_argument("--somente-relatorio", action="store_true",
                        help="não executa os testes; só gera e abre o relatório da última execução")
    return parser.parse_args()


def executar_testes(args: argparse.Namespace) -> int:
    if not args.manter_resultados and RESULTADOS.exists():
        shutil.rmtree(RESULTADOS)

    ambiente = os.environ.copy()
    if args.visivel:
        ambiente.setdefault("HEADLESS", "false")
        ambiente.setdefault("SLOW_MO", "300")

    # a saída passa por um pipe: força as cores no console e o UTF-8 (Windows)
    ambiente["PYTHONIOENCODING"] = "utf-8"
    if sys.stdout.isatty():
        ambiente.setdefault("FORCE_COLOR", "1")

    comando = [sys.executable, "-m", "behave", *(f"--tags={t}" for t in args.tags)]
    ARQUIVO_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ARQUIVO_LOG.open("w", encoding="utf-8") as log, subprocess.Popen(
        comando, cwd=DIRETORIO_RAIZ, env=ambiente, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", bufsize=1,
    ) as processo:
        for linha in processo.stdout:
            if linha.startswith(LINHAS_IGNORADAS):
                continue
            print(linha, end="", flush=True)
            log.write(CODIGOS_DE_COR.sub("", linha))
    print(f"\nLog da execução (sem cores): {ARQUIVO_LOG}")
    return processo.returncode


def gerar_relatorio(args: argparse.Namespace) -> None:
    allure = shutil.which("allure")
    if not allure:
        print("\n[AVISO] Allure CLI não encontrado no PATH; relatório não gerado.")
        print("        Instale conforme o README (seção Instalação) e rode de novo.")
        return

    # mantém a tendência (gráfico de histórico) entre execuções locais
    historico = RELATORIO / "history"
    if historico.is_dir():
        shutil.copytree(historico, RESULTADOS / "history", dirs_exist_ok=True)

    comando = [
        allure, "generate", str(RESULTADOS), "-o", str(RELATORIO), "--clean",
        "--lang", IDIOMA_RELATORIO, "--name", NOME_RELATORIO,
    ]
    if not args.servidor:
        comando.append("--single-file")
    print("\nGerando o Allure Report...", flush=True)
    subprocess.run(comando, check=True, cwd=DIRETORIO_RAIZ)
    personalizar_relatorio(RELATORIO)

    if args.servidor:
        print("Abrindo o relatório (Ctrl+C ou Stop na IDE para encerrar o servidor)...", flush=True)
        subprocess.call([allure, "open", str(RELATORIO)], cwd=DIRETORIO_RAIZ)
    else:
        indice = RELATORIO / "index.html"
        print(f"Relatório: {indice}")
        webbrowser.open(indice.as_uri())


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = ler_argumentos()
    codigo_saida = 0 if args.somente_relatorio else executar_testes(args)
    if not args.sem_relatorio:
        gerar_relatorio(args)
    return codigo_saida


if __name__ == "__main__":
    sys.exit(main())
