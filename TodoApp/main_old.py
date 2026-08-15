from typing import Annotated

import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Path, status
from models import Todos
from pydantic import BaseModel, Field
from routers import auth
from sqlalchemy.orm import Session

app = FastAPI()

# For now, it is easier to delete our `todos.db` and hten recreate it if we
# add anything extra to our todos
# Alembic Section of Course will teach how to enhance DB without deleting
# each time.
models.Base.metadata.create_all(
    bind=engine
)  # This creates the database tables based on the models defined in models.py

app.include_router(auth.router)


def get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session.
    (rovide a SQLAlchemy database session for a request.)

    Yields:
        Session: An active DB session for the current request. (An active
        database session to be used by path operations.)

    Notes:
        - A new session is created per request/use. (Creates a new session
        when the dependency is invoked.)
        - The session is always closed in `finally`, even if an error
        occurs. (Always closes the session in the finally block.)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reusable type alias for injecting a DB session, so route signatures don't
# repeat the full Annotated[...] each time
db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    """
    Request body schema for creating or updating a Todo item.

    Attributes:
    title: Short todo title with a minimum length of 3 characters.
    description: Detailed text between 3 and 100 characters.
    priority: Integer priority level from 1 to 5.
    complete: Completion flag indicating whether the todo is done.
    """

    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# Depends is dependency injection (we've to do something before we execute
# what we're trying to execute)
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    # async def read_all(db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve all Todo items.

    Args:
    db: SQLAlchemy database session injected by FastAPI dependency.

    Returns:
    list[Todo]: A list of all Todo records in the database.
    """
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Retrieve a single Todo item by its ID.

    Args:
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_id: Integer ID of the Todo to fetch.

    Returns:
        The matching Todo record if found.

    Raises:
        HTTPException: 404 error when no Todo exists with the given ID.
    """
    # Uses dependency injection to get a database session (db).
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    """
    Create a new Todo item in the database.

    Args:
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_request: Validated request body containing the new Todo data.

    Returns:
        None. The Todo is persisted to the database and the endpoint responds
        with HTTP 201 Created.

    Notes:
        - FastAPI validates todo_request using the TodoRequest model before this
        function runs.
        - The request data is unpacked into a Todos ORM instance.
        - The new record is added to the session and committed to the database.
    """
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()

    # @app.post("/todo", status_code=status.HTTP_201_CREATED) registers a
    # POST endpoint at /todo and sets the success status to 201 Created.
    # todo_request: TodoRequest tells FastAPI to read the request body as
    # JSON and validate it against your TodoRequest Pydantic model.
    # Todos(**todo_request.dict()) converts the validated request data into
    # a SQLAlchemy Todos object.
    # db.add(todo_model) stages the new object to be inserted into the
    # database.
    # db.commit() permanently saves that new row to the database.


# in the function parameters TodoRequest objects must come before
# parameters with Path validation
@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    """
    Update an existing Todo item by its ID.

    Args:
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_id: Integer ID of the Todo to update.
        todo_request: Validated request body containing the updated Todo data.

    Returns:
        None. The Todo is updated in the database and the endpoint responds
        with HTTP 204 No Content.

    Raises:
        HTTPException: 404 error when no Todo exists with the given ID.

    Notes:
        - FastAPI validates todo_request before this function runs.
        - The existing database record is fetched first.
        - Each editable field is updated from the request body.
        - The changes are committed to the database.
    """
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    # db.add(todo_model) keeps the ORM object in the session, and
    # db.commit() saves the changes.
    db.add(todo_model)
    db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Delete an existing Todo item by its ID.

    Args:
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_id: Positive integer ID of the Todo to delete.

    Returns:
        None. The Todo is removed from the database and the endpoint responds
        with HTTP 204 No Content.

    Raises:
        HTTPException: 404 error when no Todo exists with the given ID.

    Notes:
        - The function first checks whether the Todo exists.
        - If found, the matching record is deleted and the transaction is committed.
    """
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()


# .venv/bin/activate
# cd TodoApp/
# uvicorn main:app --reload

# $ sudo apt install sqlite3
# $ which sqlite3
# $ sqlite3 --version
# $ sqlite3 todos.db
# (.venv) ptobarra@ptobarra-desktop-W11-20230518:~/projects/udemy-fastapi-books$ sqlite3
# sqlite> .open ./TodoApp/todos.db

# IN THE COMMAND PROMPT:
# C:\Users\ptoba>sqlite3
# SQLite version 3.53.3 2026-06-26 20:14:12
# Enter ".help" for usage hints.
# Connected to a transient in-memory database.
# Use ".open FILENAME" to reopen on a persistent database.
# sqlite> .quit

# C:\Users\ptoba>
