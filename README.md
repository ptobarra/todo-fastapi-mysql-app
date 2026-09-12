# Todo FastAPI MySQL App

Updated todo list FastAPI Todo app built while learning from **FastAPI - The Complete Course 2026 (Beginner + Advanced)** on Udemy. Includes MySQL integration, SQLAlchemy, authentication, user management, and REST API development for a task tracking application.

## Features

- **JWT authentication** — register, log in, and receive an OAuth2 bearer token (`/auth`)
- **Per-user todos** — authenticated users can create, read, update, and delete their own todo items (`/todos`)
- **Server-rendered web UI** — Jinja2 + Bootstrap pages for login, registration, and listing/adding/editing todos, backed by a cookie-stored JWT (`access_token`)
- **User management** — view your profile, change your password, and update your phone number (`/user`)
- **Admin endpoints** — role-restricted access to view and delete any user's todos (`/admin`)
- **SQLAlchemy ORM models** for `Users` and `Todos`, with a `Todos.owner_id` relationship
- **Password hashing** with `passlib`/`bcrypt`; database-backed via SQLAlchemy, with MySQL as the target database (SQLite/PostgreSQL also usable during development)
- **Alembic migrations** — schema changes are tracked as versioned migration scripts instead of relying on `create_all`
- **Health check** endpoint (`/healthy`)
- **Test suite** — unit and integration tests (`pytest`) covering auth, todos, users, and admin routes against an isolated SQLite test database

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- [Alembic](https://alembic.sqlalchemy.org/) for database migrations
- MySQL (via `PyMySQL`) — SQLite and PostgreSQL supported as alternate backends
- [python-jose](https://github.com/mpdavis/python-jose) for JWT tokens
- [passlib](https://passlib.readthedocs.io/) + `bcrypt` for password hashing
- [Pydantic](https://docs.pydantic.dev/) for request/response validation
- [Uvicorn](https://www.uvicorn.org/) ASGI server
- [Ruff](https://docs.astral.sh/ruff/) for linting/formatting
- [pytest](https://docs.pytest.org/) + [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) for testing

## Project Structure

```
.
├── TodoApp/
│   ├── main.py             # FastAPI app entrypoint, router registration
│   ├── database.py         # SQLAlchemy engine/session config
│   ├── models.py           # Users and Todos ORM models
│   ├── alembic.ini         # Alembic configuration
│   ├── alembic/
│   │   ├── env.py          # Alembic migration environment
│   │   └── versions/       # Versioned migration scripts
│   ├── routers/
│   │   ├── auth.py         # Registration, login, JWT issuance, login/register pages
│   │   ├── todos.py        # CRUD endpoints + pages for the authenticated user's todos (prefix `/todos`)
│   │   ├── admin.py        # Admin-only endpoints
│   │   └── users.py        # Profile, password, and phone number management
│   ├── templates/          # Jinja2 templates for the server-rendered web UI
│   │   ├── layout.html     # Base layout (navbar, Bootstrap/jQuery includes)
│   │   ├── navbar.html
│   │   ├── login.html / register.html
│   │   ├── todo.html       # Todo list page
│   │   └── add-todo.html / edit-todo.html
│   ├── static/             # CSS/JS served at `/static` (Bootstrap, jQuery, popper, custom `base.js`)
│   │   ├── css/
│   │   └── js/
│   └── test/
│       ├── conftest.py     # Shared pytest fixtures (test_todo, test_user)
│       ├── utils.py        # Test database/session setup and dependency overrides
│       ├── test_auth.py
│       ├── test_todos.py
│       ├── test_users.py
│       └── test_admin.py
├── books.py / books2.py    # Standalone in-memory Books API exercises from the course
├── pyproject.toml          # Ruff and pytest configuration
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.12+
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

### Run database migrations

The app targets a MySQL database managed via Alembic (`TodoApp/alembic.ini`, pointed at the URL under `sqlalchemy.url`). From the `TodoApp/` directory:

```bash
cd TodoApp
alembic upgrade head
```

To generate a new migration after changing a model in `models.py`:

```bash
alembic revision --autogenerate -m "describe the change"
```

### Run the app

The app is structured as a package (`TodoApp`) using relative imports, so run it from the **repo root**, not from inside `TodoApp/`:

```bash
uvicorn TodoApp.main:app --reload
```

Tables are also created automatically on startup via `Base.metadata.create_all`, but for schema changes prefer the Alembic migration above. The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`. Visiting `/` redirects to the todo list page (`/todos/todo-page`).

## Web UI

Alongside the JSON API, the app serves a small server-rendered UI (Jinja2 templates in `TodoApp/templates/`, styled with Bootstrap, assets served from `/static`):

| Page                              | Description                                   |
|------------------------------------|------------------------------------------------|
| `/auth/register-page`              | Registration form                              |
| `/auth/login-page`                 | Login form                                     |
| `/todos/todo-page`                 | List the current user's todos                  |
| `/todos/add-todo-page`             | Form to create a new todo                      |
| `/todos/edit-todo-page/{todo_id}`  | Form to edit/delete an existing todo           |

The login page posts credentials to `/auth/token` and stores the returned JWT in an `access_token` cookie; the page routes above read that cookie server-side (redirecting to `/auth/login-page` if it's missing or invalid), while the page's own JavaScript (`static/js/base.js`) sends it as an `Authorization: Bearer` header when calling the JSON API to create/update/delete todos. Logging out clears the cookie client-side.

## API Overview

| Method | Endpoint                | Description                            | Auth required |
|--------|--------------------------|-----------------------------------------|----------------|
| GET    | `/healthy`               | Health check                            | No             |
| POST   | `/auth/`                 | Register a new user                     | No             |
| POST   | `/auth/token`             | Log in and receive a JWT bearer token   | No             |
| GET    | `/todos/`                 | List the current user's todos           | Yes            |
| GET    | `/todos/todo/{todo_id}`   | Get a single todo                       | Yes            |
| POST   | `/todos/todo`             | Create a todo                           | Yes            |
| PUT    | `/todos/todo/{todo_id}`   | Update a todo                           | Yes            |
| DELETE | `/todos/todo/{todo_id}`   | Delete a todo                           | Yes            |
| GET    | `/user/`                  | View the current user's profile         | Yes            |
| PUT    | `/user/password`          | Change the current user's password      | Yes            |
| PUT    | `/user/phonenumber`       | Change the current user's phone number  | Yes            |
| GET    | `/admin/todo`             | List all users' todos                   | Admin only     |
| DELETE | `/admin/todo/{todo_id}`   | Delete any user's todo                  | Admin only     |

## Testing

```bash
pytest
```

Tests run against an isolated SQLite database (`TodoApp/test/utils.py`) with the `get_db`/`get_current_user` dependencies overridden, so they don't touch the real MySQL database.

## Linting

```bash
ruff check .
ruff format .
```

## Acknowledgements

Built while following **FastAPI - The Complete Course 2026 (Beginner + Advanced)** on Udemy.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
