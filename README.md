# Task Management API

A RESTful API for managing tasks built with FastAPI and MongoDB.

## Features

- 🔐 User authentication with JWT
- ✅ CRUD operations for tasks
- 📝 Proper API documentation with Swagger UI
- 🐳 Containerized with Docker for easy deployment

## API Endpoints

### Authentication

- `POST /api/v1/auth/register`: Register a new user
- `POST /api/v1/auth/login`: Login and get JWT token

### Tasks

- `GET /api/v1/tasks`: Get all tasks for the authenticated user
- `POST /api/v1/tasks`: Create a new task
- `GET /api/v1/tasks/{task_id}`: Get a specific task by ID
- `PUT /api/v1/tasks/{task_id}`: Update a task by ID
- `DELETE /api/v1/tasks/{task_id}`: Delete a task by ID

## Tech Stack

- **FastAPI**: High-performance API framework
- **MongoDB**: NoSQL database
- **Motor**: Async MongoDB driver for Python
- **Python-Jose**: JWT token handling
- **Passlib**: Password hashing
- **Docker**: Containerization
- **Pydantic**: Data validation and settings management

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized setup)
- MongoDB URI

### Setup & Installation

1. **Clone the repository**

```bash
git clone https://github.com/venkat2305/task-manager.git
cd task-manager
```

2. **Create environment file**

```bash
cp .env.example .env
```

Edit the `.env` file with your own values.

3. **Run with Docker (recommended)**

```bash
docker-compose up -d
```

This will start both the API and MongoDB containers.

### Run Locally with Virtual Environment

1. **Create and activate a virtual environment**

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux
source venv/bin/activate
# On Windows
# venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip3 install -r requirements.txt
```

3. **Run the application**

```bash
uvicorn app.main:app --reload
```

### API Documentation

After starting the application, access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

This API is deployed on Render and can be accessed at:

`https://task-manager-ak90.onrender.com`

## Postman Collection

A Postman collection with all API endpoints and example requests is available online.

Access the Postman workspace at:
[Task Manager API Collection](https://www.postman.com/joint-operations-architect-96410091/task-manager/collection/mb0c026/task-manager?action=share&creator=38049202)