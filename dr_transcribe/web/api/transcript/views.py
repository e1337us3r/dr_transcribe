from fastapi import APIRouter, responses, status

from dr_transcribe.tasks.transcript import process_transcript
from dr_transcribe.web.api.transcript.schema import QueueTranscriptRequest

router = APIRouter()


@router.post("/")
async def queue_transcript_file(
    request: QueueTranscriptRequest,
) -> responses.Response:
    process_transcript.delay(request.transcript_id)
    return responses.Response(content=None, status_code=status.HTTP_202_ACCEPTED)
