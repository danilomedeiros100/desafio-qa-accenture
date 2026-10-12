"""Anexos e metadados do Allure Report.

Quando o behave roda sem o formatter do Allure, as chamadas abaixo não fazem nada.
"""
from __future__ import annotations

import json
import platform
from pathlib import Path

import allure

from desafio_qa import config


def anexar_screenshot(pagina, nome: str = "screenshot") -> bytes | None:
    try:
        imagem = pagina.screenshot(full_page=True)
    except Exception:  # noqa: BLE001 - evidência é best-effort
        return None
    allure.attach(imagem, name=nome, attachment_type=allure.attachment_type.PNG)
    return imagem


def anexar_json(nome: str, conteudo) -> None:
    allure.attach(
        json.dumps(conteudo, indent=2, ensure_ascii=False, default=str),
        name=nome,
        attachment_type=allure.attachment_type.JSON,
    )


def anexar_texto(nome: str, conteudo: str) -> None:
    allure.attach(conteudo, name=nome, attachment_type=allure.attachment_type.TEXT)


def anexar_arquivo(caminho: Path, nome: str, extensao: str) -> None:
    allure.attach.file(str(caminho), name=nome, extension=extensao)


def registrar_ambiente(diretorio_resultados: Path) -> None:
    """Gera o environment.properties exibido no widget 'Environment' do Allure."""
    if not diretorio_resultados.is_dir():
        return
    propriedades = {
        "URL_BASE": config.URL_BASE,
        "Navegador": config.NAVEGADOR,
        "Headless": config.HEADLESS,
        "Python": platform.python_version(),
        "Sistema": f"{platform.system()} {platform.release()}",
    }
    linhas = [f"{chave}={valor}" for chave, valor in propriedades.items()]
    (diretorio_resultados / "environment.properties").write_text("\n".join(linhas), encoding="utf-8")
