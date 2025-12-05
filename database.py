# backend/database.py
"""
This module handles database connections for the Virtual Event Assistant.
It uses SQLite (file-based) via SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Path to the database file (stored in backend/data/)
db_path = os.path.join(os.path.dirname(__file__), "data", "event_assistant.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

# Create SQLAlchemy engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
