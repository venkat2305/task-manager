from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, tasks
from .config import settings
from .utils.database import Database

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Task management Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix=settings.API_V1_PREFIX)

# Routes
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(tasks.router, prefix="/tasks")

app.include_router(api_router)


@app.on_event("startup")
async def startup_db_client():
    await Database.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await Database.close()


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Task Management API",
    }
