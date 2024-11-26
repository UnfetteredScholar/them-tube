from core.config import settings
from fastapi import APIRouter, responses
from schemas.health import Health, Status

router = APIRouter()


class HealthResponse(responses.JSONResponse):
    media_type = "application/health+json"


@router.get(
    "/health",
    response_model=Health,
    response_class=HealthResponse,
    responses={500: {"model": Health}},
)
async def get_health(response: HealthResponse):
    """API Healt Endpoint"""
    response.headers["Cache-Control"] = "max-age=3600"

    content = {
        "status": Status.PASS,
        "version": settings.VERSION,
        "release_id": settings.RELEASE_ID,
    }

    return content
