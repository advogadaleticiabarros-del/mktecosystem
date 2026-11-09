"""Grava a navegação real (bio -> calculadora -> resultado) como sequência de quadros nítidos.

Rede externa bloqueada; o envio ao CRM é respondido aqui mesmo (nenhum lead é criado).
Precisa do repositório servido em http://127.0.0.1:8766 (python -m http.server 8766 --directory <repo>).
Saída: rec/tela.mp4 (1170x2532, 30 fps) e rec/roteiro.json (toques e marcos, em segundos).
"""
import json, pathlib, shutil, subprocess
from playwright.sync_api import sync_playwright

AQUI = pathlib.Path(__file__).parent
REC = AQUI / "rec"; QD = REC / "q"
BASE = "http://127.0.0.1:8766"
shutil.rmtree(REC, ignore_errors=True); QD.mkdir(parents=True)

quadros, toques, marcos = [], [], []
t = 0.0


def rota(route):
    u = route.request.url
    if u.startswith(BASE) or "fonts.g" in u:
        return route.continue_()
    if "api/public/lead" in u:
        return route.fulfill(status=200, content_type="application/json", body='{"ok":true}',
                             headers={"Access-Control-Allow-Origin": "*"})
    return route.abort()


with sync_playwright() as p:
    nav = p.chromium.launch()
    pg = nav.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
    pg.route("**/*", rota)

    def foto(dur):
        global t
        n = QD / f"{len(quadros):05d}.png"
        pg.screenshot(path=str(n))
        quadros.append((n.name, dur)); t += dur

    def marco(nome):
        marcos.append({"t": round(t, 3), "nome": nome})

    def centro(sel):
        b = pg.locator(sel).first.bounding_box()
        return b["x"] + b["width"] / 2, b["y"] + b["height"] / 2

    def tocar(sel, depois=0.35):
        x, y = centro(sel)
        foto(0.45)  # o dedo chega
        toques.append({"t": round(t, 3), "x": x, "y": y})
        pg.locator(sel).first.click()
        pg.wait_for_timeout(250)
        foto(depois)

    def rolar_ate(sel, alvo_y=0.42, passos=24, dur=0.045):
        y0 = pg.evaluate("scrollY")
        b = pg.locator(sel).first.bounding_box()
        destino = max(0, y0 + b["y"] - 844 * alvo_y)
        for i in range(1, passos + 1):
            k = i / passos; k = k * k * (3 - 2 * k)
            pg.evaluate(f"scrollTo(0,{y0 + (destino - y0) * k})")
            foto(dur)

    def digitar(sel, texto, dur=0.11):
        tocar(sel, 0.2)
        for ch in texto:
            pg.keyboard.type(ch)
            foto(dur)
        foto(0.35)

    # 1) página da bio
    pg.goto(f"{BASE}/lp/bio/index.html"); pg.add_style_tag(content=".faixa{animation:none!important}"); pg.wait_for_timeout(1200)
    marco("bio"); foto(1.6)
    rolar_ate("[data-link=calculadora-13]", 0.5, passos=40, dur=0.05)
    foto(0.7)
    tocar("[data-link=calculadora-13]", 0.1)

    # 2) calculadora
    pg.goto(f"{BASE}/lp/calculadora-13-salario.html"); pg.wait_for_timeout(1200)
    marco("calc_topo"); foto(1.8)
    rolar_ate("#c-salario", 0.45, passos=30)
    marco("salario"); foto(0.5)
    digitar("#c-salario", "4.500,00")
    marco("situacao"); foto(0.4)
    tocar("#c-situacao", 0.2)  # mostra o campo; mantém "Estou trabalhando"
    pg.keyboard.press("Escape"); foto(0.9)
    rolar_ate("#c-comissoes", 0.4, passos=16)
    marco("comissoes")
    digitar("#c-comissoes", "800,00")
    marco("extras")
    digitar("#c-extras", "300,00")
    rolar_ate("#bt-mais", 0.45, passos=14)
    marco("mais")
    tocar("#bt-mais", 0.5)
    rolar_ate("#c-dep", 0.45, passos=16)
    marco("dependentes")
    tocar("#c-dep", 0.2)
    pg.keyboard.press("Control+A"); pg.keyboard.type("1"); foto(0.9)
    rolar_ate("#etapa1 button.enviar", 0.55, passos=14)
    marco("calcular")
    tocar("#etapa1 button.enviar", 0.3)

    # 3) contato
    rolar_ate("#l-nome", 0.35, passos=14)
    marco("contato")
    digitar("#l-nome", "Maria Souza", 0.07)
    digitar("#l-tel", "27999990000", 0.07)
    digitar("#l-email", "maria@email.com", 0.06)
    tocar("input[name=ciente]", 0.4)
    rolar_ate("#etapa2 button.enviar", 0.55, passos=10)
    tocar("#etapa2 button.enviar", 0.2)
    pg.wait_for_timeout(700)

    # 4) resultado
    rolar_ate(".recibo", 0.22, passos=20)
    marco("resultado"); foto(1.2)
    rolar_ate(".recibo .total", 0.55, passos=24, dur=0.05)
    marco("total"); foto(3.0)
    recibo = pg.inner_text(".recibo")
    nav.close()

lista = REC / "lista.txt"
with open(lista, "w", encoding="utf-8") as f:
    for nome, dur in quadros:
        f.write(f"file 'q/{nome}'\nduration {dur:.3f}\n")
    f.write(f"file 'q/{quadros[-1][0]}'\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", str(lista), "-vf", "fps=30,format=yuv420p",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", str(REC / "tela.mp4")], check=True, cwd=REC)
json.dump({"duracao": round(t, 3), "toques": toques, "marcos": marcos, "recibo": recibo},
          open(REC / "roteiro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("duração", round(t, 2), "s,", len(quadros), "quadros")
