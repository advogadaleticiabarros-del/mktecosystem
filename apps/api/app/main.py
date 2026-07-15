from fastapi import FastAPI

from app.routers import auth, pautas

app = FastAPI(title="Marketing OS API")

app.include_router(auth.router)
app.include_router(pautas.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
