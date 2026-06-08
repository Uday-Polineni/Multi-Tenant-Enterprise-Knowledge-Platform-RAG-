from arq.connections import RedisSettings

from app.core.config import get_settings
from app.worker.tasks import embed_document_task


class WorkerSettings:
    functions = [embed_document_task]
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
