from fastapi.routing import APIRouter

from dr_transcribe.web.api import monitoring, transcript

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(transcript.router, prefix="/transcript", tags=["transcript"])
