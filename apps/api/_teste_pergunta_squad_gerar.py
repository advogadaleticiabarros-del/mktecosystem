import asyncio
import base64
from pathlib import Path

from jinja2 import Template
from PIL import Image
from playwright.async_api import async_playwright

ACABAMENTO_PATH = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/"
    "ementos rdape dourado/cabeçalho e rodape.png"
)
LOGO_PATH = Path("C:/tmp/mktecosystem/logo/logo-800x800.png")
FUNDO_PATH = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/"
    "ementos rdape dourado/use esse fundo.png"
)
AVATAR_PATH = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/Advogada/"
    "Gemini_Generated_Image_rrg4ylrrg4ylrrg4.png"
)
FOTO_PATH = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/"
    "SEM FUNDO/Mulher demitida.png"
)
OUT_DIR = Path(__file__).parent / "_teste_pergunta_output"

PERGUNTA = "Fui demitida. Até quando posso processar a empresa?"
ESPECIALIDADE = "Advogada | Letícia Barros | Direito Trabalhista"

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800;900&display=swap" rel="stylesheet">
<style>
  :root {
    --dourado:        #C9A962;
    --dourado-claro:  #E8D7A6;
    --dourado-escuro: #A8863F;
    --grad-dourado:   linear-gradient(135deg, #E8D7A6 0%, #C9A962 45%, #A8863F 100%);
    --creme:          #F3EAD4;
    --creme-alt:      #EADFC1;
    --texto-escuro:   #3B2E1D;
    --texto-suave:    #6B5B3E;
    --azul-verificado:#3897F0;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { margin: 0; }

  .creative {
    width: 1080px;
    height: 1350px;
    position: relative;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
    color: var(--texto-escuro);
  }

  /* Fundo com textura dourada e selo em relevo (arquivo pronto da usuária) */
  .fundo {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
  }

  /* Moldura sutil */
  .creative::before {
    content: '';
    position: absolute;
    inset: 44px;
    border: 1.5px solid rgba(168,134,63,0.35);
    border-radius: 18px;
    pointer-events: none;
    z-index: 3;
  }

  /* Foto recortada (fundo transparente), em primeiro plano */
  .foto-wrap {
    position: absolute;
    right: -30px;
    bottom: 0;
    width: 760px;
    height: 950px;
    z-index: 2;
    filter: drop-shadow(-14px 10px 26px rgba(59,46,29,0.28));
    /* A imagem de origem tem cortes retos nas bordas esquerda/direita (o
       recorte de fundo esbarrou no limite do canvas). Esmaece só essas
       duas bordas pra dissolver no fundo em vez de terminar em linha reta;
       o contorno da pessoa em si já tem alpha limpo e fica intocado. */
    -webkit-mask-image: linear-gradient(90deg, transparent 0%, black 22%, black 88%, transparent 100%);
    mask-image: linear-gradient(90deg, transparent 0%, black 22%, black 88%, transparent 100%);
  }
  .foto-wrap img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: bottom right;
  }

  .conteudo {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 108px 96px 0;
    height: 100%;
  }

  .selo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    filter:
      drop-shadow(0 4px 10px rgba(168,134,63,0.45))
      drop-shadow(0 14px 34px rgba(168,134,63,0.35))
      drop-shadow(0 26px 60px rgba(201,169,98,0.22));
  }
  .selo img {
    width: 150px;
    height: 150px;
    object-fit: contain;
  }

  .bubble {
    margin-top: 44px;
    width: 700px;
    max-width: 100%;
  }
  .bubble__topo {
    background: var(--grad-dourado);
    color: var(--texto-escuro);
    font-weight: 800;
    font-size: 26px;
    letter-spacing: 0.5px;
    text-align: center;
    padding: 18px 32px;
    border-radius: 22px 22px 0 0;
  }
  .bubble__corpo {
    background: #FFFDF7;
    border: 2px dashed rgba(168,134,63,0.55);
    border-top: none;
    border-radius: 0 0 22px 22px;
    padding: 44px 40px 48px;
    text-align: center;
  }
  .bubble__pergunta {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 48px;
    line-height: 1.28;
    color: var(--texto-escuro);
  }

  .perfil {
    margin-top: 40px;
    display: inline-flex;
    align-items: center;
    gap: 16px;
    background: rgba(255,253,247,0.75);
    border: 1px solid rgba(168,134,63,0.30);
    border-radius: 999px;
    padding: 12px 26px 12px 12px;
  }
  .perfil__avatar {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    object-fit: cover;
    object-position: 50% 22%;
    border: 2px solid var(--dourado);
  }
  .perfil__texto {
    display: flex;
    flex-direction: column;
    text-align: left;
  }
  .perfil__handle {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 700;
    font-size: 22px;
    color: var(--texto-escuro);
  }
  .verificado {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--azul-verificado);
    color: white;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
  }
  .perfil__sub {
    font-size: 16px;
    color: var(--texto-suave);
    margin-top: 2px;
  }
</style>
</head>
<body>
  <div class="creative">
    <img class="fundo" src="{{ fundo_src }}" alt="">

    <div class="foto-wrap"><img src="{{ foto_src }}" alt=""></div>

    <div class="conteudo">
      <div class="selo"><img src="{{ logo_src }}" alt="Letícia Barros"></div>

      <div class="bubble">
        <div class="bubble__topo">Me faça uma pergunta:</div>
        <div class="bubble__corpo">
          <p class="bubble__pergunta">{{ pergunta }}</p>
        </div>
      </div>

      <div class="perfil">
        <img class="perfil__avatar" src="{{ avatar_src }}" alt="">
        <div class="perfil__texto">
          <span class="perfil__handle">adv.leticiabarros2 <span class="verificado">&#10003;</span></span>
          <span class="perfil__sub">{{ especialidade }}</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""


def arquivo_para_data_uri(caminho: Path, mime: str) -> str:
    dados = base64.b64encode(caminho.read_bytes()).decode()
    return f"data:{mime};base64,{dados}"


def aplicar_acabamento_dourado(caminho_png: Path) -> None:
    base = Image.open(caminho_png).convert("RGBA")
    acabamento = Image.open(ACABAMENTO_PATH).convert("RGBA")
    if acabamento.size != base.size:
        acabamento = acabamento.resize(base.size)
    composto = Image.alpha_composite(base, acabamento)
    composto.convert("RGB").save(caminho_png)


async def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    template = Template(TEMPLATE_HTML)

    html = template.render(
        logo_src=arquivo_para_data_uri(LOGO_PATH, "image/png"),
        fundo_src=arquivo_para_data_uri(FUNDO_PATH, "image/png"),
        avatar_src=arquivo_para_data_uri(AVATAR_PATH, "image/png"),
        foto_src=arquivo_para_data_uri(FOTO_PATH, "image/png"),
        pergunta=PERGUNTA,
        especialidade=ESPECIALIDADE,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html)
        caminho = OUT_DIR / "criativo-pergunta.png"
        await page.screenshot(path=str(caminho))
        await page.close()
        await browser.close()

    aplicar_acabamento_dourado(caminho)
    print(f"Criativo salvo em {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
