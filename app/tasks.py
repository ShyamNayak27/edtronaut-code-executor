from .celery_app import celery_app
from .services.executor import execute_python_code
from .database import SessionLocal
from . import models

@celery_app.task(name="execute_code_task")
def execute_code_task(execution_id: str, code: str):
    db = SessionLocal()
    try:
        # Update filter to execution_id
        execution = db.query(models.Execution).filter(models.Execution.execution_id == execution_id).first()
        if not execution:
            return
            
        execution.status = "RUNNING"
        db.commit()

        result = execute_python_code(code)

        execution.status = result["status"]
        execution.stdout = result["stdout"]
        execution.stderr = result["stderr"]
        execution.execution_time_ms = result["execution_time_ms"]
        db.commit()
    finally:
        db.close()