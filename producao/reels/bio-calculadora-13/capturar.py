"""Captura telas reais (bio e calculadora) para o Reels. Rede bloqueada; o envio ao CRM é respondido localmente (nenhum lead criado)."""
import pathlib, json
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).parent / "assets"
def rota(route):
    u = route.request.url
    if u.startswith("http://127.0.0.1:8766") or "fonts.g" in u: return route.continue_()
    if "api/public/lead" in u: return route.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True}), headers={"Access-Control-Allow-Origin": "*"})
    return route.abort()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
    pg.route("**/*", rota)
    pg.goto("http://127.0.0.1:8766/lp/bio/index.html"); pg.wait_for_timeout(1500)
    pg.add_style_tag(content=".faixa{animation:none!important}")
    pg.screenshot(path=str(OUT / "bio-full.png"), full_page=True)
    y = pg.evaluate("document.querySelector('[data-link=calculadora-13]').getBoundingClientRect().top + scrollY")
    open(OUT / "bio-calc-y.txt", "w").write(str(y))
    pg.goto("http://127.0.0.1:8766/lp/calculadora-13-salario.html"); pg.wait_for_timeout(1500)
    pg.screenshot(path=str(OUT / "calc-topo.png"))
    pg.evaluate("document.getElementById('c-salario').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT / "calc-form-vazio.png"))
    pg.fill("#c-salario", "3.000,00"); pg.wait_for_timeout(200)
    pg.screenshot(path=str(OUT / "calc-form-cheio.png"))
    pg.click("#etapa1 button.enviar"); pg.wait_for_timeout(500)
    pg.evaluate("document.getElementById('l-nome').scrollIntoView({block:'center'})")
    pg.fill("#l-nome", "Maria Souza"); pg.fill("#l-tel", "(27) 99999-0000"); pg.fill("#l-email", "maria@email.com")
    pg.check("input[name=ciente]"); pg.wait_for_timeout(200)
    pg.screenshot(path=str(OUT / "calc-contato.png"))
    pg.click("#etapa2 button.enviar"); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('.recibo').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT / "calc-resultado.png"))
    print(pg.inner_text(".recibo"))
    b.close()
