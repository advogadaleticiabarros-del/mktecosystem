import re

with open(r"C:\tmp\fa_all.css", encoding="utf-8") as f:
    css = f.read()

icones_usados = [
    "fa-arrow-right", "fa-briefcase", "fa-building", "fa-cart-shopping", "fa-check",
    "fa-chevron-up", "fa-child-reaching", "fa-clock", "fa-envelope", "fa-facebook-f",
    "fa-file-contract", "fa-google", "fa-hand-holding-heart", "fa-handshake",
    "fa-helmet-safety", "fa-instagram", "fa-landmark", "fa-linkedin-in",
    "fa-location-dot", "fa-lock", "fa-paper-plane", "fa-people-roof",
    "fa-person-pregnant", "fa-scale-balanced", "fa-spinner", "fa-star", "fa-whatsapp",
]

font_faces = re.findall(r"@font-face\{[^}]+\}", css)

regras_base = []
for m in re.finditer(r"([^{}]+)\{([^{}]+)\}", css):
    seletor = m.group(1)
    seletores_individuais = [s.strip() for s in seletor.split(",")]
    if any(
        s in (
            ".fa", ".fas", ".far", ".fab", ".fa-solid", ".fa-brands", ".fa-regular",
            ".fa-classic", ".svg-inline--fa", ":host", ":root",
        )
        for s in seletores_individuais
    ):
        regras_base.append(m.group(0))

regras_icones = []
for m in re.finditer(r"([^{}]+)\{([^{}]+)\}", css):
    seletor, corpo = m.group(1), m.group(2)
    seletores_individuais = [s.strip() for s in seletor.split(",")]
    for icone in icones_usados:
        alvo = f".{icone}:before"
        if alvo in seletores_individuais:
            regras_icones.append(f"{alvo}{{{corpo}}}")
            break

resultado = "\n".join(font_faces) + "\n" + "\n".join(regras_base) + "\n" + "\n".join(regras_icones)

with open(r"C:\tmp\fa_subset.css", "w", encoding="utf-8") as f:
    f.write(resultado)

print(f"CSS original: {len(css)} bytes")
print(f"CSS filtrado: {len(resultado)} bytes")
print(f"Ícones encontrados: {len(regras_icones)} de {len(icones_usados)} esperados")
print(f"Regras base: {len(regras_base)}")
print(f"Font-faces: {len(font_faces)}")
