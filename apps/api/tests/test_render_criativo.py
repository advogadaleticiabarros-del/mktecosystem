import pytest
from PIL import Image

from app.services.render_criativo import renderizar_slide

IDENTIDADE_VISUAL_TESTE = {
    "cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"},
}


@pytest.mark.anyio
async def test_renderiza_slide_1080x1350(tmp_path):
    saida = tmp_path / "slide-1.png"
    await renderizar_slide(
        texto="Direitos da gestante no trabalho",
        indice=0,
        total=5,
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    assert saida.exists()
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)


@pytest.mark.anyio
async def test_renderiza_card_de_pergunta_1080x1350(tmp_path):
    from app.services.render_criativo import renderizar_pergunta

    saida = tmp_path / "pergunta.png"
    await renderizar_pergunta(
        pergunta="Fui demitida grávida. E agora?",
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)


def test_pergunta_segue_o_padrao_aprovado_caixa_centralizada_sobre_foto():
    """Padrão aprovado em 09/10/2026 (pergunta v6): foto inteira de fundo, caixa de vidro
    centralizada com faixa "Me faça uma pergunta", destaque em itálico dourado, perfil no
    rodapé da caixa, área no cabeçalho e "A resposta está na legenda"."""
    from app.services.render_criativo import html_pergunta

    html = html_pergunta("Fui demitida grávida. <em>E agora?</em>", IDENTIDADE_VISUAL_TESTE,
                         area="Trabalhista", foto_src="data:image/jpeg;base64,AAA")

    assert "translate(-50%,-50%)" in html
    assert "Me faça uma pergunta" in html
    assert "<em>E agora?</em>" in html
    assert "adv.leticiabarros2" in html
    assert "Trabalhista" in html
    assert "A resposta está na" in html
    assert 'class="foto" src="data:image/jpeg;base64,AAA"' in html


def test_pergunta_sem_foto_usa_fundo_cafe_com_marca_dagua():
    from app.services.render_criativo import html_pergunta

    html = html_pergunta("Posso ser demitida?", IDENTIDADE_VISUAL_TESTE)

    assert 'class="foto"' not in html
    assert 'class="marca"' in html


@pytest.mark.anyio
async def test_renderiza_pergunta_com_foto(tmp_path):
    from app.services.render_criativo import renderizar_pergunta

    foto = tmp_path / "foto.jpg"
    Image.new("RGB", (800, 1200), "#6B4F35").save(foto)
    saida = tmp_path / "pergunta.png"
    await renderizar_pergunta("Tenho direito? <em>Pode?</em>", IDENTIDADE_VISUAL_TESTE, str(saida),
                              foto_path=str(foto), area="Consumidor")
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)


def test_mito_ou_lei_segue_o_padrao_aprovado_selo_no_topo_do_cartao():
    """Padrão aprovado em 09/10/2026 (Mito ou Lei v3): afirmação e explicação no mesmo
    cartão de vidro, selo encaixado no topo do cartão (nunca entre os blocos), afirmação
    riscada no MITO, rótulo "A verdade" e convite para salvar."""
    from app.services.render_criativo import html_mito_ou_lei

    html = html_mito_ou_lei("Salário nunca pode ser penhorado.", "MITO",
                            "O STJ admite penhorar parte do salário.", "STJ, Tema 1.230", IDENTIDADE_VISUAL_TESTE)
    assert "Série · Mito ou Lei" in html
    assert 'class="selo"' in html and "VEREDITO" in html
    assert html.index('class="selo"') < html.index('class="sec1"') < html.index('class="sec2"')
    assert 'class="af mito"' in html and 'penhorado<span class="aspa">”' in html  # ponto final removido
    assert "A verdade" in html and "Salve para consultar quando precisar" in html
    assert "OAB/ES 39.948" in html


def test_mito_ou_lei_veredito_lei_sem_risco_e_com_rotulo_da_lei():
    from app.services.render_criativo import html_mito_ou_lei

    html = html_mito_ou_lei("Mesário ganha 2 dias de folga.", "LEI", "E o treinamento conta.",
                            "Lei 9.504/1997, art. 98", IDENTIDADE_VISUAL_TESTE)
    assert 'class="af mito"' not in html
    assert "O que diz a lei" in html


def test_mito_ou_lei_abrevia_referencia_longa_para_caber_numa_linha():
    from app.services.render_criativo import html_mito_ou_lei

    html = html_mito_ou_lei("O chefe pode pedir voto.", "MITO", "É assédio eleitoral.",
                            "Código Eleitoral, art. 301; Resolução TSE 23.610/2019", IDENTIDADE_VISUAL_TESTE)
    assert "Cód. Eleitoral, art. 301; Res. TSE 23.610/2019" in html


def test_mito_ou_lei_rejeita_veredito_desconhecido():
    from app.services.render_criativo import html_mito_ou_lei

    with pytest.raises(ValueError):
        html_mito_ou_lei("Algo.", "TALVEZ", "x", "y", IDENTIDADE_VISUAL_TESTE)


@pytest.mark.anyio
async def test_renderiza_mito_ou_lei_1080x1350(tmp_path):
    from app.services.render_criativo import renderizar_mito_ou_lei

    saida = tmp_path / "mito.png"
    await renderizar_mito_ou_lei("Salário nunca pode ser penhorado.", "MITO", "O STJ admite exceções.",
                                 "STJ, Tema 1.230", IDENTIDADE_VISUAL_TESTE, str(saida))
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)
