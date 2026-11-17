"""Página de conferência da série 23 para a Dra. Letícia aprovar (regra de 11/11/2026: entrega com arquivo de conferência).
Os vídeos vão como prévia leve (720x1280, ~13 MB) publicada junto da página; os arquivos finais (1080x1920, 11 Mbps)
ficam em C:\\tmp\\videos-reels\\23-reels-3\\.
Uso: py pagina.py <pasta_saida>   -> <pasta_saida>/index.html (publicar como Artifact com files r1.mp4, r2.mp4, r1.jpg, r2.jpg)
"""
import html
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from legendas import LEGENDAS  # noqa: E402

DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
CORTES = {
    1: ["Saiu a abertura \u201choje chegou um atendimento\u201d e a opinião \u201cdanoso\u201d (caso de cliente e juízo de valor).",
        "Saiu \u201ce o FGTS\u201d do exemplo dos R$ 150: o FGTS não vem na diária, é depositado à parte (art. 452-A, §8º). A tela mostra isso.",
        "Saiu \u201cnada mais o trabalhador vai ter direito de receber\u201d e \u201cnão tem direito a férias\u201d: o descanso de 1 mês continua (§9º).",
        "Saíram um \u201cné\u201d e um começo repetido (\u201cele retira, não é que ele retira\u201d)."],
    2: ["Gancho: a frase \u201ctrabalhou durante anos, todos os dias… não tinha 13º\u201d abre o vídeo e volta no meio, de propósito.",
        "Saíram as hesitações depois de \u201cartigo 443\u201d, em \u201cdepois da… mudança\u201d e em \u201cse recusar a… ir trabalhar\u201d. A Reforma de 2017 foi para a tela.",
        "Saíram \u201co que que acontece\u201d, \u201co que que aconteceria\u201d e um \u201cné\u201d; as perguntas aparecem escritas na tela.",
        "Saiu a frase sobre \u201cameaça\u201d, que ficou invertida na gravação."],
    3: ["Abre com “hoje chegou um atendimento” (situação fictícia) e segue a ordem da gravação, como explicação.",
        "Saiu a opinião “danoso”, que contradiz o “não tira direitos” do meio do vídeo.",
        "Saiu “e o FGTS” do exemplo dos R$ 150 (o FGTS é depositado à parte, art. 452-A, §8º) e “nada mais vai receber”.",
        "Saíram um “né” e um começo repetido (“ele retira, não é que ele retira”)."],
    4: ["Contado em capítulos: o caso, as provas, a lei e o desfecho. Na tela: “Estudo de caso · situação hipotética”.",
        "Começa em “o trabalhador trabalhou em contrato intermitente”: o “E o que que acontece” do início saiu.",
        "A parte da lei (art. 443, juízes que validam, julgados que questionam) vem antes do desfecho, para o caso fechar na conclusão.",
        "Saíram as hesitações, um “né”, o “o que que aconteceria” e a frase sobre “ameaça”, que ficou invertida."],
}
# Versões B de 17/11/2026: a Dra. escolhe uma versão de cada vídeo (as versões A ficam guardadas)
GRUPOS = [("Vídeo 1 · O que é o contrato intermitente", [(3, "Versão B · explicação, abre com o atendimento"), (1, "Versão A · abre com o 13º")]),
          ("Vídeo 2 · Estudo de caso", [(4, "Versão B · estudo de caso em capítulos"), (2, "Versão A · intermitente de fachada")])]
DURACAO = {}


def quando(txt):
    d = datetime.fromisoformat(txt)
    return f"{DIAS[d.weekday()]}, {d.day:02d}/{d.month:02d} às {d.hour}h{d.minute:02d}"


def bloco(n, info, versao):
    leg, pc = html.escape(info["legenda"]), html.escape(info["pc"])
    cortes = "".join(f"<li>{html.escape(c)}</li>" for c in CORTES[n])
    titulo = html.escape(info["titulo"].replace("Reels da Dra.: ", ""))
    return f"""
<section class="reel" id="reel-{n}">
  <div class="tela">
    <video src="r{n}.mp4" poster="r{n}.jpg" controls playsinline preload="metadata"></video>
    <p class="nota">Prévia leve para assistir aqui. O arquivo final sai em alta qualidade.</p>
  </div>
  <div class="texto">
    <p class="rotulo">{html.escape(versao)} · {quando(info['quando'])}</p>
    <h2>{titulo}</h2>
    <h3>Legenda</h3>
    <div class="caixa"><pre id="leg-{n}">{leg}</pre><button type="button" data-copia="leg-{n}">Copiar legenda</button></div>
    <h3>Primeiro comentário</h3>
    <div class="caixa"><pre id="pc-{n}">{pc}</pre><button type="button" data-copia="pc-{n}">Copiar comentário</button></div>
    <h3>O que foi tirado da gravação</h3>
    <ul class="cortes">{cortes}</ul>
  </div>
</section>"""


