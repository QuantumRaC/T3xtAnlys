from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# FastAPI & SQL tutorial: 
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-app-with-a-single-model
# Local testing at:
# http://127.0.0.1:8000/docs#/

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

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# Creates the Database Tables when the application starts
# probably use a migration script that runs before app is started for production
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    # same Pydantic model type annotations can be used,
    # i.e. type User can be read directly from JSON body
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/records/", response_model=AnalysisRecord)
def create_record(record: AnalysisRecord, session: SessionDep) -> AnalysisRecord:
    user_id = record.owner_id
    # manual check to prevent integrity errors
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User in record not found")

    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
