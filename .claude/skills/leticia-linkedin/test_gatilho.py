import json
import subprocess
import sys
from pathlib import Path

import pytest

from gatilho import fala_de_linkedin

SCRIPT = Path(__file__).with_name("gatilho.py")


@pytest.mark.parametrize("texto", [
    "vamos revisar o LinkedIn", "deixe automatico quando formos falar de linkdin", "post no linkedln",
    "lnkedin da Dra.", "Linked In", "linkdim", "linkedin.com/company/leticia-barros-advocacia",
])
def test_reconhece_linkedin_e_erros_de_digitacao(texto):
    assert fala_de_linkedin(texto)


@pytest.mark.parametrize("texto", ["manda o link do artigo", "link dinâmico", "carrossel do Instagram", ""])
def test_ignora_outros_assuntos(texto):
    assert not fala_de_linkedin(texto)


def rodar(entrada: bytes) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT)], input=entrada, capture_output=True)


def test_gancho_injeta_o_lembrete_da_skill_quando_o_assunto_e_linkedin():
    saida = rodar(json.dumps({"prompt": "revise o linkdin"}, ensure_ascii=False).encode("utf-8"))
    dados = json.loads(saida.stdout)["hookSpecificOutput"]
    assert saida.returncode == 0 and dados["hookEventName"] == "UserPromptSubmit"
    assert "leticia-linkedin" in dados["additionalContext"]


def test_gancho_fica_em_silencio_em_outro_assunto_ou_entrada_invalida():
    for entrada in (json.dumps({"prompt": "edite o reels"}).encode(), b"nao e json"):
        saida = rodar(entrada)
        assert saida.returncode == 0 and saida.stdout == b""
