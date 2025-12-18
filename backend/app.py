import spacy
from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from langdetect import detect
from analyze import text_analyze_chn, text_analyze_eng
from google import genai
import os
from dotenv import load_dotenv

# DB:
from fastapi import Depends, HTTPException, Header
from sqlmodel import Session, select
from typing import Annotated
from typing import List # helper to display all users & records

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
app = FastAPI() #creating FastAPI application "server"
client = genai.Client(api_key=api_key)
nlp_en = None
nlp_cn = None

# entry point for web app

# FastAPI automates the conversion of Python objects into JSON;
# The response model handles the translation.
# Sessions are temporary single-user-request staging tables between the user and the db
# Depends(get_session) is a Dependency Injection that ensures everytime a user hits the API 
# they get a fresh clean Session with no data conflicts.
# Tags are purely for Documentation Organization (grouped together under their headers).

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Handle rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Please try again later."}
    )

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # during dev allow all; in prod restrict to site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- IMPORT FROM BACKEND MODULE ---
from backend.database.models import (
    User, AnalysisRecord, 
    create_db_and_tables, get_session, engine
)

# Dependency for Database Session
SessionDep = Annotated[Session, Depends(get_session)]

# Creates the Database Tables when the application starts
# probably use a migration script that runs before app is started for production
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Dependency for Mock Auth ("Login")
def get_current_user(
    session: SessionDep, 
    x_user_id: int = Header(...) # Tells FastAPI this header is Required
) -> User:
    
    user = session.get(User, x_user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid User ID")
    return user


# New Endpoints:

@app.post("/users/", tags=["Database"])
def create_user(user: User, session: SessionDep) -> User:
    # same Pydantic model type annotations can be used,
    # i.e. type User can be read directly from JSON body
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Manual override for creating record; automated creation is in the /analyze_text endpoint
@app.post("/records/", response_model=AnalysisRecord, tags=["Database"])
def create_record(record: AnalysisRecord, session: SessionDep) -> AnalysisRecord:
    user_id = record.owner_id
    # manual check to prevent integrity errors 
    # since SQLite foreign keys aren't strictly enforced by default
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User in record not found")

    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@app.get("/records/{record_id}", response_model=AnalysisRecord, tags=["Database"])
def read_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    record = session.get(AnalysisRecord, record_id)
    # Check record existence
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    # Fix IDOR vulnerability by checking ownership (authorization)
    if(current_user.id != record.owner_id):
        raise HTTPException(status_code=403, detail="Not authorized to access this record")
   
    return record

# Helper endpoint to see everyone in the DB
@app.get("/debug/db", tags=["Debug"])
def read_all_data(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    records = session.exec(select(AnalysisRecord)).all()
    return {"users": users, "records": records}

# Basic Root Endpoint

@app.get("/")
async def root():
    return {"message": "T3xtAnlys API is up and *running*!"}

@app.post("/analyze")
@limiter.limit("30/minute;500/day")
async def analyze_text(
    request: Request, 
    payload: dict = Body(...),
    session = Depends(get_session)):
    text = payload.get("text", "")
    if not text.strip():
        return {"error": "No text provided."}
    lang = detect(text)

    # 1. Cache check
    existing_record = session.exec(
        select(AnalysisRecord).where(AnalysisRecord.input == text)
    ).first()
    if existing_record:
        return {"language": lang, "analysis": existing_record.output}
    
    # 2. Cache not hit scenario - analyze
    print(text)
    if lang == "en":
        global nlp_en
        if not nlp_en:
            nlp_en = spacy.load("en_core_web_sm")
        prompt = text_analyze_eng(text, nlp_en)
        nlp_en = None
    elif lang == "zh-cn":
        global nlp_cn
        if not nlp_cn:
            nlp_cn = spacy.load("zh_core_web_sm")
        prompt = text_analyze_chn(text, nlp_cn)
        nlp_cn = None
    else:
        return {"error": f"Unsupported language detected: {lang}"}
    
    try:
        print("Gemini request sent")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        return {"error": f"AI generation failed: {str(e)}"}
    
    print("Gemini response received")
    
    # 3. Save new AnalysisRecord to DB
    new_record = AnalysisRecord(input=text, output=response.text, owner_id=1) #TODO: owner_id is now default =1 for testing
    session.add(new_record)
    session.commit()
    print("New analysis cached")
    return {"language": lang, "analysis": response.text}
