from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .tasks import execute_code_task

from . import models, schemas, database

# 1. Initialize the Database
database.init_db()

# 2. Create the FastAPI instance 
app = FastAPI(title="Edtronaut Code Execution API")

# 3. Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

# Requirement 2.1.1
@app.post("/code-sessions", response_model=schemas.SessionResponse)
def create_session(session_data: schemas.SessionCreate, db: Session = Depends(get_db)):
    new_session = models.CodeSession(
        language=session_data.language,
        source_code=session_data.template_code
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    # Return the new field name
    return {"session_id": new_session.session_id, "status": "ACTIVE"}

# Requirement 2.1.2
@app.patch("/code-sessions/{session_id}", response_model=schemas.SessionResponse)
def update_session(session_id: str, update_data: schemas.SessionUpdate, db: Session = Depends(get_db)):
    # Filter by session_id
    db_session = db.query(models.CodeSession).filter(models.CodeSession.session_id == session_id).first()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if update_data.language:
        db_session.language = update_data.language
    if update_data.source_code is not None:
        db_session.source_code = update_data.source_code
        
    db.commit()
    return {"session_id": db_session.session_id, "status": "ACTIVE"}

# Requirement 2.1.3
@app.post("/code-sessions/{session_id}/run")
def run_code(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(models.CodeSession).filter(models.CodeSession.session_id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    new_execution = models.Execution(
        session_id=session_id,
        status="QUEUED"
    )
    db.add(new_execution)
    db.commit()
    db.refresh(new_execution)

    execute_code_task.delay(new_execution.execution_id, db_session.source_code)
    
    return {"execution_id": new_execution.execution_id, "status": "QUEUED"}

# Requirement 2.2.1
@app.get("/executions/{execution_id}", response_model=schemas.ExecutionResponse)
def get_execution_result(execution_id: str, db: Session = Depends(get_db)):
    # Filter by execution_id
    execution = db.query(models.Execution).filter(models.Execution.execution_id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution