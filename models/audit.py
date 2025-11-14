from sqlalchemy import Column, Integer, String, DateTime, func, JSON, Text, ForeignKey,Float
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    method = Column(String)
    url = Column(String)
    ip_address = Column(String)
    status_code = Column(Integer)
    latency = Column(Float)
    user_agent = Column(String)
    message = Column(String, nullable=True)            # SUCCESS or ERROR message
    response_body = Column(String, nullable=True)      # JSON / text
    error_trace = Column(String, nullable=True)        # stack trace if exception occurs

    created_at = Column(DateTime, server_default=func.now())
