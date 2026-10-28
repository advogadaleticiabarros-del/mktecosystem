"""Botão em destaque no topo da home (que também é o link da bio) apontando para a LP da demissão pelo voto (28/10/2026).

`aplicar(html)` devolve a home com o botão; `remover(html)` tira o botão e o CSS (para quando a campanha acabar).
Rodar no container: `python home_alerta.py publicar` (backup em /tmp/bkp_home_v1.html) ou `python home_alerta.py remover`.
"""
import asyncio
import sys

INICIO, FIM = "<!-- alerta-campanha-voto:inicio -->", "<!-- alerta-campanha-voto:fim -->"
LINK = "/lp/demissao-por-voto.html?utm_source=site&utm_medium=home-hero&utm_campaign=assedio-eleitoral-2026"

CSS = f"""{INICIO}<style>
.hero-alerta{{display:flex;align-items:center;gap:14px;max-width:480px;margin:0 0 22px;padding:16px 18px;
  background:var(--gradient-gold);color:var(--fundo-escuro);border-radius:10px;text-decoration:none;
  box-shadow:0 6px 28px rgba(201,169,98,.35);animation:alerta-pulso 2.4s ease-in-out infinite;transition:var(--transition)}}
.hero-alerta:hover{{transform:translateY(-2px);box-shadow:0 10px 34px rgba(201,169,98,.5)}}
.hero-alerta .ha-icone{{flex:0 0 40px;height:40px;border-radius:50%;background:rgba(35,30,26,.14);display:flex;
  align-items:center;justify-content:center;font-size:1.25rem}}
.hero-alerta .ha-txt{{font-size:.9rem;line-height:1.35;text-align:left}}
.hero-alerta .ha-txt strong{{display:block;font-size:1rem;font-weight:700}}
.hero-alerta .ha-seta{{margin-left:auto;font-size:1rem}}
.hero-alerta.ha-mob{{display:none}}
@keyframes alerta-pulso{{0%,100%{{box-shadow:0 6px 28px rgba(201,169,98,.3)}}50%{{box-shadow:0 6px 38px rgba(201,169,98,.6)}}}}
@media (max-width:1024px){{.hero-alerta.ha-desk{{display:none}}.hero-alerta.ha-mob{{display:flex;order:-2;margin:0 auto;width:100%}}}}
@media (prefers-reduced-motion:reduce){{.hero-alerta{{animation:none}}}}
</style>{FIM}
"""

BOTAO = f"""{INICIO}<a href="{LINK}" class="hero-alerta CLASSE">
                <span class="ha-icone">🗳️</span>
                <span class="ha-txt"><strong>Demitido ou ameaçado por causa do voto?</strong>Veja seus direitos e como denunciar</span>
                <span class="ha-seta"><i class="fa-solid fa-arrow-right"></i></span>
            </a>{FIM}"""

ANCORA_BOTOES = '<div class="hero-buttons">'
ANCORA_HERO = '<section class="hero" id="hero">'
ANCORA_GRADE = '<div class="container">'


def aplicar(html: str) -> str:
    if INICIO in html:
        return html
    assert html.count(ANCORA_BOTOES) == 1, "a home mudou: não achei os botões do topo"
    assert html.count(ANCORA_HERO) == 1, "a home mudou: não achei o topo"
    assert html.count("</head>") == 1
    html = html.replace("</head>", CSS + "</head>")
    # Computador: acima do WhatsApp. Celular: primeiro item do topo, antes da foto (quem vem da bio está no celular).
    html = html.replace(ANCORA_BOTOES, BOTAO.replace("CLASSE", "ha-desk") + "\n            " + ANCORA_BOTOES)
    grade = html.index(ANCORA_GRADE, html.index(ANCORA_HERO)) + len(ANCORA_GRADE)
    return html[:grade] + "\n        " + BOTAO.replace("CLASSE", "ha-mob") + html[grade:]


def remover(html: str) -> str:
    while INICIO in html:
        a = html.index(INICIO)
        b = html.index(FIM, a) + len(FIM)
        fim_recuo = b + 1 if html[b:b + 1] == "\n" else b
        while html[fim_recuo:fim_recuo + 1] == " ":
            fim_recuo += 1
        if html[fim_recuo:].startswith(ANCORA_BOTOES):  # botão do computador: entrou com quebra e recuo
            b = fim_recuo
        elif html[a - 1:a] == "\n":        # CSS: entrou logo antes do </head>, com uma quebra no fim
            b += 1 if html[b:b + 1] == "\n" else 0
        else:                              # botão do celular: entrou depois de "\n        "
            while html[a - 1:a] == " ":
                a -= 1
            a -= 1 if html[a - 1:a] == "\n" else 0
        html = html[:a] + html[b:]
    return html


async def main(acao: str) -> None:
    from app.services.central_google import _site_padrao
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    atual = await s.ler("index.html")
    open("/tmp/bkp_home_v1.html", "w", encoding="utf-8", newline="").write(atual)
    novo = aplicar(atual) if acao == "publicar" else remover(atual)
    if novo == atual:
        print("nada a mudar")
    else:
        await sftp.upload(f"{raiz}/index.html", novo.encode("utf-8"))
        print(acao, "feito; backup em /tmp/bkp_home_v1.html")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "publicar"))
