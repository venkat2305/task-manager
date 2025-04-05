from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional
from bson import ObjectId
from ..utils.security import get_password_hash


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


class User:
    collection_name = "users"

    def __init__(self, email: str, username: str, password: str, 
                 user_id: Optional[PyObjectId] = None,
                 created_at: Optional[datetime] = None):
        self.user_id = user_id or ObjectId()
        self.email = email
        self.username = username
        self.hashed_password = get_password_hash(password) if password else None
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            user_id=data.get("_id"),
            email=data.get("email"),
            username=data.get("username"),
            password=None,  # Don't set password from dict
            created_at=data.get("created_at")
        )


# Pydantic models for request/response validation
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    }


class UserInDB(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "_id": "60d5ec9af3f36a9ac0cb22aa",
                "email": "user@example.com",
                "username": "johndoe",
                "created_at": "2023-01-01T00:00:00"
            }
        }
    }

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime):
        return dt.isoformat()


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    }


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }


class TokenData(BaseModel):
    user_id: Optional[str] = None
