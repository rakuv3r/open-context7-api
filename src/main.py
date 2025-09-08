"""FastAPI application main entry point."""

from fastapi import FastAPI

from src import __version__
from src.api import router as api_router
from src.core.config import settings
from src.core.constants import APP_NAME
from src.core.logging import setup_logging
from src.core.sentry import setup_sentry
from src.middleware import register_middlewares


# Setup monitoring and logging
setup_sentry()
setup_logging()

app = FastAPI(**settings.fastapi_config)

# Register middlewares
register_middlewares(app)

# Include API routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def get_api_info() -> dict[str, str]:
    """## API Information.

    Get basic service info including name and version.

    ### Returns
    - **service** (str): Service name
    - **version** (str): Version number

    ### Example Response
    ```json
    {
        "service": "open-context7-api",
        "version": "v0.0.1"
    }
    ```
    """
    return {
        "service": APP_NAME,
        "version": __version__,
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """## Health Check.

    Check if service is running properly.

    ### Returns
    - **status** (str): Health status (always "healthy")

    ### Example Response
    ```json
    {
        "status": "healthy"
    }
    ```
    """
    return {"status": "healthy"}
