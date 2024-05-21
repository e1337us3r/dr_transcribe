from celery import Celery
from dr_transcribe.settings import settings

app = Celery(
    "dr_transcribe",
    broker=settings.rabbitmq_url,
    backend=settings.celery_backend_url,
    include=["dr_transcribe.tasks.transcript"],
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
