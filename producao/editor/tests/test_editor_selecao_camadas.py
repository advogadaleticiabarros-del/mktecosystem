"""Seleção de vários elementos, copiar e colar, e ordem das camadas, no editor em navegador real."""
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import expect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_editor import ambiente, el, elemento, navegador, salvo  # noqa: F401 (fixtures)


def ordem(acervo, peca="arte"):
    return [e["id"] for e in acervo.abrir(peca)["elementos"]]


def clicar(pagina, id, **extra):
    el(pagina, id).click(**extra)


def arrastar(pagina, id, dx, dy):
    q = el(pagina, id).bounding_box()
    pagina.mouse.move(q["x"] + 5, q["y"] + 5)
    pagina.mouse.down()
    pagina.mouse.move(q["x"] + 5 + dx, q["y"] + 5 + dy, steps=4)
    pagina.mouse.up()


def test_shift_clique_seleciona_dois_e_arrastar_move_os_dois_igual(ambiente):
    pagina, acervo, _ = ambiente
    clicar(pagina, "frase")
    clicar(pagina, "nome", modifiers=["Shift"])
    expect(pagina.locator("#painel")).to_contain_text("2 elementos")
    arrastar(pagina, "nome", 80, 40)
    salvo(pagina)
    frase, nome = elemento(acervo, "frase"), elemento(acervo, "nome")
    assert frase["x"] - 100 == nome["x"] - 100 > 50
    assert frase["y"] - 100 == nome["y"] - 400 > 20
    pagina.keyboard.press("Control+z")
    salvo(pagina)
    assert (elemento(acervo, "frase")["x"], elemento(acervo, "nome")["y"]) == (100, 400)


def test_laco_seleciona_so_o_que_fica_inteiro_dentro_e_setas_movem_todos(ambiente):
    pagina, acervo, _ = ambiente
    frase, nome = el(pagina, "frase").bounding_box(), el(pagina, "nome").bounding_box()
    pagina.mouse.move(frase["x"] - 12, frase["y"] - 12)  # fundo da arte, fora de qualquer elemento
    pagina.mouse.down()
    pagina.mouse.move(nome["x"] + nome["width"] + frase["width"], nome["y"] + nome["height"] + 6, steps=4)
    pagina.mouse.up()
    expect(pagina.locator("#painel")).to_contain_text("2 elementos")
    pagina.keyboard.press("ArrowRight")
    salvo(pagina)
    assert elemento(acervo, "frase")["x"] == 101 and elemento(acervo, "nome")["x"] == 101
    assert elemento(acervo, "foto")["x"] == 100


def test_clique_simples_em_um_do_grupo_deixa_so_ele_selecionado(ambiente):
    pagina, _, _ = ambiente
    clicar(pagina, "frase")
    clicar(pagina, "nome", modifiers=["Shift"])
    clicar(pagina, "nome")
    expect(pagina.locator("#painel h2").first).to_have_text("Nome")


def test_shift_clique_de_novo_tira_da_selecao(ambiente):
    pagina, _, _ = ambiente
    clicar(pagina, "frase")
    clicar(pagina, "nome", modifiers=["Shift"])
    clicar(pagina, "nome", modifiers=["Shift"])
    expect(pagina.locator("#painel h2").first).to_have_text("Frase")


def test_copiar_e_colar_foto_cria_outra_com_o_mesmo_arquivo_e_desfazer_tira(ambiente):
    pagina, acervo, _ = ambiente
    clicar(pagina, "foto")
    pagina.keyboard.press("Control+c")
    pagina.keyboard.press("Control+v")
    salvo(pagina)
    fotos = [e for e in acervo.abrir("arte")["elementos"] if e["tipo"] == "imagem"]
    assert len(fotos) == 2
    assert fotos[1]["arquivo"] == fotos[0]["arquivo"] and fotos[1]["id"] != fotos[0]["id"]
    assert fotos[1]["x"] != fotos[0]["x"]
    pagina.keyboard.press("Control+v")
    salvo(pagina)
    assert sum(e["tipo"] == "imagem" for e in acervo.abrir("arte")["elementos"]) == 3
    pagina.keyboard.press("Control+z")
    pagina.keyboard.press("Control+z")
    salvo(pagina)
    assert sum(e["tipo"] == "imagem" for e in acervo.abrir("arte")["elementos"]) == 1


def test_colar_foto_em_outra_peca_leva_o_arquivo_junto(ambiente):
    pagina, acervo, _ = ambiente
    pagina.once("dialog", lambda d: d.accept("arte-v2"))
    pagina.get_by_role("button", name="Nova versão").click()
    expect(pagina.locator("#peca")).to_have_value("arte-v2")
    acervo.criar("vazia", {"largura": 1080, "altura": 1440, "fundo": "#231E1A", "elementos": []})
    pagina.reload()
    expect(pagina.locator('#peca option[value="vazia"]')).to_have_count(1)
    pagina.locator("#peca").select_option("arte")
    expect(el(pagina, "foto")).to_be_visible()
    clicar(pagina, "foto")
    pagina.keyboard.press("Control+c")
    pagina.locator("#peca").select_option("vazia")
    expect(el(pagina, "foto")).to_have_count(0)
    pagina.locator("#palco-area").click(position={"x": 5, "y": 5})
    pagina.keyboard.press("Control+v")
    expect(pagina.locator("#palco .el-imagem")).to_have_count(1)
    salvo(pagina)
    foto = acervo.abrir("vazia")["elementos"][0]
    assert acervo.caminho_foto("vazia", foto["arquivo"]).exists()


