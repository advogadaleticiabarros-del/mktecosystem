import json, sys, io, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
d = json.load(open("pexels.json", encoding="utf-8"))
T = Path("/c/tmp/assedio-carrossel/thumbs".replace("/c/", "C:/"))
UA = {"User-Agent": "Mozilla/5.0 (Orbit)"}
fonte = ImageFont.truetype("arial.ttf", 22)
for qi, (q, fotos) in enumerate(d.items()):
    tiles = []
    for p in fotos:
        f = T / f"{p['id']}.jpg"
        if not f.exists():
            f.write_bytes(urllib.request.urlopen(urllib.request.Request(p["med"], headers=UA), timeout=30).read())
        im = Image.open(f).convert("RGB"); im.thumbnail((240, 360))
        c = Image.new("RGB", (250, 395), "white"); c.paste(im, (5, 5))
        ImageDraw.Draw(c).text((8, 365), str(p["id"]), fill="black", font=fonte)
        tiles.append(c)
    folha = Image.new("RGB", (250 * 8, 395 * 2), "white")
    for i, t in enumerate(tiles[:16]):
        folha.paste(t, ((i % 8) * 250, (i // 8) * 395))
    folha.save(T.parent / f"folha-{qi}.jpg", quality=80)
    print(qi, q)
