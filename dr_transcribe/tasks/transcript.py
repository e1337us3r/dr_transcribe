from dr_transcribe.celery import app
from dr_transcribe.settings import settings
from dr_transcribe.tasks.util.aws import S3Helper
from dr_transcribe.tasks.util.embedding_examiner import EmbeddingExaminer
from dr_transcribe.tasks.util.examiner import BaseExaminor
from dr_transcribe.tasks.util.llm_examiner import LLMExaminer
from dr_transcribe.tasks.util.openai_examiner import OpenAIExaminer


def _create_examiner(settings_) -> BaseExaminor:
    if settings.examiner_type == "openai":
        examiner = OpenAIExaminer(settings_.openai_api_key)
    elif settings.examiner_type == "llm":
        examiner = LLMExaminer(model=settings_.llm_model)
    else:
        examiner = EmbeddingExaminer(model=settings_.embedding_model)

    return examiner


@app.task
def process_transcript(transcript_id: str) -> float:
    s3helper = S3Helper(settings.aws_region, settings.s3_bucket_name)
    data_parsed = s3helper.read_json(transcript_id)

    examiner = _create_examiner(settings)

    score = examiner.examine(data_parsed)

    return score
