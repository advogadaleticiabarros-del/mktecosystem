"""Acervo: as peças editáveis em disco. Guarda as regras da marca e nunca apaga material pronto:
original.json e saídas não são sobrescritos. Cada peça é pecas/<nome>/{peca.json, original.json, fotos/}."""
import io
import json
import re
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps

FONTES = {"EB Garamond", "Inter"}  # Cormorant reprovada pela Dra.; ver docs/PASSAGEM_DE_CONTEXTO.md
TAMANHO_MINIMO = 22  # docs/MANUAL_CONTEUDO_REDES.md: nada abaixo de 22 px
LADO_MAXIMO_FOTO = 2400
_NOME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")
_FOTO = re.compile(r"^[A-Za-z0-9_-]+\.jpg$")


class PecaInvalida(ValueError):
    """A mensagem é mostrada a quem está editando."""


def _validar(doc):
    if not isinstance(doc, dict) or not isinstance(doc.get("elementos"), list):
        raise PecaInvalida("Peça sem elementos.")
    for e in doc["elementos"]:
        tipo = e.get("tipo") if isinstance(e, dict) else None
        if tipo not in ("texto", "imagem", "retangulo", "luz"):
            raise PecaInvalida(f"Elemento desconhecido: {tipo}.")
        if tipo == "texto":
            if e.get("fonte") not in FONTES:
                raise PecaInvalida("Use EB Garamond ou Inter.")
            if not isinstance(e.get("tamanho"), (int, float)) or e["tamanho"] < TAMANHO_MINIMO:
                raise PecaInvalida(f"Nenhum texto pode ficar abaixo de {TAMANHO_MINIMO} px.")
        if tipo == "imagem" and not _FOTO.match(str(e.get("arquivo", ""))):
            raise PecaInvalida("Foto inválida.")


class Acervo:
    def __init__(self, raiz):
        self._raiz = Path(raiz)
        self._pecas = self._raiz / "pecas"
        self._saidas = self._raiz / "saidas"

    def _pasta(self, nome):
        if not _NOME.match(str(nome)):
            raise PecaInvalida("Use só letras, números, hífen e sublinhado no nome.")
        return self._pecas / nome

    def _existente(self, nome):
        pasta = self._pasta(nome)
        if not (pasta / "peca.json").exists():
            raise PecaInvalida(f"Peça não encontrada: {nome}.")
        return pasta

    @staticmethod
    def _gravar(caminho, doc):
        temp = caminho.with_suffix(".tmp")
        temp.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        temp.replace(caminho)  # troca atômica: queda de energia não deixa peça pela metade

    def nomes(self):
        return sorted(p.parent.name for p in self._pecas.glob("*/peca.json"))

    def abrir(self, nome):
        return json.loads((self._existente(nome) / "peca.json").read_text(encoding="utf-8"))

    def criar(self, nome, doc, fotos=None):
        """fotos: {arquivo: bytes} já tratadas, gravadas como vieram."""
        pasta = self._pasta(nome)
        if pasta.exists():
            raise PecaInvalida(f"Já existe uma peça chamada {nome}.")
        _validar(doc)
        for arquivo in fotos or {}:
            if not _FOTO.match(arquivo):
                raise PecaInvalida("Foto inválida.")
        (pasta / "fotos").mkdir(parents=True)
        for arquivo, dados in (fotos or {}).items():
            (pasta / "fotos" / arquivo).write_bytes(dados)
        self._gravar(pasta / "peca.json", doc)
        self._gravar(pasta / "original.json", doc)

    def salvar(self, nome, doc):
        pasta = self._existente(nome)
        _validar(doc)
        self._gravar(pasta / "peca.json", doc)

    def restaurar(self, nome):
        pasta = self._existente(nome)
        doc = json.loads((pasta / "original.json").read_text(encoding="utf-8"))
        self._gravar(pasta / "peca.json", doc)
        return doc

    def copiar(self, nome, novo):
        origem = self._existente(nome)
        destino = self._pasta(novo)
        if destino.exists():
            raise PecaInvalida(f"Já existe uma peça chamada {novo}.")
        doc = self.abrir(nome)
        shutil.copytree(origem / "fotos", destino / "fotos")
        self._gravar(destino / "peca.json", doc)
        self._gravar(destino / "original.json", doc)

    def guardar_foto(self, nome, dados):
        pasta = self._existente(nome)
        try:
            imagem = ImageOps.exif_transpose(Image.open(io.BytesIO(dados))).convert("RGB")
        except Exception as erro:
            raise PecaInvalida("Esse arquivo não é uma imagem que eu consiga abrir.") from erro
        imagem.thumbnail((LADO_MAXIMO_FOTO, LADO_MAXIMO_FOTO), Image.LANCZOS)
        arquivo = f"{uuid.uuid4().hex}.jpg"
        imagem.save(pasta / "fotos" / arquivo, "JPEG", quality=92)
        return {"arquivo": arquivo, "largura": imagem.width, "altura": imagem.height}

    def caminho_foto(self, nome, arquivo):
        if not _FOTO.match(str(arquivo)):
            raise PecaInvalida("Foto inválida.")
        return self._existente(nome) / "fotos" / arquivo

    def guardar_saida(self, nome, dados):
        self._existente(nome)
        self._saidas.mkdir(exist_ok=True)
        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
        caminho, n = self._saidas / f"{nome}-{carimbo}.jpg", 2
        while caminho.exists():
            caminho, n = self._saidas / f"{nome}-{carimbo}-{n}.jpg", n + 1
        caminho.write_bytes(dados)
        return caminho

    def caminho_saida(self, arquivo):
        if not re.match(r"^[A-Za-z0-9_-]+\.jpg$", str(arquivo)):
            raise PecaInvalida("Arquivo inválido.")
        return self._saidas / arquivo
