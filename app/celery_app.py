from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    # This line is the fix! It tells the worker to load the tasks file.
    include=["app.tasks"] 
)

#Ensure the worker uses the same queue name
celery_app.conf.task_default_queue = 'main_queue'