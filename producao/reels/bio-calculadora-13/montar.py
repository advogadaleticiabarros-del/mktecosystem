"""Gera video/index.html (Reels detalhado da calculadora) a partir de rec/roteiro.json e feed/perfil.json."""
import json, pathlib
AQUI = pathlib.Path(__file__).parent
rot = json.load(open(AQUI / "rec/roteiro.json", encoding="utf-8"))
perfil = json.load(open(AQUI / "feed/perfil.json", encoding="utf-8"))["perfil"]

INTRO = 6.0                      # abertura no perfil
TELA = rot["duracao"]            # gravação real
FIM = 5.0                        # CTA
TOTAL = round(INTRO + TELA + FIM, 2)
S = 620 / 390                    # css px -> px da tela do celular
TX, TY = 230, 394                # canto da tela no quadro

TITULOS = {
    "bio": ("Passo 1", "Na página da bio, desça até <em>Ferramentas gratuitas</em>"),
    "calc_topo": ("Passo 2", "Abra a <em>Calculadora do 13º</em>"),
    "salario": ("Passo 3", "Digite o <em>salário bruto</em> do holerite"),
    "situacao": ("Passo 4", "Escolha a sua <em>situação</em> no emprego"),
    "comissoes": ("Passo 5", "Recebe <em>comissão</em>? Coloque a média do mês"),
    "extras": ("Passo 6", "<em>Horas extras</em> e noturno também entram"),
    "mais": ("Passo 7", "Abra as <em>informações extras</em>"),
    "dependentes": ("Passo 8", "Tem filhos? Informe os <em>dependentes</em> do IR"),
    "calcular": ("Passo 9", "Toque em <em>Calcular meu 13º</em>"),
    "contato": ("Passo 10", "Nome, WhatsApp e e-mail para <em>ver o resultado</em>"),
    "resultado": ("Resultado", "Cada parcela, já com <em>INSS e Imposto de Renda</em>"),
    "total": ("No exemplo", "Salário de R$ 4.500 + comissão e extras: <em>R$ 4.829,38</em>"),
}

marcos = rot["marcos"]
titulos_html, titulos_js = [], []
abertura = ("Calculadora do 13º", "Onde fica? <em>No link da bio.</em>")
lista = [(0.0, INTRO, abertura)]
for i, m in enumerate(marcos):
    ini = INTRO + m["t"]
    fim = INTRO + marcos[i + 1]["t"] if i + 1 < len(marcos) else INTRO + TELA
    lista.append((ini, fim - ini, TITULOS[m["nome"]]))
for i, (ini, dur, (olho, txt)) in enumerate(lista):
    titulos_html.append(f'<h1 id="t{i}" class="titulo clip" data-start="{ini:.2f}" data-duration="{dur:.2f}" data-track-index="1">'
                        f'<span class="passo">{olho}</span>{txt}</h1>')
    if i:
        titulos_js.append(f'tl.fromTo("#t{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:E}},{ini + .02:.2f});')

toques = [(4.6, 430, 815)] + [(INTRO + q["t"], TX + q["x"] * S, TY + q["y"] * S) for q in rot["toques"]]
toques_js = "\n".join(f"tocar({t:.2f},{x:.0f},{y:.0f});" for t, x, y in toques)
sons = "\n      ".join(
    f'<audio id="som{i}" class="clip" src="assets/toque.wav" data-start="{t:.2f}" data-duration="0.2" data-track-index="5" data-volume="0.8"></audio>'
    for i, (t, x, y) in enumerate(toques))
t_total = INTRO + next(m["t"] for m in marcos if m["nome"] == "total")

posts = "".join(f'<div class="post"><img src="assets/feed/post{i:02d}.jpg" alt=""></div>' for i in range(12))
bio_txt = perfil["biography"].replace("\n", "<br>")

