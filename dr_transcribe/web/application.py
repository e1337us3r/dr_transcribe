from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from dr_transcribe.logging import configure_logging
from dr_transcribe.web.api.router import api_router
from dr_transcribe.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="dr_transcribe",
        version=metadata.version("dr_transcribe"),
        docs_url="/api/docs",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
