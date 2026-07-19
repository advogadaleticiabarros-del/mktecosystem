from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, content, pautas, public

if settings.ENVIRONMENT != "development" and settings.JWT_SECRET == "dev-secret-change-in-production":
    raise RuntimeError(
        "JWT_SECRET must be set via environment variable in non-development environments."
    )

app = FastAPI(title="Marketing OS API")

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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
