from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api import router
from .config import settings
from .database import initialize_database


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Reference MVP for a local Cognitive Operating System.",
    )
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    app.include_router(router)

    @app.on_event("startup")
    def startup() -> None:
        initialize_database()

    @app.get("/", include_in_schema=False)
    def home() -> FileResponse:
        return FileResponse(settings.static_dir / "index.html")

    return app
