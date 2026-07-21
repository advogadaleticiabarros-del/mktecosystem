import re
import unicodedata


def gerar_slug(titulo: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    minusculo = sem_acento.lower()
    apenas_alfanumerico = re.sub(r"[^a-z0-9]+", "-", minusculo)
    return apenas_alfanumerico.strip("-")
