from fastapi import FastAPI

app = FastAPI(title="Marketing OS API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
