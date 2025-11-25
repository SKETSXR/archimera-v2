from fastapi import FastAPI

app = FastAPI(title="Archimera Backend")

@app.get("/health")
def health():
    return {"status": "ok"}