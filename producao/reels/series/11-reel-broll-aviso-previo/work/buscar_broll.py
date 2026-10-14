"""Busca e baixa b-roll no Pexels para as 5 cenas do reel do dia."""
import os

import requests
from pathlib import Path

API_KEY = os.environ["PEXELS_API_KEY"]  # chave fora do git
OUT = Path(__file__).parent

# Uma query por cena, pensada a partir da descrição de b-roll do roteiro
QUERIES = [
    "pregnant woman office working",       # cena 0: gancho, contexto de trabalho
    "pregnant woman reading document",     # cena 1: confirmação/documentação
    "woman working laptop pregnant belly", # cena 2: contexto profissional contínuo
    "pregnant woman calm reflective",      # cena 3: proteção/segurança
    "woman lawyer office professional",    # cena 4: fechamento, advogada
]


def buscar_e_baixar(query: str, indice: int) -> dict:
    resp = requests.get(
        "https://api.pexels.com/videos/search",
        headers={"Authorization": API_KEY},
        params={"query": query, "per_page": 5, "orientation": "portrait"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    videos = data.get("videos", [])
    if not videos:
        raise RuntimeError(f"Nenhum resultado para query: {query}")

    # Escolhe o primeiro vídeo com arquivo HD 1080x1920 (vertical nativo)
    escolhido = None
    arquivo_escolhido = None
    for v in videos:
        for f in v["video_files"]:
            if f["quality"] == "hd" and f["width"] == 1080 and f["height"] == 1920:
                escolhido = v
                arquivo_escolhido = f
                break
        if escolhido:
            break
    if not escolhido:
        # fallback: pega o primeiro vídeo, maior arquivo HD disponível
        escolhido = videos[0]
        hd_files = [f for f in escolhido["video_files"] if f["quality"] == "hd"]
        arquivo_escolhido = max(hd_files, key=lambda f: f["width"]) if hd_files else escolhido["video_files"][0]

    destino = OUT / f"broll_{indice}.mp4"
    video_resp = requests.get(arquivo_escolhido["link"], timeout=60)
    video_resp.raise_for_status()
    destino.write_bytes(video_resp.content)

    return {
        "query": query,
        "arquivo": str(destino),
        "pexels_url": escolhido["url"],
        "autor": escolhido["user"]["name"],
        "duracao_disponivel": escolhido["duration"],
    }


if __name__ == "__main__":
    resultados = []
    for i, q in enumerate(QUERIES):
        info = buscar_e_baixar(q, i)
        resultados.append(info)
        print(f"cena {i}: {info['arquivo']} (query='{q}', autor={info['autor']}, dur={info['duracao_disponivel']}s)")
        print(f"   fonte: {info['pexels_url']}")
