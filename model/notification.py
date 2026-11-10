from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .base import Base

class NotificationLog(Base):
    """
    Audit log for SMS and Email notifications dispatched across system workflows.
    Tracks inspection alerts (> 30 days) and citizen report status updates.
    """
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(20), nullable=False) # "SMS", "EMAIL"
    recipient = Column(String(100), nullable=False) # Phone number or Email address
    subject = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="SENT", nullable=False) # "SENT", "FAILED", "QUEUED"
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<NotificationLog(channel='{self.channel}', recipient='{self.recipient}', status='{self.status}')>"
