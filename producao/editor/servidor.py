"""Servidor local do editor: só escuta neste computador. Uso: python servidor.py (ou Abrir editor.bat)."""
import json
import mimetypes
import re
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from acervo import Acervo, PecaInvalida

AQUI = Path(__file__).resolve().parent
WEB = AQUI / "web"
PORTA = 8765
LIMITE_ENVIO = 40 * 1024 * 1024
_ARQUIVO_WEB = re.compile(r"^[a-z0-9_-]+\.(html|js|css|woff2)$")


def renderizar_playwright(url):
    """Abre a página da peça num Chromium limpo e devolve o JPG 1080×1440."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        try:
            pagina = navegador.new_page(viewport={"width": 1080, "height": 1440})
            pagina.goto(url, wait_until="networkidle")
            pagina.wait_for_selector("body[data-pronto]", state="attached", timeout=30000)
            return pagina.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440}, type="jpeg", quality=92)
        finally:
            navegador.close()


def criar_servidor(acervo, renderizar, porta=0):
    """renderizar(url) -> bytes do JPG. porta=0 escolhe uma porta livre."""
    trava_exportar = threading.Lock()

    class Pedido(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def _responder(self, status, corpo=b"", tipo="application/json; charset=utf-8"):
            self.send_response(status)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(corpo)

        def _json(self, dados, status=200):
            self._responder(status, json.dumps(dados, ensure_ascii=False).encode("utf-8"))

        def _arquivo(self, caminho):
            if not caminho.is_file():
                return self._responder(404)
            tipo = mimetypes.guess_type(caminho.name)[0] or "application/octet-stream"
            if tipo.startswith("text/") or tipo.endswith("javascript"):
                tipo += "; charset=utf-8"
            self._responder(200, caminho.read_bytes(), tipo)

        def _origem_permitida(self):
            porta_real = self.server.server_port
            locais = {f"127.0.0.1:{porta_real}", f"localhost:{porta_real}"}
            if self.headers.get("Host") not in locais:
                return False
            origem = self.headers.get("Origin")
            return origem is None or origem in {f"http://{h}" for h in locais}

        def _corpo(self):
            tamanho = int(self.headers.get("Content-Length") or 0)
            if tamanho > LIMITE_ENVIO:
                raise PecaInvalida("Arquivo grande demais (limite de 40 MB).")
            return self.rfile.read(tamanho)

        def _tratar(self):
            if not self._origem_permitida():
                return self._responder(403)
            caminho = unquote(urlsplit(self.path).path)
            partes = caminho.strip("/").split("/")
            try:
                self._rotear(caminho, partes)
            except PecaInvalida as erro:
                self._json({"erro": str(erro)}, 400)
            except json.JSONDecodeError:
                self._json({"erro": "Dados inválidos."}, 400)

        def _rotear(self, caminho, partes):
            m = self.command
            if m == "GET" and caminho == "/":
                return self._arquivo(WEB / "index.html")
            if m == "GET" and len(partes) == 2 and partes[0] == "web":
                return self._arquivo(WEB / partes[1]) if _ARQUIVO_WEB.match(partes[1]) else self._responder(404)
            if m == "GET" and caminho == "/api/pecas":
                return self._json(acervo.nomes())
            if m == "GET" and len(partes) == 3 and partes[:2] == ["api", "saidas"]:
                return self._arquivo(acervo.caminho_saida(partes[2]))
            if len(partes) < 3 or partes[:2] != ["api", "pecas"]:
                return self._responder(404)
            nome, acao = partes[2], partes[3:]
            if m == "GET" and not acao:
                return self._json(acervo.abrir(nome))
            if m == "GET" and len(acao) == 2 and acao[0] == "fotos":
                return self._arquivo(acervo.caminho_foto(nome, acao[1]))
            if m == "PUT" and not acao:
                acervo.salvar(nome, json.loads(self._corpo()))
                return self._json({"ok": True})
            if m == "POST" and acao == ["foto"]:
                return self._json(acervo.guardar_foto(nome, self._corpo()))
            if m == "POST" and acao == ["restaurar"]:
                return self._json(acervo.restaurar(nome))
            if m == "POST" and acao == ["copia"]:
                novo = json.loads(self._corpo()).get("nome", "")
                acervo.copiar(nome, novo)
                return self._json({"nome": novo})
            if m == "POST" and acao == ["exportar"]:
                acervo.abrir(nome)
                with trava_exportar:
                    dados = renderizar(f"http://127.0.0.1:{self.server.server_port}/web/render.html?peca={nome}")
                return self._json({"arquivo": acervo.guardar_saida(nome, dados).name})
            self._responder(404)

        do_GET = do_PUT = do_POST = _tratar

    return ThreadingHTTPServer(("127.0.0.1", porta), Pedido)


def _ja_aberto(porta):
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", porta)) == 0


def main():
    endereco = f"http://127.0.0.1:{PORTA}/"
    if _ja_aberto(PORTA):
        webbrowser.open(endereco)
        return
    servidor = criar_servidor(Acervo(AQUI), renderizar_playwright, PORTA)
    print(f"Editor aberto em {endereco}\nDeixe esta janela aberta enquanto edita. Para encerrar, feche-a.")
    threading.Timer(0.5, webbrowser.open, [endereco]).start()
    servidor.serve_forever()


if __name__ == "__main__":
    main()
