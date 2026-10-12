"""Personaliza o Allure Report com a identidade visual da Accenture.

Roda depois do `allure generate`: troca o favicon pelo ícone ">" da Accenture e injeta o
tema (cores, logo do menu lateral e faixa da Visão geral) no index.html.

Uso: python -m desafio_qa.support.allure_branding reports/allure-report
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote

DIRETORIO_TEMA = Path(__file__).resolve().parents[2] / "resources" / "allure"
MARCADOR = "<!-- tema-accenture -->"
NOME_RELATORIO = "Accenture QA Report"
TEMA_PADRAO = "light"

# Roda antes do Allure iniciar: define o tema claro como padrão, sem sobrescrever a escolha
# que o usuário fizer no botão de tema (o Allure guarda em localStorage["allure-theme"]).
SCRIPT_TEMA_PADRAO = (
    "<script>try{if(!localStorage.getItem('allure-theme'))"
    f"localStorage.setItem('allure-theme','{TEMA_PADRAO}')}}catch(e){{}}</script>"
)


def _icone_data_uri() -> str:
    svg = (DIRETORIO_TEMA / "accenture-icon.svg").read_text(encoding="utf-8")
    svg = re.sub(r"\s+", " ", svg).strip()
    return "data:image/svg+xml," + quote(svg, safe=" =:/',")


def personalizar_relatorio(diretorio_relatorio: Path) -> Path:
    indice = Path(diretorio_relatorio) / "index.html"
    html = indice.read_text(encoding="utf-8")
    if MARCADOR in html:
        return indice

    icone = _icone_data_uri()
    css = (DIRETORIO_TEMA / "accenture-theme.css").read_text(encoding="utf-8")
    js = (DIRETORIO_TEMA / "accenture-theme.js").read_text(encoding="utf-8")

    html = re.sub(r'<link rel="icon"[^>]*>', "", html, count=1)
    html = re.sub(r"<title>.*?</title>", f"<title>{NOME_RELATORIO}</title>", html, count=1, flags=re.S)
    injecao = (
        f"{MARCADOR}\n"
        f'<link rel="icon" type="image/svg+xml" href="{icone}">\n'
        f"<style>:root {{ --acn-icone: url(\"{icone}\"); }}\n{css}</style>\n"
        f"<script>{js}</script>\n"
    )
    html = re.sub(r"<head[^>]*>", lambda m: m.group(0) + SCRIPT_TEMA_PADRAO, html, count=1)
    html = html.replace("</head>", injecao + "</head>", 1)
    indice.write_text(html, encoding="utf-8")
    return indice


if __name__ == "__main__":
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else "reports/allure-report")
    print(f"Tema Accenture aplicado em {personalizar_relatorio(destino)}")
