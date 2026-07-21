from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    auth,
    avaliacoes,
    calendario,
    content,
    dashboard,
    email,
    integracoes,
    media,
    pautas,
    public,
)

if settings.ENVIRONMENT != "development" and settings.JWT_SECRET == "dev-secret-change-in-production":
    raise RuntimeError(
        "JWT_SECRET must be set via environment variable in non-development environments."
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = None
    if settings.ENABLE_SCHEDULER:
        from app.scheduler import criar_scheduler

        scheduler = criar_scheduler()
        scheduler.start()
    yield
    if scheduler is not None:
        scheduler.shutdown(wait=False)


app = FastAPI(title="Marketing OS API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pautas.router)
app.include_router(content.router)
app.include_router(public.router)
app.include_router(email.router)
app.include_router(calendario.router)
app.include_router(dashboard.router)
app.include_router(integracoes.router)
app.include_router(media.router)
app.include_router(avaliacoes.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
