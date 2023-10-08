from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

# switch between SQLite and Postgres
is_using_sqlite = True

if is_using_sqlite:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app/database/snapidb.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Password01@localhost:5432/snapidb"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
