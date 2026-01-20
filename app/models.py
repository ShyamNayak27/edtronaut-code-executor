import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CodeSession(Base):
    __tablename__ = "code_sessions"
    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    language = Column(String, default="python")
    source_code = Column(Text, default="")
    status = Column(String, default="ACTIVE")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Execution(Base):
    __tablename__ = "executions"
    execution_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String)
    status = Column(String, default="QUEUED")
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)