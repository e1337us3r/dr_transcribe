from pydantic import BaseModel


class QueueTranscriptRequest(BaseModel):
    transcript_id: str
