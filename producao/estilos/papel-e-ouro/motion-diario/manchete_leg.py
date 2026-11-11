"""Legenda dos Flagrantes 23-33, tirada de producao/estilos/manchete/legendas.md (mesmo tema do estático Manchete).
Troca o fechamento 'Salve este post...' pelo do Flagrante (o motor insere o convite para seguir) e põe a base legal
do primeiro comentário dentro da legenda, como pede docs/ESTILO_FLAGRANTE.md."""
import re
from pathlib import Path

ARQ = Path(__file__).resolve().parents[2] / "manchete" / "legendas.md"


def legenda(peca, gancho=""):
    sec = ARQ.read_text(encoding="utf-8").split(f"## {peca}\n", 1)[1].split("\n## ", 1)[0]
    leg = sec.split("**Legenda:**", 1)[1].split("**Primeiro comentário:**", 1)[0].strip()
    com = sec.split("**Primeiro comentário:**", 1)[1].strip()
    base = next((l for l in com.splitlines() if l.startswith("📚")), "")
    resto = "\n".join(l for l in com.splitlines() if not l.startswith("📚")).strip()
    leg = re.sub(r"Cada caso tem detalhes e precisa ser avaliado\..*?confiança\.",
                 (base + "\n\n" if base else "") + "Cada caso tem detalhes. Procure uma advogada de confiança.", leg, flags=re.S)
    return {"primeiro_comentario": resto, "legenda": (gancho + "\n\n" if gancho else "") + leg}
