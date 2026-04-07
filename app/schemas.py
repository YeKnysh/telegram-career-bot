from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, example="Schedule interview")
    description: Optional[str] = Field(None, example="Call candidate at 14:00")
    status: TaskStatus = TaskStatus.pending
    assigned_to: Optional[str] = Field(None, example="@manager_bot")

    class Config:
        use_enum_values = True


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_to: Optional[str] = None

    class Config:
        use_enum_values = True


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
