"""Conecta <label> aos seus <input>/<select>/<textarea> via for/id,
corrigindo o item de acessibilidade "elementos de formulário sem
etiquetas associadas" apontado pelo PageSpeed Insights. Puramente
estrutural — não muda nada visualmente.
"""
import re
from pathlib import Path

PASTA = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3")

# Mapeamento label -> (id a atribuir, padrão do campo seguinte)
CAMPOS = [
    ("Seu nome completo", "f-name", r'(<input name="name")'),
    ("WhatsApp", "f-phone", r'(<input name="phone")'),
    ("Conte o seu caso", "f-msg-label", r'(<textarea name="message" id="f-msg")'),
    ("Conte a sua situação", "f-msg-label", r'(<textarea name="message" id="f-msg")'),
    ("Conte sua situação", "f-msg-label", r'(<textarea name="message" id="f-msg")'),
]


def processar(caminho: Path) -> bool:
    conteudo = caminho.read_text(encoding="utf-8")
    original = conteudo

    conteudo = re.sub(
        r'<label>Seu nome completo \*</label>\s*\n(\s*)<input name="name"',
        r'<label for="f-name">Seu nome completo *</label>\n\1<input id="f-name" name="name"',
        conteudo,
    )
    conteudo = re.sub(
        r'<label>WhatsApp \*</label>\s*\n(\s*)<input name="phone"',
        r'<label for="f-phone">WhatsApp *</label>\n\1<input id="f-phone" name="phone"',
        conteudo,
    )
    # Selects com id já existente (f-qualif) — só falta o for no label anterior
    conteudo = re.sub(
        r'<label>([^<]+)</label>\s*\n(\s*)<select name="qualif" id="f-qualif">',
        r'<label for="f-qualif">\1</label>\n\2<select name="qualif" id="f-qualif">',
        conteudo,
    )
    # Textarea com id já existente (f-msg) — só falta o for no label anterior
    conteudo = re.sub(
        r'<label>([^<]+)</label>\s*\n(\s*)<textarea name="message" id="f-msg"',
        r'<label for="f-msg">\1</label>\n\2<textarea name="message" id="f-msg"',
        conteudo,
    )

    if conteudo != original:
        caminho.write_text(conteudo, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    for arquivo in sorted(PASTA.glob("*.html")):
        mudou = processar(arquivo)
        print(f"{arquivo.name}: {'corrigido' if mudou else 'sem mudança'}")
