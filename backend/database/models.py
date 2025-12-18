from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# FastAPI & SQL tutorial: 
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-app-with-a-single-model

# Creating Database models
class User(SQLModel, table=True): # represents a table in the db, not just a data model
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    # age: int | None = Field(default=None, index=True)
    # secret_name: str

class AnalysisRecord(SQLModel, table=True):
    # "Child" table
    id: int | None = Field(default=None, primary_key=True)
    # !! we link this record to a specific user
    owner_id: int = Field(foreign_key="user.id") # enforces that this number must exist in the User table
    
    input: str = Field(index=True) # input text, index created by SQLModel for faster lookups
    output: str = Field(index=True) # output text, indexed

# Creating an Engine (holds connection to the db)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Allows FastAPI to use the same SQLite db in different threads,
# necessary because one request could use more than one thread (e.g. dependencies)
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Creating the Tables
def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine) # create tables for all table models

# Creating session dependency
def get_session():
    with Session(engine) as session:
        yield session 
        # creates FastAPI dependency with yield that provides new session for each request,
        # ensures we use a single session per request