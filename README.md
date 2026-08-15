# Todo FastAPI MySQL App

Updated todo list FastAPI Todo app built while learning from **FastAPI - The Complete Course 2026 (Beginner + Advanced)** on Udemy. Includes MySQL integration, SQLAlchemy, authentication, user management, and REST API development for a task tracking application.

## Features

- **JWT authentication** — register, log in, and receive an OAuth2 bearer token (`/auth`)
- **Per-user todos** — authenticated users can create, read, update, and delete their own todo items
- **User management** — view your profile and change your password (`/user`)
- **Admin endpoints** — role-restricted access to view and delete any user's todos (`/admin`)
- **SQLAlchemy ORM models** for `Users` and `Todos`, with a `Todos.owner_id` relationship
- **Password hashing** with `passlib`/`bcrypt`; database-backed via SQLAlchemy, with MySQL as the target database (SQLite/PostgreSQL also usable during development)

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- MySQL (via `PyMySQL`) — SQLite and PostgreSQL supported as alternate backends
- [python-jose](https://github.com/mpdavis/python-jose) for JWT tokens
- [passlib](https://passlib.readthedocs.io/) + `bcrypt` for password hashing
- [Pydantic](https://docs.pydantic.dev/) for request/response validation
- [Uvicorn](https://www.uvicorn.org/) ASGI server
- [Ruff](https://docs.astral.sh/ruff/) for linting/formatting
- [pytest](https://docs.pytest.org/) for testing

## Project Structure

```
.
├── TodoApp/
│   ├── main.py            # FastAPI app entrypoint, router registration
│   ├── database.py        # SQLAlchemy engine/session config
│   ├── models.py          # Users and Todos ORM models
│   └── routers/
│       ├── auth.py        # Registration, login, JWT issuance
│       ├── todos.py       # CRUD endpoints for the authenticated user's todos
│       ├── admin.py       # Admin-only endpoints
│       └── users.py       # Profile and password management
├── books.py / books2.py   # Standalone in-memory Books API exercises from the course
├── pyproject.toml         # Ruff configuration
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.11+
- A MySQL server (or adjust `TodoApp/database.py` to point at SQLite/PostgreSQL instead)

### Setup

```bash
# Clone the repo
git clone https://github.com/ptobarra/todo-fastapi-mysql-app.git
cd todo-fastapi-mysql-app

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure the database

Update the `SQLALCHEMY_DATABASE_URL` in [TodoApp/database.py](TodoApp/database.py) with your own database credentials, e.g.:

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://<user>:<password>@localhost:3306/<database>"
```

### Run the app

```bash
cd TodoApp
uvicorn main:app --reload
```

Tables are created automatically on startup. The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## API Overview

| Method | Endpoint             | Description                          | Auth required |
|--------|-----------------------|---------------------------------------|----------------|
| POST   | `/auth/`               | Register a new user                   | No             |
| POST   | `/auth/token`           | Log in and receive a JWT bearer token | No             |
| GET    | `/`                     | List the current user's todos         | Yes            |
| GET    | `/todo/{todo_id}`       | Get a single todo                     | Yes            |
| POST   | `/todo`                 | Create a todo                         | Yes            |
| PUT    | `/todo/{todo_id}`       | Update a todo                         | Yes            |
| DELETE | `/todo/{todo_id}`       | Delete a todo                         | Yes            |
| GET    | `/user/`                | View the current user's profile       | Yes            |
| PUT    | `/user/password`        | Change the current user's password    | Yes            |
| GET    | `/admin/todo`           | List all users' todos                 | Admin only     |
| DELETE | `/admin/todo/{todo_id}` | Delete any user's todo                | Admin only     |

## Linting

```bash
ruff check .
ruff format .
```

## Acknowledgements

Built while following **FastAPI - The Complete Course 2026 (Beginner + Advanced)** on Udemy.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
