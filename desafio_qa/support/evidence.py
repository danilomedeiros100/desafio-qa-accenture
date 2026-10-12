"""Anexos e metadados do Allure Report.

Quando o behave roda sem o formatter do Allure, as chamadas abaixo não fazem nada.
"""
from __future__ import annotations

import json
import platform
from pathlib import Path

import allure
import allure_commons
from allure_commons.model2 import Label
from allure_commons.types import LabelType

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


def anexar_video(caminho: Path) -> None:
    allure.attach.file(str(caminho), name="Vídeo da execução", attachment_type=allure.attachment_type.WEBM)


TIPOS_DE_TESTE = {"api": "Testes de API", "frontend": "Testes de Front-end"}

# Classificação das falhas exibida na aba "Categorias" do Allure
CATEGORIAS_DE_FALHA = [
    {"name": "Falha de validação (assert)", "matchedStatuses": ["failed"]},
    {"name": "Tempo esgotado (timeout)", "matchedStatuses": ["broken", "failed"],
     "messageRegex": ".*Timeout.*"},
    {"name": "Erro de automação (exceção no código de teste)", "matchedStatuses": ["broken"]},
    {"name": "Steps não implementados", "matchedStatuses": ["skipped"],
     "messageRegex": ".*undefined.*"},
]


def categorizar_cenario(tags: set[str], funcionalidade: str) -> None:
    """Agrupa o cenário por tipo de teste (API x Front-end) nas abas Suítes e Comportamentos.

    O allure-behave não implementa `allure.dynamic.label`, então os rótulos são adicionados
    direto no resultado do cenário em andamento (já criado quando o before_scenario roda)."""
    resultado = _resultado_em_andamento()
    if resultado is None:  # behave executado sem o formatter do Allure
        return
    tipo = next((nome for tag, nome in TIPOS_DE_TESTE.items() if tag in tags), "Outros testes")
    resultado.labels.extend([
        Label(name=LabelType.PARENT_SUITE, value=tipo),
        Label(name=LabelType.SUITE, value=funcionalidade),
        Label(name=LabelType.EPIC, value=tipo),
    ])


def _resultado_em_andamento():
    for plugin in allure_commons.plugin_manager.get_plugins():
        logger = getattr(plugin, "logger", None)
        if logger is not None and hasattr(logger, "get_test"):
            return logger.get_test(None)
    return None


def registrar_categorias(diretorio_resultados: Path) -> None:
    if diretorio_resultados.is_dir():
        (diretorio_resultados / "categories.json").write_text(
            json.dumps(CATEGORIAS_DE_FALHA, indent=2, ensure_ascii=False), encoding="utf-8"
        )


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
