# retrieval/api/main.py
from fastapi import FastAPI

app = FastAPI(title="Archimera Retrieval")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search():
    return {"message": "Search API is up and running!"}
