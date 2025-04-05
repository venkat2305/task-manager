from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from ..models.task_model import Task, PyObjectId
from ..utils.database import Database


class TaskService:
    @staticmethod
    async def create_task(title: str, user_id: str, description: Optional[str] = None, status: str = "pending") -> Task:
        collection = await Database.get_collection(Task.collection_name)

        task = Task(
            title=title,
            description=description,
            status=status,
            user_id=PyObjectId(user_id)
        )

        await collection.insert_one(task.to_dict())
        return task

    @staticmethod
    async def get_tasks_by_user(user_id: str) -> List[Task]:
        collection = await Database.get_collection(Task.collection_name)
        tasks_cursor = collection.find({"user_id": PyObjectId(user_id)})

        tasks = []
        async for task_data in tasks_cursor:
            tasks.append(Task.from_dict(task_data))
        return tasks

    @staticmethod
    async def get_task_by_id(task_id: str, user_id: str) -> Optional[Task]:
        if not ObjectId.is_valid(task_id):
            return None

        collection = await Database.get_collection(Task.collection_name)
        task_data = await collection.find_one({
            "_id": ObjectId(task_id),
            "user_id": PyObjectId(user_id)
        })

        if not task_data:
            return None

        return Task.from_dict(task_data)

    @staticmethod
    async def update_task(task_id: str, user_id: str, update_data: dict) -> Optional[Task]:
        if not ObjectId.is_valid(task_id):
            return None

        collection = await Database.get_collection(Task.collection_name)

        # Only include non-None values in the update
        update_fields = {k: v for k, v in update_data.items() if v is not None}
        
        # Set updated_at timestamp for any actual update
        if update_fields:
            update_fields["updated_at"] = datetime.now(timezone.utc)

        # Only perform update if there are fields to update
        if not update_fields:
            # No actual changes to make
            return await TaskService.get_task_by_id(task_id, user_id)

        result = await collection.update_one(
            {"_id": ObjectId(task_id), "user_id": PyObjectId(user_id)},
            {"$set": update_fields}
        )

        if result.modified_count == 0:
            return None

        return await TaskService.get_task_by_id(task_id, user_id)

    @staticmethod
    async def delete_task(task_id: str, user_id: str) -> bool:
        if not ObjectId.is_valid(task_id):
            return False

        collection = await Database.get_collection(Task.collection_name)
        result = await collection.delete_one({
            "_id": ObjectId(task_id),
            "user_id": PyObjectId(user_id)
        })

        return result.deleted_count > 0
