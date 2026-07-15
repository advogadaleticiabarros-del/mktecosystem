from fastapi import FastAPI

from app.routers import auth, content, pautas

app = FastAPI(title="Marketing OS API")

app.include_router(auth.router)
app.include_router(pautas.router)
app.include_router(content.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
