#backend/api/main.py
from __future__ import annotations
from backend.api.routes import assets, views
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Archimera Backend", version="0.1.0")

    app.include_router(assets.router)
    app.include_router(views.router)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    return app


app = create_app()
