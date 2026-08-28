# Models is a way for SQLAlchemy to map Python classes to database tables.
# Each class represents a table, and each attribute of the class represents
# a column in that table. This allows developers to interact with the
# database using Python objects instead of writing raw SQL queries.

# Models is a way for SQLAlchemy to be able to understand what kind of
# database tables we are going to be creating within our database in the
# future.

# A databse model is going to be the actual record that is inside a
# database table.

# A model is going to be a class that is going to represent a table in our
# database. Each model is going to have attributes that are going to
# represent the columns of the table.

# We are going to be creating this model for our database.py file.
from database import Base
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String)
    # phone_number: Mapped[str] = mapped_column(String)


class Todos(Base):
    __tablename__ = "todos"  # This specifies the name of the table in the database

    # This defines the 'id' column as an integer, primary key, and indexed
    # (and unique) for faster lookups
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    priority: Mapped[int] = mapped_column(Integer)
    # 0 = False, 1 = True in a Database.
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
