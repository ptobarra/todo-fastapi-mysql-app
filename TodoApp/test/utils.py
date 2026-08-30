from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session.
    (provide a SQLAlchemy database session for a request.)

    Yields:
        Session: An active DB session for the current request. (An active
        database session to be used by path operations.)

    Notes:
        - A new session is created per request/use. (Creates a new session
        when the dependency is invoked.)
        - The session is always closed in `finally`, even if an error
        occurs. (Always closes the session in the finally block.)
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "codingwithrobytest", "id": 1, "user_role": "admin"}


client = TestClient(app)
