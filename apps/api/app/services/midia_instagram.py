"""Transforma uma peça aprovada nas imagens e na legenda que vão pro Instagram.

Interface: `montar_midia(piece, ...)` devolve `Midia(imagens, legenda,
primeiro_comentario)` — uma URL pública por imagem já renderizada em `pasta`, e o
comentário que o próprio perfil publica logo depois do post ("" = nenhum). Uma
imagem = post único; várias = carrossel. Quem publica não precisa saber o formato da peça. Se a
peça já traz arte pronta (`imagem` / `imagens` no corpo), ela é usada como está.

`publicavel(tipo)` diz se o tipo tem imagem própria (os demais — legenda,
stories, reels, artigo, jornal — não passam por aqui).
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from app.models.content_piece import ContentPiece
from app.services import render_criativo


class PecaSemConteudo(ValueError):
    """A peça não tem o texto que vira imagem (ex.: frase vazia)."""


@dataclass(frozen=True)
class Midia:
    imagens: list[str]
    legenda: str
    primeiro_comentario: str = ""


class Renderizador(Protocol):
    async def slide(self, texto: str, indice: int, total: int, identidade_visual: dict, caminho_saida: str) -> None: ...
    async def frase(self, texto: str, identidade_visual: dict, caminho_saida: str) -> None: ...
    async def pergunta(self, texto: str, identidade_visual: dict, caminho_saida: str) -> None: ...


class RenderizadorPlaywright:
    async def slide(self, texto, indice, total, identidade_visual, caminho_saida):
        await render_criativo.renderizar_slide(texto, indice, total, identidade_visual, caminho_saida)

    async def frase(self, texto, identidade_visual, caminho_saida):
        await render_criativo.renderizar_frase_impacto(texto, identidade_visual, caminho_saida)

    async def pergunta(self, texto, identidade_visual, caminho_saida):
        await render_criativo.renderizar_pergunta(texto, identidade_visual, caminho_saida)


# tipo da peça → (método do renderizador, campo do corpo com o texto da imagem)
_IMAGEM_UNICA = {
    "frase": ("frase", "frase"),
    "pergunta": ("pergunta", "pergunta"),
    "estatico": ("frase", "texto_overlay"),
}


def publicavel(tipo: str) -> bool:
    return tipo == "carrossel" or tipo in _IMAGEM_UNICA


def _legenda(corpo: dict) -> str:
    partes = [corpo.get("legenda", "").strip(), corpo.get("cta", "").strip()]
    return "\n\n".join(p for p in partes if p)


def _midia(imagens: list[str], corpo: dict) -> Midia:
    return Midia(
        imagens=imagens,
        legenda=_legenda(corpo),
        primeiro_comentario=(corpo.get("primeiro_comentario") or "").strip(),
    )


async def montar_midia(
    piece: ContentPiece,
    *,
    identidade_visual: dict,
    pasta: Path,
    base_url: str,
    prefixo: str,
    renderizador: Renderizador | None = None,
) -> Midia:
    render = renderizador or RenderizadorPlaywright()
    corpo = piece.corpo or {}
    pasta.mkdir(parents=True, exist_ok=True)

    def caminho(i: int) -> tuple[str, str]:
        nome = f"{prefixo}-{i}.png"
        return str(pasta / nome), f"{base_url}/{nome}"

    # Arte já enviada à mão (POST /media/upload) tem prioridade sobre a gerada.
    if piece.tipo == "carrossel" and corpo.get("imagens"):
        return _midia(list(corpo["imagens"]), corpo)
    if piece.tipo in _IMAGEM_UNICA and corpo.get("imagem"):
        return _midia([corpo["imagem"]], corpo)

    if piece.tipo == "carrossel":
        slides = [s for s in corpo.get("slides", []) if s]
        if not slides:
            raise PecaSemConteudo("carrossel sem slides")
        urls = []
        for i, texto in enumerate(slides):
            local, url = caminho(i)
            await render.slide(texto, i, len(slides), identidade_visual, local)
            urls.append(url)
        return _midia(urls, corpo)

    if piece.tipo not in _IMAGEM_UNICA:
        raise PecaSemConteudo(f"tipo '{piece.tipo}' não tem imagem para o Instagram")

    metodo, campo = _IMAGEM_UNICA[piece.tipo]
    texto = (corpo.get(campo) or "").strip()
    if not texto:
        raise PecaSemConteudo(f"{piece.tipo} sem '{campo}'")
    local, url = caminho(0)
    await getattr(render, metodo)(texto, identidade_visual, local)
    return _midia([url], corpo)
