from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.logging_config import configure_logging

configure_logging()

# async def health() -> FastAPI:
#     app = FastAPI()

#     @app.get("/health")

#     return {"status": "ok"}

def create_app() -> FastAPI:
    app = FastAPI(
        title="SportsApp Service",
        version="1.0.0"
    )

    # Register API routers
    app.include_router(api_router, prefix="/api/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"], # Your frontend URL
        allow_credentials=True,
        allow_methods=["*"], # Allows GET, POST, etc.
        allow_headers=["*"], # Allows all headers
    )

    return app


# This is the ASGI app uvicorn expects
app = create_app()