def test_colar_imagem_copiada_de_fora_do_editor_vira_foto_nova(ambiente):
    pagina, acervo, _ = ambiente
    b = io.BytesIO()
    Image.new("RGB", (200, 100), "#777777").save(b, "PNG")
    pagina.evaluate("""async (bytes) => {
        const dt = new DataTransfer();
        dt.items.add(new File([new Uint8Array(bytes)], "print.png", { type: "image/png" }));
        document.body.dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true }));
    }""", list(b.getvalue()))
    expect(pagina.locator("#palco .el-imagem")).to_have_count(2)
    salvo(pagina)
    assert sum(e["tipo"] == "imagem" for e in acervo.abrir("arte")["elementos"]) == 2


def test_botoes_de_camada_levam_para_frente_tras_topo_e_fundo(ambiente):
    pagina, acervo, _ = ambiente
    assert ordem(acervo) == ["foto", "frase", "nome"]
    clicar(pagina, "frase")
    pagina.get_by_role("button", name="Para frente", exact=True).click()
    salvo(pagina)
    assert ordem(acervo) == ["foto", "nome", "frase"]
    pagina.get_by_role("button", name="Enviar para o fundo").click()
    salvo(pagina)
    assert ordem(acervo) == ["frase", "foto", "nome"]
    pagina.get_by_role("button", name="Trazer para o topo").click()
    salvo(pagina)
    assert ordem(acervo) == ["foto", "nome", "frase"]
    pagina.get_by_role("button", name="Para trás", exact=True).click()
    salvo(pagina)
    assert ordem(acervo) == ["foto", "frase", "nome"]
    assert pagina.evaluate("[...document.querySelectorAll('#palco .el')].map(n=>n.dataset.id)") == ["foto", "frase", "nome"]


def test_arrastar_na_lista_de_camadas_muda_a_ordem(ambiente):
    pagina, acervo, _ = ambiente
    linhas = pagina.locator("#camadas button")
    expect(linhas).to_have_text(["Nome", "Frase", "Foto"], use_inner_text=True)
    pagina.locator("#camadas button", has_text="Foto").drag_to(pagina.locator("#camadas button", has_text="Nome"), target_position={"x": 20, "y": 2})
    salvo(pagina)
    assert ordem(acervo) == ["frase", "nome", "foto"]


def test_luz_nova_pode_ser_ajustada_e_vira_brilho_redondo_na_arte(ambiente):
    pagina, acervo, _ = ambiente
    pagina.get_by_role("button", name="+ Luz").click()
    campo = pagina.get_by_label("Intensidade")
    campo.fill("0.4")
    campo.press("Tab")
    salvo(pagina)
    luz = next(e for e in acervo.abrir("arte")["elementos"] if e["tipo"] == "luz")
    assert luz["intensidade"] == 0.4
    estilo = pagina.evaluate("""() => { const s = getComputedStyle(document.querySelector('#palco .el-luz'));
        return { fundo: s.backgroundImage, opacidade: s.opacity, canto: s.borderTopLeftRadius }; }""")
    assert "radial-gradient" in estilo["fundo"] and estilo["opacidade"] == "0.4" and estilo["canto"] == "50%"


def test_fio_e_trecho_destacado_podem_ser_ouro_com_brilho(ambiente):
    pagina, acervo, _ = ambiente
    clicar(pagina, "frase")
    pagina.get_by_role("button", name="Ouro com brilho no destaque").click()
    salvo(pagina)
    assert elemento(acervo, "frase")["cor_destaque"] == "ouro-brilho"
    assert "linear-gradient" in pagina.evaluate("getComputedStyle(document.querySelector('#palco [data-id=frase] i')).backgroundImage")
    pagina.get_by_role("button", name="+ Fio").click()
    pagina.get_by_role("button", name="Ouro com brilho").click()
    salvo(pagina)
    fio = next(e for e in acervo.abrir("arte")["elementos"] if e["tipo"] == "retangulo")
    assert fio["cor"] == "ouro-brilho"
    assert "linear-gradient" in pagina.evaluate("getComputedStyle(document.querySelector('#palco .el-retangulo')).backgroundImage")


def test_botao_direito_abre_menu_com_camadas_e_copiar(ambiente):
    pagina, acervo, _ = ambiente
    el(pagina, "foto").click(button="right")
    menu = pagina.locator("#menu")
    expect(menu).to_be_visible()
    menu.get_by_role("button", name="Trazer para o topo").click()
    expect(menu).to_be_hidden()
    salvo(pagina)
    assert ordem(acervo) == ["frase", "nome", "foto"]
    el(pagina, "foto").click(button="right")
    menu.get_by_role("button", name="Copiar").click()
    el(pagina, "foto").click(button="right")
    menu.get_by_role("button", name="Colar").click()
    expect(pagina.locator("#palco .el-imagem")).to_have_count(2)
