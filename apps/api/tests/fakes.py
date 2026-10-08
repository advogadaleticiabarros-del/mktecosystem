from pathlib import Path


class RenderizadorFalso:
    """Registra o que foi pedido e cria um arquivo vazio no caminho de saída."""

    def __init__(self) -> None:
        self.chamadas: list[tuple[str, str]] = []

    async def slide(self, texto, indice, total, identidade_visual, caminho_saida):
        self.chamadas.append(("slide", texto))
        Path(caminho_saida).write_bytes(b"")

    async def frase(self, texto, identidade_visual, caminho_saida):
        self.chamadas.append(("frase", texto))
        Path(caminho_saida).write_bytes(b"")

    async def pergunta(self, texto, identidade_visual, caminho_saida):
        self.chamadas.append(("pergunta", texto))
        Path(caminho_saida).write_bytes(b"")
