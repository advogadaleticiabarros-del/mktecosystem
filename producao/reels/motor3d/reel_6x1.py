"""Reels "Fim da 6x1" no motor 3D (15/10/2026), inspirado no formato de mundo em miniatura com câmera contínua.
Fatos: PEC 221/2019 aprovada no Senado em 14/10/2026, dois turnos no mesmo dia, 75 a 1 (Senado Notícias, Agência
Brasil); vai à promulgação pelo Congresso (emenda constitucional, sem sanção); 2 meses após a publicação: 2 folgas e
42 h; mais 1 ano: 40 h; sem redução salarial (Agência Câmara). Ainda não está em vigor.

Uso: py reel_6x1.py --checar | --amostras | --render
Áudio: com a gravação da Letícia em fontes/narracao.* + transcricao.json (Whisper), os tempos vêm das palavras;
sem ela, usa tempos estimados (prévia muda).
"""
import asyncio
import json
import sys
from pathlib import Path

import motor3d as m3

AQUI = Path(__file__).resolve().parent
TRABALHO = Path(r"C:\tmp\videos-reels\14-reels-3d-6x1")
TRANSCRICAO = TRABALHO / "fontes" / "transcricao.json"

BLOCOS = [
    "Acabou a escala 6x1? Calma. Ainda não.",
    "Na quarta-feira, o Senado aprovou a proposta em dois turnos, no mesmo dia. 75 votos a 1.",
    "Como ela muda a Constituição, não passa pela sanção do presidente. O próprio Congresso promulga.",
    "E aí começa a contagem. Dois meses depois da publicação: duas folgas por semana e, no máximo, 42 horas.",
    "Um ano depois: 40 horas. E sem reduzir o salário.",
    "Até lá, vale a regra de hoje. Então guarda os seus contracheques e o seu espelho de ponto.",
    "Manda esse vídeo pra quem trabalha na 6x1. Cada caso tem detalhes: procure uma advogada de confiança.",
]
DESTAQUES = {"6x1", "ainda", "não", "senado", "dois", "turnos", "75", "1", "constituição", "sanção", "congresso",
             "promulga", "contagem", "meses", "duas", "folgas", "42", "horas", "40", "salário", "contracheques",
             "ponto", "advogada"}


def palavras_estimadas() -> list[dict]:
    """Tempos estimados (prévia sem áudio): ~2,6 palavras/s, pausa de 0,5 s entre blocos."""
    ws, t = [], 0.4
    for bloco in BLOCOS:
        for p in bloco.split():
            d = 0.16 + 0.055 * len(p) + (0.18 if p[-1] in ".?:," else 0)
            ws.append({"t": p, "a": round(t, 2), "b": round(t + d - 0.04, 2)})
            t += d
        t += 0.5
    return ws


def palavras() -> list[dict]:
    if TRANSCRICAO.exists():
        r = json.loads(TRANSCRICAO.read_text(encoding="utf-8"))
        return [{"t": w["word"].strip(), "a": w["start"], "b": w["end"]} for s in r["segments"] for w in s["words"]]
    return palavras_estimadas()


