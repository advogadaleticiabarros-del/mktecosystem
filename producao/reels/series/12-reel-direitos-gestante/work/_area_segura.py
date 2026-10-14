"""Aplica o layout de área segura (Meta: topo 14%, base 35%, laterais 65 px) no montador."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
novo = (AQUI / "_roteiros_seguros.txt").read_text(encoding="utf-8")
p = AQUI / "serie.py"
s = p.read_text(encoding="utf-8")
i = s.index("def outro(a, proxima):")
j = s.index("REELS = {")
s = s[:i] + novo + s[j:]
p.write_text(s, encoding="utf-8", newline="\n")

p = AQUI / "engine.html"
s = p.read_text(encoding="utf-8")
for a, b in [
    ("#cab { position:absolute; z-index:40; top:150px;", "#cab { position:absolute; z-index:40; top:284px;"),
    ("#barra { position:absolute; z-index:40; top:196px;", "#barra { position:absolute; z-index:40; top:326px;"),
    ("#leg { position:absolute; z-index:40; left:70px; right:150px; top:1330px; text-align:left; font-size:50px;",
     "#leg { position:absolute; z-index:40; left:90px; right:130px; top:1110px; text-align:center; font-size:52px;"),
    ("#leg .w { margin-right:12px; opacity:.55; }", "#leg .w { margin:0 6px; opacity:.55; }"),
]:
    assert s.count(a) == 1, a[:40]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
