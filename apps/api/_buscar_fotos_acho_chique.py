"""Busca fotos no Pexels (foto estática, não vídeo) para os 16 slides
da trend 'Acho Chique' (2 carrosséis de 8, Trabalhista e Família)."""
import os
import requests
from pathlib import Path

API_KEY = os.environ["PEXELS_API_KEY"]
OUT = Path(__file__).parent / "_saida_acho_chique"

QUERIES_TRABALHISTA = [
    "brazilian office team meeting professional",       # 1 capa
    "hands shaking business agreement contract",         # 2 verbas rescisórias
    "pregnant woman working office professional",        # 3 grávida
    "person leaving office end of day",                  # 4 hora extra
    "woman closing laptop leaving work relaxed",          # 5 desconectar
    "woman comforting colleague support workplace",       # 6 assédio moral
    "worker uniform smiling retail store",                # 7 carteira assinada
    "woman reading book library calm confident",          # 8 fechamento
]

QUERIES_FAMILIA = [
    "mother child park sunny day",                        # 1 capa
    "single mother with child home happy",                # 2 pensão em dia
    "father daughter playing park bonding",                # 3 guarda compartilhada
    "child holding hands two parents",                     # 4 visita/pensão
    "mother working from home with child",                 # 5 sozinha
    "mother child grocery shopping together",               # 6 pensão revisão
    "father son video call phone",                          # 7 participar da vida
    "woman reading book library calm confident",            # 8 fechamento
]


def buscar_e_baixar(query: str, destino: Path) -> None:
    resp = requests.get(
        "https://api.pexels.com/v1/search",
        headers={"Authorization": API_KEY},
        params={"query": query, "per_page": 5, "orientation": "portrait"},
        timeout=30,
    )
    resp.raise_for_status()
    photos = resp.json().get("photos", [])
    if not photos:
        raise RuntimeError(f"Nenhum resultado para: {query}")
    foto = photos[0]
    url = foto["src"]["large2x"]
    img = requests.get(url, timeout=60)
    destino.write_bytes(img.content)
    print(f"{destino.name} <- {query} (autor: {foto['photographer']})")


if __name__ == "__main__":
    for i, q in enumerate(QUERIES_TRABALHISTA, start=1):
        buscar_e_baixar(q, OUT / "trabalhista" / f"foto_{i}.jpg")
    for i, q in enumerate(QUERIES_FAMILIA, start=1):
        buscar_e_baixar(q, OUT / "familia" / f"foto_{i}.jpg")
