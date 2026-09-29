import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import settings
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/media", tags=["media"])

MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)

EXTENSOES_PERMITIDAS = {".png", ".jpg", ".jpeg"}
TAMANHO_MAXIMO_BYTES = 15 * 1024 * 1024


@router.get("/{arquivo}")
async def servir_midia(arquivo: str) -> FileResponse:
    caminho = (MEDIA_DIR / arquivo).resolve()
    if MEDIA_DIR.resolve() not in caminho.parents or not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(caminho)


@router.post("/upload", status_code=201)
async def upload_midia(
    arquivo: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    extensao = Path(arquivo.filename or "").suffix.lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        raise HTTPException(status_code=422, detail="Formato de arquivo não suportado")

    conteudo = await arquivo.read()
    if len(conteudo) > TAMANHO_MAXIMO_BYTES:
        raise HTTPException(status_code=422, detail="Arquivo excede o tamanho máximo permitido")

    nome_arquivo = f"{uuid.uuid4()}{extensao}"
    (MEDIA_DIR / nome_arquivo).write_bytes(conteudo)

    return {
        "url": f"{settings.PUBLIC_API_URL}/media/{nome_arquivo}",
        "arquivo": nome_arquivo,
    }