def pagina():
    reels = "".join(f'<h2 class="grupo">{html.escape(g)}</h2>' + "".join(bloco(n, LEGENDAS[n], v) for n, v in itens)
                    for g, itens in GRUPOS)
    return f"""<title>Contrato intermitente: Reels da Dra.</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap">
<style>
/* Mesa de aprovação: papel claro do feed, café no texto, ouro só nos detalhes; vídeo à esquerda, textos à direita */
:root {{
  --papel: #F7F2EA; --cartao: #FFFCF7; --cafe: #2B231C; --cafe-suave: #6B5A4A; --ouro: #9A7A3C; --linha: #E4D9C8;
  --serif: "EB Garamond", Garamond, Georgia, serif; --sans: Inter, "Segoe UI", system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --papel: #1C1713; --cartao: #251F1A; --cafe: #F1E9DD; --cafe-suave: #BFAF9C; --ouro: #D4B26A; --linha: #3A3029; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --papel: #1C1713; --cartao: #251F1A; --cafe: #F1E9DD; --cafe-suave: #BFAF9C; --ouro: #D4B26A; --linha: #3A3029; color-scheme: dark }}
body {{ background: var(--papel); color: var(--cafe); font: 16px/1.6 var(--sans); }}
.pagina {{ max-width: 1080px; margin: 0 auto; padding-block: 40px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 48px; }}
header {{ display: grid; gap: 10px; border-bottom: 1px solid var(--linha); padding-bottom: 28px; }}
.rotulo {{ margin: 0; font-size: 12px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: var(--ouro); }}
h1 {{ margin: 0; font: 600 clamp(32px, 5vw, 48px)/1.1 var(--serif); text-wrap: balance; }}
h1 em {{ color: var(--ouro); }}
header p.intro {{ margin: 0; max-width: 62ch; color: var(--cafe-suave); }}
.passos {{ margin: 6px 0 0; padding-left: 20px; max-width: 62ch; }}
.reel {{ display: grid; grid-template-columns: minmax(0, 340px) minmax(0, 1fr); gap: 36px; align-items: start; }}
.tela {{ position: sticky; top: calc(16px + env(safe-area-inset-top, 0px)); display: grid; gap: 8px; }}
video {{ width: 100%; max-width: 100%; aspect-ratio: 9 / 16; background: #000; border-radius: 14px; box-shadow: 0 18px 40px rgba(43,35,28,.18); }}
.nota {{ margin: 0; font-size: 13px; color: var(--cafe-suave); }}
.texto {{ min-width: 0; display: grid; gap: 12px; }}
h2 {{ margin: 0 0 8px; font: 600 30px/1.15 var(--serif); text-wrap: balance; }}
h3 {{ margin: 14px 0 0; font-size: 13px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--cafe-suave); }}
.caixa {{ background: var(--cartao); border: 1px solid var(--linha); border-radius: 10px; padding: 18px 20px; display: grid; gap: 12px; }}
pre {{ margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 15px/1.6 var(--sans); }}
button {{ justify-self: start; font: 600 14px var(--sans); color: var(--cafe); background: transparent; border: 1px solid var(--ouro); border-radius: 999px; padding: 8px 16px; cursor: pointer; }}
button:hover {{ background: var(--ouro); color: var(--papel); }}
button:focus-visible {{ outline: 2px solid var(--ouro); outline-offset: 2px; }}
h2.grupo {{ margin: 0; padding-top: 8px; font-size: 36px; color: var(--ouro); border-top: 1px solid var(--linha); padding-top: 32px; }}
.cortes {{ margin: 0; padding-left: 20px; display: grid; gap: 6px; color: var(--cafe-suave); }}
footer {{ border-top: 1px solid var(--linha); padding-top: 20px; font-size: 13px; color: var(--cafe-suave); }}
@media (max-width: 760px) {{ .reel {{ grid-template-columns: minmax(0, 1fr); }} .tela {{ position: static; max-width: 360px; justify-self: center; }} }}
</style>
<main class="pagina">
  <header>
    <p class="rotulo">Para aprovação · Dra. Letícia Barros</p>
    <h1>Contrato intermitente: <em>escolha uma versão de cada vídeo</em></h1>
    <p class="intro">Os dois vídeos que a senhora gravou, cada um em duas versões editadas, com cenas, animações e efeitos sonoros. A sua voz e a sua imagem estão como foram gravadas: só tiramos pausas, repetições e frases que não fecharam.</p>
    <ol class="passos">
      <li>Assista com som.</li>
      <li>Confira a legenda e a base legal de cada um.</li>
      <li>Responda à Jessica qual versão fica em cada vídeo (por exemplo, “1B e 2A”) ou o ajuste que quiser.</li>
    </ol>
  </header>
  {reels}
  <footer>Série 23 · gravações IMG_2092 e IMG_2093 · versões A (16/11) e B (17/11) · base legal: CLT, arts. 9º, 443, §3º, e 452-A (Lei 13.467/2017).</footer>
</main>
<script>
document.querySelectorAll("[data-copia]").forEach(function (b) {{
  b.addEventListener("click", function () {{
    var alvo = document.getElementById(b.dataset.copia), texto = alvo.textContent, rotulo = b.textContent;
    function feito() {{ b.textContent = "Copiado"; setTimeout(function () {{ b.textContent = rotulo; }}, 1600); }}
    function seleciona() {{ var r = document.createRange(); r.selectNodeContents(alvo); var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = "Selecionado: use Ctrl+C"; }}
    try {{ navigator.clipboard.writeText(texto).then(feito, seleciona); }} catch (e) {{ seleciona(); }}
  }});
}});
</script>
"""


if __name__ == "__main__":
    saida = Path(sys.argv[1])
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "index.html").write_text(pagina(), encoding="utf-8")
    print("ok", saida / "index.html")
