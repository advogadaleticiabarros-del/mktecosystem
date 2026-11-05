"""Gancho UserPromptSubmit: quando a mensagem fala de LinkedIn, manda o Claude abrir a skill `leticia-linkedin`.

Interface: `fala_de_linkedin(texto)`. Como script, lê o JSON do gancho na entrada e só escreve se o assunto for
LinkedIn. Nunca atrapalha a mensagem: entrada inválida termina em silêncio.
"""
import json
import re
import sys

_LINKEDIN = re.compile(r"\bl[iy]?nk+e?d+[\s-]?[il1][nm]", re.IGNORECASE)
LEMBRETE = ("A mensagem fala de LinkedIn. Antes de responder ou agir, carregue a skill leticia-linkedin com a "
            "ferramenta Skill e siga o caminho que couber.")


def fala_de_linkedin(texto: str) -> bool:
    return bool(_LINKEDIN.search(texto))


def main() -> None:
    try:
        prompt = json.loads(sys.stdin.buffer.read().decode("utf-8")).get("prompt", "")
    except ValueError:
        return
    if fala_de_linkedin(prompt):
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": LEMBRETE}}))


if __name__ == "__main__":
    main()
