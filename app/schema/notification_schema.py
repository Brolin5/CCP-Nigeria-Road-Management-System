from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NotificationBase(BaseModel):
    channel: str = Field(default="SMS", max_length=20, description="SMS, EMAIL")
    recipient: str = Field(..., max_length=100)
    subject: Optional[str] = Field(None, max_length=200)
    message: str
    status: str = Field(default="SENT", max_length=50)

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    channel: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None

class NotificationResponse(NotificationBase):
    id: int
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True
