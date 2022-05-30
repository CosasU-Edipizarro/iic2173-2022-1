import os
from functools import lru_cache
from kombu import Queue
from db.models import ENV

def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = ENV['CELERY_BROKER_URL']
    CELERY_RESULT_BACKEND: str = ENV['CELERY_RESULT_BACKEND']

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),
        # custom queues
        Queue("hello_world"),
    )

    CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()