html = f"""<!doctype html>
<html lang="pt-BR"
  data-composition-variables='[{{"id":"cta","type":"string","label":"CTA","default":"Clique no link da bio e faça o seu cálculo"}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --cafe:#231E1A; --papel:#EFE6D9; --ouro:#B8935A; --ouro-claro:#D4B483; --serif:"EB Garamond",serif; --sans:"Inter",sans-serif; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--cafe); }}
      #root {{ position:relative; width:100%; height:100%; font-family:var(--sans); color:var(--papel); overflow:hidden; }}
      #fundo {{ position:absolute; inset:0; background:radial-gradient(ellipse 80% 50% at 50% 40%, #3A2F27 0%, var(--cafe) 70%); }}
      .titulo {{ position:absolute; left:80px; right:80px; top:176px; text-align:center; font-family:var(--serif); font-weight:400; font-size:58px; line-height:1.06; color:var(--papel); text-wrap:balance; }}
      .titulo em {{ font-style:normal; color:var(--ouro-claro); }}
      .passo {{ display:block; font-family:var(--sans); font-size:26px; letter-spacing:.2em; text-transform:uppercase; color:var(--ouro); margin-bottom:12px; }}
      #celular {{ position:absolute; left:216px; top:380px; width:648px; height:1370px; border-radius:64px; background:#0E0B09; border:2px solid rgba(212,180,131,.45); box-shadow:0 40px 90px rgba(0,0,0,.55); }}
      #tela {{ position:absolute; left:230px; top:394px; width:620px; height:1342px; border-radius:52px; overflow:hidden; background:#fff; }}
      #gravacao {{ position:absolute; left:0; top:0; width:620px; height:1342px; }}
      /* perfil real (dados da conta), desenhado sem a marca do app */
      #perfil {{ position:absolute; inset:0; background:#fff; color:#111; font-family:var(--sans); }}
      #perfil-rola {{ position:absolute; left:0; right:0; top:0; }}
      .p-top {{ height:118px; display:flex; align-items:flex-end; padding:0 26px 16px; font-weight:700; font-size:27px; }}
      .p-head {{ display:flex; align-items:center; gap:22px; padding:6px 26px 0; }}
      .p-head img {{ width:150px; height:150px; border-radius:50%; object-fit:cover; flex:none; }}
      .p-num {{ flex:1; display:flex; justify-content:space-around; text-align:center; }}
      .p-num b {{ display:block; font-size:27px; }} .p-num span {{ font-size:20px; color:#333; }}
      .p-nome {{ padding:16px 26px 0; font-weight:700; font-size:21px; line-height:1.3; }}
      .p-bio {{ padding:4px 26px 0; font-size:21px; line-height:1.35; }}
      #p-link {{ display:inline-block; margin:6px 0 0 20px; padding:2px 6px; border-radius:8px; color:#00376B; font-weight:600; font-size:21px; }}
      .p-btns {{ display:flex; gap:8px; padding:18px 26px; }}
      .p-btns div {{ flex:1; background:#EFEFEF; border-radius:10px; text-align:center; padding:12px 0; font-weight:600; font-size:20px; }}
      .p-btns div:first-child {{ background:#0095F6; color:#fff; }}
      .p-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:3px; border-top:1px solid #eee; padding-top:3px; }}
      .post {{ aspect-ratio:3/4; overflow:hidden; background:#ddd; }}
      .post img {{ width:100%; height:100%; object-fit:cover; display:block; }}
      .toque {{ position:absolute; left:0; top:0; width:84px; height:84px; margin:-42px 0 0 -42px; border-radius:50%; background:rgba(255,255,255,.5); border:4px solid #fff; box-shadow:0 6px 20px rgba(0,0,0,.35); opacity:0; z-index:20; }}
      .onda {{ position:absolute; left:0; top:0; width:84px; height:84px; margin:-42px 0 0 -42px; border-radius:50%; border:4px solid var(--ouro-claro); opacity:0; z-index:19; }}
      #final {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:0 100px 260px; background:var(--cafe); }}
      #final .linha {{ width:120px; height:2px; background:var(--ouro); margin:34px 0; }}
      #cta {{ font-family:var(--serif); font-size:96px; line-height:1.02; color:var(--papel); }}
      #cta-sub {{ font-size:34px; color:var(--ouro-claro); letter-spacing:.04em; }}
      #arroba {{ font-size:32px; color:var(--papel); }}
      #oab {{ font-size:24px; color:rgba(239,230,217,.6); margin-top:14px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="fundo"></div>
      {chr(10).join('      ' + h for h in titulos_html).strip()}

      <div id="celular"></div>
      <div id="tela">
        <video id="gravacao" class="clip" src="assets/tela.mp4" muted playsinline data-start="{INTRO}" data-duration="{TELA}" data-track-index="2"></video>
        <div id="perfil" class="clip" data-start="0" data-duration="{INTRO}" data-track-index="3">
          <div id="perfil-rola">
            <div class="p-top">{perfil["username"]}</div>
            <div class="p-head"><img src="assets/feed/avatar.jpg" alt="" />
              <div class="p-num"><div><b>{perfil["media_count"]}</b><span>posts</span></div><div><b>{perfil["followers_count"]}</b><span>seguidores</span></div><div><b>{perfil["follows_count"]}</b><span>seguindo</span></div></div></div>
            <div class="p-nome">{perfil["name"]}</div>
            <div class="p-bio">{bio_txt}</div>
            <span id="p-link">advogadaleticiabarros.com.br/bio</span>
            <div class="p-btns"><div>Seguir</div><div>Mensagem</div></div>
            <div class="p-grid">{posts}</div>
          </div>
        </div>
      </div>

      <div id="toque" class="toque clip" data-start="0" data-duration="{INTRO + TELA}" data-track-index="4"></div>
      <div id="onda" class="onda clip" data-start="0" data-duration="{INTRO + TELA}" data-track-index="4"></div>

      {sons}
      <audio id="som-total" class="clip" src="assets/resultado.wav" data-start="{t_total:.2f}" data-duration="1.2" data-track-index="6" data-volume="0.6"></audio>

      <div id="final" class="clip" data-start="{INTRO + TELA}" data-duration="{FIM}" data-track-index="7">
        <div id="cta-sub">Calcule o seu 13º de 2026</div>
        <div class="linha"></div>
        <div id="cta" data-var-text="cta">Clique no link da bio e faça o seu cálculo</div>
        <div class="linha"></div>
        <div id="arroba">@{perfil["username"]}</div>
        <div id="oab">Dra. Letícia Barros · OAB/ES 39.948</div>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const E = "power3.out";
      {chr(10).join('      ' + j for j in titulos_js).strip()}
      // abertura: o feed desce um pouco, volta, e o link acende
      tl.fromTo("#perfil-rola", {{ y: 0 }}, {{ y: -420, duration: 1.5, ease: "power2.inOut" }}, 0.6);
      tl.to("#perfil-rola", {{ y: 0, duration: 1.2, ease: "power2.inOut" }}, 2.3);
      tl.fromTo("#p-link", {{ backgroundColor: "rgba(212,180,131,0)" }}, {{ backgroundColor: "rgba(212,180,131,.5)", duration: .35, yoyo: true, repeat: 1 }}, 3.5);
      function tocar(t, x, y) {{
        tl.set("#toque", {{ x: x, y: y }}, t - .4);
        tl.fromTo("#toque", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: .25, ease: E }}, t - .4);
        tl.to("#toque", {{ scale: .8, duration: .1 }}, t);
        tl.to("#toque", {{ scale: 1, opacity: 0, duration: .25 }}, t + .12);
        tl.set("#onda", {{ x: x, y: y }}, t);
        tl.fromTo("#onda", {{ opacity: .9, scale: .6 }}, {{ opacity: 0, scale: 2.3, duration: .5, ease: "power2.out" }}, t);
      }}
      {toques_js.replace(chr(10), chr(10) + '      ')}
      tl.fromTo("#final", {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, {INTRO + TELA});
      tl.fromTo("#cta", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .6, ease: E }}, {INTRO + TELA + .3:.2f});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(AQUI / "video/index.html").write_text(html, encoding="utf-8")
print("total", TOTAL, "s; toques", len(toques))
