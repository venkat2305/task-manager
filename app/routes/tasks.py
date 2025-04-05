from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..models.task_model import TaskCreate, TaskUpdate, TaskInDB
from ..services.task_service import TaskService
from ..utils.security import decode_access_token
from ..services.auth_service import AuthService

router = APIRouter(tags=["Tasks"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await AuthService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, current_user=Depends(get_current_user)):
    task = await TaskService.create_task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=str(current_user.user_id)
    )

    return {
        "_id": str(task.task_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": str(task.user_id),
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }


@router.get("/", response_model=List[TaskInDB])
async def get_all_tasks(current_user=Depends(get_current_user)):
    tasks = await TaskService.get_tasks_by_user(str(current_user.user_id))

    return [
        {
            "_id": str(task.task_id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": str(task.user_id),
            "created_at": task.created_at,
            "updated_at": task.updated_at
        } for task in tasks
    ]


@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str, current_user=Depends(get_current_user)):
    task = await TaskService.get_task_by_id(
        task_id=task_id,
        user_id=str(current_user.user_id)
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "_id": str(task.task_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": str(task.user_id),
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }


@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(task_id: str, task_data: TaskUpdate, current_user=Depends(get_current_user)):
    update_data = task_data.model_dump(exclude_unset=True)

    task = await TaskService.update_task(
        task_id=task_id,
        user_id=str(current_user.user_id),
        update_data=update_data
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or update failed"
        )

    return {
        "_id": str(task.task_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": str(task.user_id),
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user=Depends(get_current_user)):
    success = await TaskService.delete_task(
        task_id=task_id,
        user_id=str(current_user.user_id)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None
