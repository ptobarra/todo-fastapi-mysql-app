from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlite:/// — tells SQLAlchemy to use SQLite as the database engine
# ./todo.db — creates/uses a database file named todo.db in the current directory

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:test1234!@localhost:5434/TodoApplicationDatabase"
)

# we don't check the same thread because SQLite is not designed for
# high-concurrency applications, and this setting allows multiple threads to
# access the database without raising an error. There could be multiple
# threads happening to our SQLite database.

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionmaker is a factory for creating new Session objects. It is
# configured with the engine and other options.

# Create a session factory configured with autocommit/autoflush disabled and
# bound to the database engine
# - autocommit=False: changes must be explicitly committed
# - autoflush=False: changes aren't auto-flushed to DB before queries
# We don't want the database transactions to do things automatically. We
# want to be in fully control of wahtever our database does in the future.
# - bind=engine: sessions created from this factory use our SQLite engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a class that our SQLAlchemy models will inherit from. It provides
# the necessary functionality for defining database tables and mapping them
# to Python classes.
# Base is an object of the database which is going to be able to control our
# database.
Base = declarative_base()

# postgresql database password = 'test1234!'

# (.venv) ptobarra@ptobarra-desktop-W11-20230518:~/projects/udemy-fastapi-books$
# $psql -h localhost -U postgres -d TodoApplicationDatabase -W
# Password:
# psql (16.14 (Ubuntu 16.14-0ubuntu0.24.04.1))
# SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
# Type "help" for help.

# TodoApplicationDatabase=# \dt
#          List of relations
#  Schema | Name  | Type  |  Owner
# --------+-------+-------+----------
#  public | todos | table | postgres
#  public | users | table | postgres
# (2 rows)

# TodoApplicationDatabase=#

# ---

# mysql 20260723
# --
# > mysql root username: root
# > mysql root password: test1234
# > user name: admin
# > role: DB Admin
# > password: test1234