def montar() -> dict:
    ws = palavras()
    for w in ws:
        w["d"] = w["t"].lower().strip(".,?!:") in DESTAQUES

    def W(txt: str, depois: float = -1.0) -> float:
        return next(w["a"] for w in ws if w["a"] > depois and w["t"].lower().strip(".,?!:") == txt.lower().strip(".,?!:"))

    # legenda: blocos de até 24 caracteres, quebra em pontuação
    legendas, atual, n = [], [], 0
    for w in ws:
        if atual and (n + len(w["t"]) > 24 or atual[-1]["t"][-1] in ".?!:"):
            legendas.append({"a": atual[0]["a"], "b": atual[-1]["b"] + 0.3, "w": atual}); atual, n = [], 0
        atual.append(w); n += len(w["t"]) + 1
    if atual:
        legendas.append({"a": atual[0]["a"], "b": atual[-1]["b"] + 0.3, "w": atual})

    t_sen, t_const, t_cont, t_ano = W("Na"), W("Como"), W("E", W("promulga.")), W("Um")
    t_ate, t_cta = W("Até"), W("Manda")
    fim = ws[-1]["b"] + 0.4
    total = round(fim + 3.6, 2)

    SEM = [4.5, 7.5, 21, 0.3, -1.3, 0]
    CONG = [14, 9.2, 25, 9, 0.05, 0]
    CONST = [20.8, 7.2, 16, 17.6, -1.0, 0]
    SEM2 = [-2.5, 7.5, 21, 0.2, -1.3, 0]
    COFRE = [-5.2, 6.5, 15, -8.0, -0.9, 0]
    PAP = [-5.0, 6.4, 13, -7.3, -1.0, 0]
    camera = [
        [0, [7, 10.5, 29, 0.3, -1.3, 0]], [1.4, SEM], [t_sen - 0.2, SEM], [t_sen + 1.2, CONG],
        [t_const - 0.2, CONG], [t_const + 1.2, CONST], [t_cont - 0.2, CONST], [t_cont + 1.2, SEM2],
        [W("salário.") - 0.9, SEM2], [W("salário.") + 0.4, COFRE], [t_ate + 0.6, COFRE], [t_ate + 1.6, PAP],
        [t_cta, PAP], [t_cta + 1.4, [4, 15, 42, 3, 0, 0]],
    ]
    trilhas = {
        "semana_sobe": [[0.2, 0], [1.6, 1]],
        "horas": [[0, 1], [W("42") - 0.2, 1], [W("42") + 0.6, 42 / 44], [W("40") - 0.1, 42 / 44], [W("40") + 0.7, 40 / 44]],
        "sabado_folga": [[0, 0], [W("duas", t_cont) - 0.1, 0], [W("folgas") + 0.3, 1]],
        "carimbo_vis": [[0, 0], [W("aprovou") - 0.1, 1], [t_const, 1], [t_const + 0.01, 0]],
        "carimbo": [[0, 0], [W("aprovou") - 0.05, 0], [W("aprovou") + 0.45, 1]],
        "livro_abre": [[0, 0], [W("Constituição,") - 0.2, 0], [W("Constituição,") + 0.8, 1]],
        "assina": [[0, 0], [W("promulga.") - 0.3, 0], [W("promulga.") + 0.6, 1]],
        "moedas": [[0, 0], [W("salário.") + 0.2, 0], [W("salário.") + 1.3, 1]],
        "papeis": [[0, 0], [W("guarda") - 0.2, 0], [W("guarda") + 1.0, 1]],
    }
    capitulos = [
        {"a": 0.2, "b": t_sen - 0.1, "texto": "Fim da 6x1"},
        {"a": t_sen, "b": t_const - 0.1, "texto": "Senado"},
        {"a": t_const, "b": t_cont - 0.1, "texto": "Promulgação"},
        {"a": t_cont, "b": W("salário.") + 0.2, "texto": "A contagem"},
        {"a": W("salário.") + 0.3, "b": t_ate - 0.1, "texto": "Salário"},
        {"a": t_ate, "b": t_cta - 0.1, "texto": "Até lá"},
    ]
    callouts = [
        {"a": W("quarta-feira,"), "b": W("turnos,") + 0.2, "texto": "Quarta, 14/10", "sub": "votação no Senado", "ancora": [9, 3.35, -0.6], "dx": -250, "dy": -70},
        {"a": W("turnos,"), "b": t_const - 0.2, "texto": "2 turnos", "sub": "no mesmo dia", "ancora": [11, 1.4, 0.3], "dx": 150, "dy": -150},
        {"a": W("sanção"), "b": W("promulga.") - 0.1, "texto": "Sanção do presidente", "sub": "não passa por ela", "risco": True, "ancora": [18.7, 1.35, 0], "dx": 140, "dy": -240},
        {"a": W("Congresso"), "b": t_cont - 0.2, "texto": "O Congresso promulga", "sub": "vira emenda", "ancora": [18, 1.35, 0], "dx": -150, "dy": -230},
        {"a": W("meses"), "b": W("42") - 0.3, "texto": "+2 meses", "sub": "depois da publicação", "ancora": [-2.4, 2.2, 0], "dx": 120, "dy": -230},
        {"a": W("contracheques"), "b": t_cta - 0.2, "texto": "Contracheques", "sub": "guarde todos", "ancora": [-7.2, 0.1, 0.1], "dx": -170, "dy": -260},
        {"a": W("ponto."), "b": t_cta - 0.2, "texto": "Espelho de ponto", "sub": "as horas reais", "ancora": [-6.6, 0.1, -0.3], "dx": 160, "dy": -360},
    ]
    selos = [
        {"a": W("Ainda"), "b": t_sen - 0.2, "texto": "Ainda não vale", "x": 540, "y": 1010, "rot": -5},
        {"a": W("aprovou") + 0.45, "b": W("75") - 0.2, "texto": "Aprovada", "x": 700, "y": 520, "rot": -6},
        {"a": W("salário.") + 0.4, "b": t_ate - 0.2, "texto": "Salário mantido", "x": 540, "y": 1010, "rot": -4},
    ]
    numeros = [
        {"a": W("75"), "b": t_const - 0.2, "texto": "75 × 1", "sub": "votos no Senado", "x": 540, "y": 1000, "size": 160},
        {"a": W("42"), "b": W("40") - 0.2, "texto": "42 h", "sub": "por semana", "x": 540, "y": 1000, "size": 180},
        {"a": W("40"), "b": W("salário.") + 0.2, "texto": "40 h", "sub": "por semana", "x": 540, "y": 1000, "size": 180},
    ]
    return {"tema": "Escala 6x1", "total": total, "camera": camera, "trilhas": trilhas, "capitulos": capitulos,
            "callouts": callouts, "selos": selos, "numeros": numeros, "legendas": legendas,
            "fechamento": {"a": t_cta + 0.2, "titulo": "Manda pra quem trabalha na 6x1"}}


def main(argv):
    R = montar()
    if "--checar" in argv:
        erros = asyncio.run(m3.checar(R))
        print("\n".join(erros[:40]) if erros else "área limpa: ok", f"({len(erros)} avisos)")
    if "--amostras" in argv:
        ts = [float(x) for x in next((a.split("=")[1] for a in argv if a.startswith("--t=")), "").split(",") if x] or \
             [1.0, 3.5, 6.5, 9.0, 13.0, 16.5, 20.5, 24.0, 27.0, 31.0, R["total"] - 1]
        for f in asyncio.run(m3.amostras(R, ts, TRABALHO / "amostras")):
            print(f)
    if "--render" in argv:
        TRABALHO.mkdir(parents=True, exist_ok=True)
        asyncio.run(m3.video_mudo(R, TRABALHO / "video_mudo.mp4"))
        print("ok", TRABALHO / "video_mudo.mp4", R["total"], "s")


if __name__ == "__main__":
    main(sys.argv[1:])
