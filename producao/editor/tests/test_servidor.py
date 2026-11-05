import http.client
import json
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acervo import Acervo
from servidor import criar_servidor
from test_acervo import doc, jpeg, texto


@pytest.fixture
def ambiente(tmp_path):
    acervo = Acervo(tmp_path)
    acervo.criar("arte", doc())
    urls = []

    def renderizar(url):
        urls.append(url)
        return b"imagem-renderizada"

    servidor = criar_servidor(acervo, renderizar)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    yield servidor.server_port, urls, acervo
    servidor.shutdown()
    servidor.server_close()


def pedir(porta, metodo, caminho, corpo=None, cabecalhos=None):
    c = http.client.HTTPConnection("127.0.0.1", porta, timeout=5)
    dados = json.dumps(corpo).encode() if isinstance(corpo, (dict, list)) else corpo
    c.request(metodo, caminho, dados, cabecalhos or {})
    r = c.getresponse()
    return r.status, r.read()


def test_lista_e_salva_peca(ambiente):
    porta, _, acervo = ambiente
    status, corpo = pedir(porta, "GET", "/api/pecas")
    assert status == 200 and json.loads(corpo) == ["arte"]
    novo = doc(texto(html="Editado"))
    assert pedir(porta, "PUT", "/api/pecas/arte", novo)[0] == 200
    assert acervo.abrir("arte") == novo


def test_regra_da_marca_volta_como_erro_legivel(ambiente):
    porta, _, acervo = ambiente
    status, corpo = pedir(porta, "PUT", "/api/pecas/arte", doc(texto(tamanho=10)))
    assert status == 400 and "22 px" in json.loads(corpo)["erro"]
    assert acervo.abrir("arte") == doc()


def test_exportar_renderiza_a_propria_pagina_da_peca_e_guarda_arquivo_novo(ambiente):
    porta, urls, acervo = ambiente
    status, corpo = pedir(porta, "POST", "/api/pecas/arte/exportar")
    assert status == 200
    arquivo = json.loads(corpo)["arquivo"]
    assert urls == [f"http://127.0.0.1:{porta}/web/render.html?peca=arte"]
    status, imagem = pedir(porta, "GET", f"/api/saidas/{arquivo}")
    assert status == 200 and imagem == b"imagem-renderizada"


def test_enviar_foto_e_buscar_de_volta(ambiente):
    porta, _, _ = ambiente
    status, corpo = pedir(porta, "POST", "/api/pecas/arte/foto", jpeg())
    assert status == 200
    status, imagem = pedir(porta, "GET", f"/api/pecas/arte/fotos/{json.loads(corpo)['arquivo']}")
    assert status == 200 and imagem[:2] == b"\xff\xd8"


def test_copia_e_restaurar(ambiente):
    porta, _, acervo = ambiente
    assert pedir(porta, "POST", "/api/pecas/arte/copia", {"nome": "arte-v2"})[0] == 200
    assert "arte-v2" in acervo.nomes()
    pedir(porta, "PUT", "/api/pecas/arte", doc(texto(html="Mudei")))
    status, corpo = pedir(porta, "POST", "/api/pecas/arte/restaurar")
    assert status == 200 and json.loads(corpo) == doc()


def test_outro_site_nao_consegue_alterar_nem_ler_peca(ambiente):
    porta, _, acervo = ambiente
    malicioso = {"Origin": "https://site-malicioso.example"}
    assert pedir(porta, "PUT", "/api/pecas/arte", doc(texto(html="Hack")), malicioso)[0] == 403
    assert pedir(porta, "POST", "/api/pecas/arte/exportar", None, malicioso)[0] == 403
    assert pedir(porta, "GET", "/api/pecas", None, {"Host": "site-malicioso.example"})[0] == 403
    assert acervo.abrir("arte") == doc()


@pytest.mark.parametrize("caminho", ["/web/../acervo.py", "/web/..%2facervo.py", "/web/%2e%2e/servidor.py"])
def test_nao_entrega_arquivo_fora_da_pasta_web(ambiente, caminho):
    assert pedir(ambiente[0], "GET", caminho)[0] == 404
