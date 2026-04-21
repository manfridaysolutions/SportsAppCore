from fastapi import FastAPI
from app.api.v1.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="SportsApp Service",
        version="1.0.0"
    )

    # Register API routers
    app.include_router(api_router, prefix="/api/v1")

    return app


# This is the ASGI app uvicorn expects
app = create_app()
