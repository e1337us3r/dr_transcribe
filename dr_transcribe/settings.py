import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DR_TRANSCRIBE_",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    rabbitmq_url: str = "amqp://guest:guest@localhost:5672//"
    celery_backend_url: str = "rpc://"

    s3_bucket_name: str = "wudpecker-hackathon"
    aws_region: str = "eu-central-1"
    examiner_type: str = "default"

    openai_api_key: str = ""
    llm_model: str = "facebook/xglm-564M"
    embedding_model: str = "distiluse-base-multilingual-cased-v2"


settings = Settings()
