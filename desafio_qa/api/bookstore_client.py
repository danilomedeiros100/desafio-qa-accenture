"""Cliente da API Book Store do demoqa (Swagger: https://demoqa.com/swagger/)."""
from __future__ import annotations

import time

import requests

from desafio_qa.config import TIMEOUT_API_S, URL_BASE
from desafio_qa.support import evidence, terminal


class ClienteBookStore:
    CONTA = "/Account/v1"
    LIVRARIA = "/BookStore/v1"

    def __init__(self, url_base: str = URL_BASE, timeout: int = TIMEOUT_API_S):
        self.url_base = url_base
        self.timeout = timeout
        self.sessao = requests.Session()
        self.sessao.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )

    # ---------- auxiliares ----------
    def _requisitar(self, metodo: str, caminho: str, token: str | None = None, **kwargs) -> requests.Response:
        """Executa a requisição e imprime no terminal método, rota, status e tempo."""
        cabecalhos = {"Authorization": f"Bearer {token}"} if token else {}
        inicio = time.perf_counter()
        resposta = self.sessao.request(
            metodo, f"{self.url_base}{caminho}", headers=cabecalhos, timeout=self.timeout, **kwargs
        )
        duracao = time.perf_counter() - inicio
        terminal.acao(f"{metodo} {caminho} -> {resposta.status_code} ({duracao:.2f}s)")
        self._anexar_no_allure(metodo, caminho, kwargs.get("json"), resposta)
        return resposta

    @staticmethod
    def _anexar_no_allure(metodo: str, caminho: str, corpo_requisicao, resposta: requests.Response) -> None:
        try:
            corpo_resposta = resposta.json()
        except ValueError:
            corpo_resposta = resposta.text
        if isinstance(corpo_requisicao, dict) and "password" in corpo_requisicao:
            corpo_requisicao = {**corpo_requisicao, "password": "***"}
        evidence.anexar_json(
            f"{metodo} {caminho}",
            {
                "requisicao": {"metodo": metodo, "url": resposta.url, "corpo": corpo_requisicao},
                "resposta": {"status": resposta.status_code, "corpo": corpo_resposta},
            },
        )

    # ---------- Account ----------
    def criar_usuario(self, nome_usuario: str, senha: str) -> requests.Response:
        return self._requisitar(
            "POST", f"{self.CONTA}/User", json={"userName": nome_usuario, "password": senha}
        )

    def gerar_token(self, nome_usuario: str, senha: str) -> requests.Response:
        return self._requisitar(
            "POST", f"{self.CONTA}/GenerateToken", json={"userName": nome_usuario, "password": senha}
        )

    def verificar_autorizacao(self, nome_usuario: str, senha: str) -> requests.Response:
        return self._requisitar(
            "POST", f"{self.CONTA}/Authorized", json={"userName": nome_usuario, "password": senha}
        )

    def consultar_usuario(self, id_usuario: str, token: str) -> requests.Response:
        return self._requisitar("GET", f"{self.CONTA}/User/{id_usuario}", token=token)

    def excluir_usuario(self, id_usuario: str, token: str) -> requests.Response:
        return self._requisitar("DELETE", f"{self.CONTA}/User/{id_usuario}", token=token)

    # ---------- BookStore ----------
    def listar_livros(self) -> requests.Response:
        return self._requisitar("GET", f"{self.LIVRARIA}/Books")

    def alugar_livros(self, id_usuario: str, isbns: list[str], token: str) -> requests.Response:
        return self._requisitar(
            "POST",
            f"{self.LIVRARIA}/Books",
            token=token,
            json={"userId": id_usuario, "collectionOfIsbns": [{"isbn": i} for i in isbns]},
        )
