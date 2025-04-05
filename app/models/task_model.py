from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from bson import ObjectId
from enum import Enum


class PyObjectId(ObjectId):
    """Custom ObjectId class for Pydantic models"""
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.string_schema(),
                core_schema.no_info_plain_validator_function(PyObjectId.validate),
                core_schema.is_instance_schema(ObjectId),
            ]),
        ])

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class Task:
    """OOP-based Task model for database operations"""

    collection_name = "tasks"

    def __init__(self, title: str, user_id: PyObjectId, 
                 description: Optional[str] = None,
                 status: str = TaskStatus.PENDING,
                 task_id: Optional[PyObjectId] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.task_id = task_id or ObjectId()
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at  # No default value, will be None for new tasks

    def to_dict(self):
        """Convert Task object to dictionary for database storage"""
        return {
            "_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Task object from dictionary"""
        if not data:
            return None
        return cls(
            task_id=data.get("_id"),
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

# Pydantic models for request/response validation
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Complete project",
                "description": "Finish the task management API project",
                "status": "pending"
            }
        }
    }

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "status": "in-progress"
            }
        }
    }

class TaskInDB(TaskBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3f36a9ac0cb22bb",
                "title": "Complete project",
                "description": "Finish the task management API project",
                "status": "pending",
                "user_id": "60d5ec9af3f36a9ac0cb22aa",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": None
            }
        }
    }

    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, dt: datetime):
        return dt.isoformat() if dt else None