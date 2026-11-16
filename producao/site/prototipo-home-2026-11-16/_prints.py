import sys, pathlib
from playwright.sync_api import sync_playwright
d=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for tema in ["clara","escura"]:
        for disp,vp in [("cel",(390,844)),("pc",(1366,800))]:
            pg=b.new_page(viewport={"width":vp[0],"height":vp[1]})
            pg.goto((d/f"home-{tema}.html").as_uri(),wait_until="networkidle",timeout=60000)
            pg.add_style_tag(content=".js .surge{opacity:1!important;transform:none!important}.faixa{animation:none!important}")
            pg.wait_for_timeout(800)
            pg.screenshot(path=str(out/f"{tema}-{disp}.png"))
            pg.screenshot(path=str(out/f"{tema}-{disp}-inteira.png"),full_page=True)
            pg.close()
    b.close()
