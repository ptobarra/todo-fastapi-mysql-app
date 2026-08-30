# import models
from fastapi import FastAPI

# from database import engine
from .database import engine
from .models import Base

# from routers import admin, auth, todos, users
from .routers import admin, auth, todos, users

app = FastAPI()

# For now, it is easier to delete our `todos.db` and then recreate it if we
# add anything extra to our todos
# Alembic Section of Course will teach how to enhance DB without deleting
# each time.
# models.Base.metadata.create_all(
#     bind=engine
# )  # This creates the database tables based on the models defined in models.py

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# .venv/bin/activate
# cd TodoApp/
# uvicorn main:app --reload
# now to execute from the root folder
# uvicorn TodoApp.main:app --reload

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
