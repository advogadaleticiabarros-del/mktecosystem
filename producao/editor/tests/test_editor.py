"""O editor de verdade, num navegador de verdade, como a Jessica usa."""
import io
import sys
import threading
from pathlib import Path

import pytest
from PIL import Image
from playwright.sync_api import expect, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acervo import Acervo
from servidor import criar_servidor, renderizar_playwright
from test_acervo import jpeg


def peca():
    return {"largura": 1080, "altura": 1440, "fundo": "#231E1A", "elementos": [
        {"id": "foto", "nome": "Foto", "tipo": "imagem", "x": 100, "y": 700, "largura": 300, "altura": 600, "arquivo": "foto.jpg", "pb": True},
        {"id": "frase", "nome": "Frase", "tipo": "texto", "x": 100, "y": 100, "html": "não é <i>cobrar.</i>", "fonte": "EB Garamond", "tamanho": 100, "cor": "#EFE6D9", "cor_destaque": "#C9A962"},
        {"id": "nome", "nome": "Nome", "tipo": "texto", "x": 100, "y": 400, "html": "LETÍCIA", "fonte": "Inter", "tamanho": 40, "cor": "#EFE6D9"},
    ]}


@pytest.fixture(scope="module")
def navegador():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def ambiente(tmp_path, navegador):
    acervo = Acervo(tmp_path)
    acervo.criar("arte", peca(), {"foto.jpg": jpeg()})
    servidor = criar_servidor(acervo, renderizar_playwright)  # o servidor roda em outra thread, com seu próprio Playwright
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    contexto = navegador.new_context(viewport={"width": 1500, "height": 950}, accept_downloads=True)
    pagina = contexto.new_page()
    pagina.goto(f"http://127.0.0.1:{servidor.server_port}/")
    expect(pagina.locator('#palco [data-id="frase"]')).to_be_visible()
    yield pagina, acervo, tmp_path
    contexto.close()
    servidor.shutdown()
    servidor.server_close()


def el(pagina, id):
    return pagina.locator(f'#palco [data-id="{id}"]')


def salvo(pagina):
    expect(pagina.locator("#situacao")).to_have_text("Salvo")


def elemento(acervo, id):
    return next(e for e in acervo.abrir("arte")["elementos"] if e["id"] == id)


def test_escrever_no_texto_salva_sozinho_e_mantem_so_marcacao_permitida(ambiente):
    pagina, acervo, _ = ambiente
    el(pagina, "nome").dblclick()
    pagina.keyboard.press("Control+A")
    pagina.keyboard.type("Dra. Letícia")
    pagina.keyboard.press("Enter")
    pagina.keyboard.type("Barros")
    pagina.locator("#palco-area").click(position={"x": 5, "y": 5})
    salvo(pagina)
    assert elemento(acervo, "nome")["html"] == "Dra. Letícia<br>Barros"


def test_arrastar_move_e_desfazer_volta(ambiente):
    pagina, acervo, _ = ambiente
    caixa = el(pagina, "nome").bounding_box()
    pagina.mouse.move(caixa["x"] + 5, caixa["y"] + 5)
    pagina.mouse.down()
    pagina.mouse.move(caixa["x"] + 105, caixa["y"] + 55, steps=4)
    pagina.mouse.up()
    salvo(pagina)
    movido = elemento(acervo, "nome")
    assert movido["x"] > 150 and movido["y"] > 430
    pagina.keyboard.press("Control+z")
    salvo(pagina)
    assert (elemento(acervo, "nome")["x"], elemento(acervo, "nome")["y"]) == (100, 400)


def test_setas_movem_um_pixel_e_com_shift_dez(ambiente):
    pagina, acervo, _ = ambiente
    el(pagina, "nome").click()
    pagina.keyboard.press("ArrowRight")
    pagina.keyboard.press("Shift+ArrowDown")
    salvo(pagina)
    assert (elemento(acervo, "nome")["x"], elemento(acervo, "nome")["y"]) == (101, 410)


def test_tamanho_nao_desce_de_22_e_avisa(ambiente):
    pagina, acervo, _ = ambiente
    el(pagina, "nome").click()
    campo = pagina.get_by_label("Tamanho")
    campo.fill("10")
    campo.press("Tab")
    expect(pagina.locator("#aviso")).to_contain_text("22 px")
    salvo(pagina)
    assert elemento(acervo, "nome")["tamanho"] == 22


def test_mudar_cor_para_ouro_com_brilho(ambiente):
    pagina, acervo, _ = ambiente
    el(pagina, "nome").click()
    pagina.get_by_role("button", name="Ouro com brilho").click()
    salvo(pagina)
    assert elemento(acervo, "nome")["cor"] == "ouro-brilho"


def test_baixar_imagem_gera_1080x1440_com_a_edicao_e_arquivo_novo_a_cada_vez(ambiente):
    pagina, acervo, raiz = ambiente
    el(pagina, "nome").click()
    pagina.keyboard.press("Delete")
    salvo(pagina)
    assert all(e["id"] != "nome" for e in acervo.abrir("arte")["elementos"])
    with pagina.expect_download() as d:
        pagina.get_by_role("button", name="Baixar imagem").click()
    imagem = Image.open(d.value.path())
    assert imagem.size == (1080, 1440)
    with pagina.expect_download():
        pagina.get_by_role("button", name="Baixar imagem").click()
    assert len(list((raiz / "saidas").glob("arte-*.jpg"))) == 2


def test_trocar_foto_mantem_largura_e_ajusta_altura(ambiente):
    pagina, acervo, _ = ambiente
    pagina.get_by_role("button", name="Foto", exact=True).click()
    b = io.BytesIO()
    Image.new("RGB", (200, 100), "#777777").save(b, "PNG")
    with pagina.expect_file_chooser() as escolha:
        pagina.get_by_role("button", name="Trocar foto").click()
    escolha.value.set_files({"name": "nova.png", "mimeType": "image/png", "buffer": b.getvalue()})
    pagina.wait_for_function("document.querySelector('#palco [data-id=foto] img').src.indexOf('foto.jpg')<0")
    salvo(pagina)
    foto = elemento(acervo, "foto")
    assert foto["arquivo"] != "foto.jpg" and foto["largura"] == 300 and foto["altura"] == 150


def test_nova_versao_nao_muda_a_peca_de_origem_e_original_pode_voltar(ambiente):
    pagina, acervo, _ = ambiente
    pagina.once("dialog", lambda d: d.accept("arte-v2"))
    pagina.get_by_role("button", name="Nova versão").click()
    expect(pagina.locator("#peca")).to_have_value("arte-v2")
    el(pagina, "nome").click()
    pagina.keyboard.press("Delete")
    salvo(pagina)
    assert any(e["id"] == "nome" for e in acervo.abrir("arte")["elementos"])
    assert all(e["id"] != "nome" for e in acervo.abrir("arte-v2")["elementos"])
    pagina.once("dialog", lambda d: d.accept())
    pagina.get_by_role("button", name="Voltar ao original").click()
    expect(el(pagina, "nome")).to_be_visible()
    assert any(e["id"] == "nome" for e in acervo.abrir("arte-v2")["elementos"])
