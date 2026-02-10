# FastAPI CRUD API with Authentication

A FastAPI project that provides CRUD endpoints for users, tasks, and tags, with JWT-based authentication and MySQL persistence via SQLAlchemy and Alembic.

## Features
- User CRUD
- Task CRUD
- Tag CRUD
- JWT login and protected task endpoints
- MySQL + SQLAlchemy ORM
- Alembic migrations

## Tech Stack
- FastAPI
- SQLAlchemy
- Alembic
- MySQL (PyMySQL)
- Pydantic
- JWT (python-jose)
- Uvicorn

## Project Structure
- `main.py` FastAPI app and router registration
- `tables.py` SQLAlchemy models
- `schemas.py` Pydantic schemas
- `connection.py` DB engine/session
- `oauth2.py` JWT helpers and auth dependency
- `routers/` API routes for users, tasks, tags, auth
- `migration/` Alembic migrations

## Setup
1. Create and activate a virtual environment.
2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root.

```env
# Database
USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=3306
DB_NAME=your_db_name

# App
APP_HOST=127.0.0.1
APP_PORT=8000

# Auth
SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TIME=30
```

## Database Migrations
Initialize the DB schema:

```bash
alembic upgrade head
```

Create a new migration (autogenerate):

```bash
alembic revision --autogenerate -m "your message"
```

## Run the Server
```bash
python main.py
```

The API will be available at:
- `http://<APP_HOST>:<APP_PORT>/api`

Swagger UI:
- `http://<APP_HOST>:<APP_PORT>/docs`

## API Overview
Auth:
- `POST /login`

Users:
- `POST /users/`
- `GET /users/all`
- `GET /users/{id}`
- `PATCH /users/{id}`
- `DELETE /users/{id}`

Tasks:
- `POST /tasks/` (requires auth)
- `GET /tasks/all`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}` (requires auth)
- `DELETE /tasks/{id}` (requires auth)

Tags:
- `POST /tags/`
- `GET /tags/all`
- `GET /tags/{id}`
- `PATCH /tags/{id}`
- `DELETE /tags/{id}`

## Authentication
Login returns a JWT token.
Provide it in the `Authorization` header:

```
Authorization: Bearer <token>
```
