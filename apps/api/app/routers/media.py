from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/media", tags=["media"])

MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)


@router.get("/{arquivo}")
async def servir_midia(arquivo: str) -> FileResponse:
    caminho = (MEDIA_DIR / arquivo).resolve()
    if MEDIA_DIR.resolve() not in caminho.parents or not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(caminho)
