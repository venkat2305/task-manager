from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings


class Database:
    client = None
    db = None

    @classmethod
    async def connect(cls):
        """Establish async connection to MongoDB using Motor"""
        if cls.client is None:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.DATABASE_NAME]
        return cls.db

    @classmethod
    async def get_collection(cls, collection_name: str):
        if cls.db is None:
            await cls.connect()
        return cls.db[collection_name]

    @classmethod
    async def close(cls):
        """Close the MongoDB connection"""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None
