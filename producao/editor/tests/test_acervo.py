import io
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acervo import Acervo, PecaInvalida


def texto(**extra):
    return {"id": "t1", "tipo": "texto", "x": 10, "y": 10, "html": "Oi", "fonte": "Inter", "tamanho": 30, "cor": "#ffffff"} | extra


def doc(*elementos):
    return {"largura": 1080, "altura": 1440, "fundo": "#231E1A", "elementos": list(elementos) or [texto()]}


def jpeg():
    b = io.BytesIO()
    Image.new("RGB", (40, 80), "#888888").save(b, "JPEG")
    return b.getvalue()


@pytest.fixture
def acervo(tmp_path):
    return Acervo(tmp_path)


def test_peca_salva_volta_igual_ao_abrir(acervo):
    acervo.criar("arte", doc())
    novo = doc(texto(html="Mudei"))
    acervo.salvar("arte", novo)
    assert acervo.abrir("arte") == novo
    assert acervo.nomes() == ["arte"]


def test_restaurar_volta_ao_estado_de_quando_a_peca_foi_criada(acervo):
    acervo.criar("arte", doc(texto(html="Primeira")))
    acervo.salvar("arte", doc(texto(html="Segunda")))
    assert acervo.restaurar("arte")["elementos"][0]["html"] == "Primeira"
    assert acervo.abrir("arte")["elementos"][0]["html"] == "Primeira"


def test_criar_com_nome_existente_nao_sobrescreve(acervo):
    acervo.criar("arte", doc(texto(html="Pronta")))
    with pytest.raises(PecaInvalida):
        acervo.criar("arte", doc(texto(html="Outra")))
    assert acervo.abrir("arte")["elementos"][0]["html"] == "Pronta"


def test_copia_e_peca_independente_com_as_mesmas_fotos(acervo):
    acervo.criar("arte", doc())
    foto = acervo.guardar_foto("arte", jpeg())["arquivo"]
    acervo.copiar("arte", "arte-v2")
    acervo.salvar("arte-v2", doc(texto(html="Só na cópia")))
    assert acervo.abrir("arte")["elementos"][0]["html"] == "Oi"
    assert acervo.caminho_foto("arte-v2", foto).exists()


@pytest.mark.parametrize("ruim", [
    texto(tamanho=21),
    texto(fonte="Cormorant Garamond"),
    {"id": "x", "tipo": "video", "x": 0, "y": 0},
    {"id": "i", "tipo": "imagem", "x": 0, "y": 0, "largura": 100, "altura": 100, "arquivo": "../fora.jpg"},
])
def test_regras_da_marca_barram_elemento_invalido(acervo, ruim):
    acervo.criar("arte", doc())
    with pytest.raises(PecaInvalida):
        acervo.salvar("arte", doc(ruim))
    assert acervo.abrir("arte") == doc()


@pytest.mark.parametrize("nome", ["../fora", "a/b", "", "a\\b", ".."])
def test_nome_fora_da_pasta_e_recusado(acervo, nome):
    with pytest.raises(PecaInvalida):
        acervo.criar(nome, doc())


def test_foto_guardada_informa_o_tamanho_e_arquivo_invalido_e_recusado(acervo):
    acervo.criar("arte", doc())
    foto = acervo.guardar_foto("arte", jpeg())
    assert (foto["largura"], foto["altura"]) == (40, 80)
    with pytest.raises(PecaInvalida):
        acervo.guardar_foto("arte", b"isto nao e imagem")


def test_foto_de_outra_pasta_nao_e_entregue(acervo):
    acervo.criar("arte", doc())
    with pytest.raises(PecaInvalida):
        acervo.caminho_foto("arte", "../peca.json")


def test_peca_pode_nascer_com_fotos_e_o_original_ja_as_inclui(acervo):
    foto = {"id": "f", "tipo": "imagem", "x": 0, "y": 0, "largura": 100, "altura": 100, "arquivo": "foto.jpg"}
    acervo.criar("arte", doc(foto), {"foto.jpg": jpeg()})
    assert acervo.caminho_foto("arte", "foto.jpg").exists()
    assert acervo.restaurar("arte")["elementos"][0]["arquivo"] == "foto.jpg"


def test_saida_nunca_sobrescreve_arquivo_anterior(acervo):
    acervo.criar("arte", doc())
    a = acervo.guardar_saida("arte", b"um")
    b = acervo.guardar_saida("arte", b"dois")
    assert a != b
    assert a.read_bytes() == b"um" and b.read_bytes() == b"dois"


def test_playfair_display_e_aceita_para_o_estilo_manchete(acervo):
    acervo.criar("arte", doc(texto(fonte="Playfair Display")))
    assert acervo.abrir("arte")["elementos"][0]["fonte"] == "Playfair Display"
