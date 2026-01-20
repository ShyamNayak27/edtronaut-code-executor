from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Session Schemas ---
class SessionCreate(BaseModel):
    language: str = "python"
    template_code: Optional[str] = ""

class SessionUpdate(BaseModel):
    language: Optional[str] = None
    source_code: Optional[str] = None

class SessionResponse(BaseModel):
    session_id: str
    status: str

# --- Execution Schemas ---
class ExecutionResponse(BaseModel):
    execution_id: str
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    execution_time_ms: Optional[int] = None

    class Config:
        from_attributes = True