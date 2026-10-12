"""Configurações centrais do projeto, sobrescrevíveis por variáveis de ambiente."""
import os
from pathlib import Path

DIRETORIO_RAIZ = Path(__file__).resolve().parents[1]

URL_BASE = os.getenv("BASE_URL", "https://demoqa.com").rstrip("/")

NAVEGADOR = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
HEADLESS = os.getenv("HEADLESS", "true").lower() not in ("false", "0", "no", "nao", "não")
ATRASO_ENTRE_ACOES_MS = int(os.getenv("SLOW_MO", "0"))
TIMEOUT_PADRAO_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))
TAMANHO_JANELA = {"width": 1920, "height": 1080}
GRAVAR_VIDEO = os.getenv("RECORD_VIDEO", "false").lower() in ("true", "1", "yes", "sim")

TIMEOUT_API_S = int(os.getenv("API_TIMEOUT_S", "30"))

ARQUIVO_UPLOAD = DIRETORIO_RAIZ / "resources" / "upload" / "arquivo_upload.txt"
DIRETORIO_RELATORIOS = DIRETORIO_RAIZ / "reports"
DIRETORIO_SCREENSHOTS = DIRETORIO_RELATORIOS / "screenshots"
DIRETORIO_TRACES = DIRETORIO_RELATORIOS / "traces"
DIRETORIO_VIDEOS = DIRETORIO_RELATORIOS / "videos"
