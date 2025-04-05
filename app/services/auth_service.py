from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from ..models.user_model import User
from ..utils.security import verify_password, create_access_token
from ..utils.database import Database
from ..config import settings


class AuthService:
    @staticmethod
    async def create_user(email: str, username: str, password: str) -> Optional[User]:
        """Create a new user in the database"""
        collection = await Database.get_collection(User.collection_name)
        existing_user = await collection.find_one({"email": email})
        if existing_user:
            return None

        user = User(email=email, username=username, password=password)
        await collection.insert_one(user.to_dict())
        return user

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        collection = await Database.get_collection(User.collection_name)
        user_data = await collection.find_one({"email": email})

        if not user_data:
            return None

        user = User.from_dict(user_data)

        if not verify_password(password, user_data["hashed_password"]):
            return None

        return user

    @staticmethod
    def create_user_token(user_id: str) -> dict:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": str(user_id)},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        if not ObjectId.is_valid(user_id):
            return None

        collection = await Database.get_collection(User.collection_name)
        user_data = await collection.find_one({"_id": ObjectId(user_id)})

        if not user_data:
            return None

        return User.from_dict(user_data)
