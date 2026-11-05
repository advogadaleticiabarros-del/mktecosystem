"""Conferência automática de post do LinkedIn da Dra. Letícia.

Interface:
- `conferir(texto, oab=...)` devolve a lista `{"trecho", "motivo", "nivel"}`, no mesmo formato do verificador da OAB
  do Orbit. `nivel` "bloqueia" impede aprovar; "atencao" pede leitura humana.
- Linha de comando: `python conferir_post.py ARQUIVO [--de AAAA-MM-DD] [--ate AAAA-MM-DD]`. ARQUIVO é um .txt com um
  post ou um .json de fila (`data`, `tema`, `link`, `texto`). Devolve 1 se algo bloqueia.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[3]
LIMITE_API = 3000
FAIXA = (600, 1300)
GANCHO = 140  # aproximado: até onde a primeira linha aparece antes do "ver mais" no celular
HASHTAGS = 3

_REGRAS = [
    (r"\bdefici[êe]nci\w*|\bdeficientes?\b", 'Palavra proibida: usar "necessidades especiais".', "bloqueia"),
    (r"\bex-(marido|mulher|esposa|esposo|companheir[oa])\b|\b(meu|minha|seu|sua|o|a) ex\b(?!-)",
     'Palavra proibida: usar "genitor" ou "genitora".', "bloqueia"),
    (r"[—–]", "Travessão: trocar por ponto, vírgula ou quebra de linha.", "bloqueia"),
    (r"\bme chama\b|\bfale comigo\b|\bme (mande|envie)\b|\benvie seu caso\b|\banaliso (o )?seu caso\b"
     r"|\bsem compromisso\b|\bcontrate\b|\bentre com (uma )?a[çc][ãa]o\b",
     "Oferta direta ou indução a litigar (OAB).", "bloqueia"),
    (r"\b(deste mês|este mês|esta semana|nesta semana|semana passada|hoje|ontem|amanhã|neste ano|este ano|em (uma|duas|três) semanas|faltam)\b",
     "Data relativa: confira com a data de publicação do post.", "atencao"),
    (r"\bmais vejo\b|\bvejo no dia a dia\b|\bchegam? toda semana\b|\bno meu escritório\b|\batendi\b"
     r"|\bum cliente\b|\buma cliente\b|\bna minha experiência\b",
     "Experiência afirmada: precisa de confirmação da Dra. e não pode expor caso.", "atencao"),
    (r"\ba verdade é\b|\ba realidade é\b|\bo segredo\b|\ba melhor parte\b|\bnos dias de hoje\b|\bno mundo atual\b"
     r"|\bcada vez mais\b|\bvale lembrar\b|\bé importante ressaltar\b|\bdeixa eu\b|\be se eu te dissesse\b",
     "Fórmula genérica de texto de IA.", "atencao"),
    (r"\bnão é [^.!?\n]{1,60}[.,] (é|mas)\b|, não para\b",
     "Fórmula de reversão: mantenha só se o contraste ensinar a regra.", "atencao"),
    (r"\*\*[^*]+\*\*", "O LinkedIn não tem negrito: os asteriscos sairiam no post.", "atencao"),
]


def _oab_do_orbit(texto: str) -> list[dict]:
    """Usa as regras do publicador (a mesma checagem que barra o post em produção)."""
    caminho = _RAIZ / "apps/api/app/services/conformidade_oab.py"
    spec = importlib.util.spec_from_file_location("conformidade_oab", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo.verificar_texto_oab(texto)


def _medidas(texto: str) -> list[dict]:
    avisos = []
    tamanho = len(texto)
    if tamanho > LIMITE_API:
        avisos.append({"trecho": f"{tamanho} caracteres", "motivo": "Acima de 3.000: a API recusa.", "nivel": "bloqueia"})
    elif not FAIXA[0] <= tamanho <= FAIXA[1]:
        avisos.append({"trecho": f"{tamanho} caracteres", "motivo": "Fora da faixa de 600 a 1.300 caracteres.",
                       "nivel": "atencao"})
    primeira = texto.split("\n", 1)[0]
    if len(primeira) > GANCHO:
        avisos.append({"trecho": primeira[:40] + "...",
                       "motivo": f'Gancho com {len(primeira)} caracteres: pode cortar antes do "ver mais".',
                       "nivel": "atencao"})
    hashtags = re.findall(r"(?<!\w)#\w+", texto)
    if len(hashtags) > HASHTAGS:
        avisos.append({"trecho": " ".join(hashtags), "motivo": f"{len(hashtags)} hashtags: o máximo aqui é 3.",
                       "nivel": "atencao"})
    return avisos


def conferir(texto: str, oab=_oab_do_orbit) -> list[dict]:
    avisos = list(oab(texto)) + _medidas(texto)
    for padrao, motivo, nivel in _REGRAS:
        for achado in re.finditer(padrao, texto, re.IGNORECASE):
            avisos.append({"trecho": achado.group(0), "motivo": motivo, "nivel": nivel})
    return avisos


def _ler_posts(caminho: Path, de: str | None, ate: str | None) -> list[dict]:
    conteudo = caminho.read_text(encoding="utf-8")
    if caminho.suffix.lower() != ".json":
        return [{"data": "", "tema": caminho.name, "texto": conteudo.strip()}]
    return [p for p in json.loads(conteudo)
            if (not de or p["data"] >= de) and (not ate or p["data"] <= ate)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Confere posts do LinkedIn da Dra. Letícia.")
    parser.add_argument("arquivo", type=Path)
    parser.add_argument("--de")
    parser.add_argument("--ate")
    args = parser.parse_args(argv)
    bloqueou = False
    for post in _ler_posts(args.arquivo, args.de, args.ate):
        avisos = conferir(post["texto"])
        print(f"{post['data']} {post['tema']}: {len(avisos)} aviso(s)".strip())
        for aviso in avisos:
            bloqueou = bloqueou or aviso["nivel"] == "bloqueia"
            print(f"  {aviso['nivel'].upper()}: \"{aviso['trecho']}\". {aviso['motivo']}")
    return 1 if bloqueou else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
