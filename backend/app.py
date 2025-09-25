from fastapi import FastAPI, Body 
from langdetect import detect
from analyze import text_analyze_chn, text_analyze_eng
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
app = FastAPI() #creating FastAPI application obj ("server")
client = genai.Client(api_key=api_key)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # during dev allow all; in prod restrict to your site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "T3xtAnlys API is up and *running*!"}

@app.post("/analyze")
async def analyze_text(payload: dict = Body(...)):
    text = payload.get("text", "")
    if not text.strip():
        return {"error": "No text provided."}
        # in case of empty input, return error instead of sending it to GenAI
    
    lang = detect(text)
    print(text)
    if lang == "en":
        prompt = text_analyze_eng(text)
    elif lang == "zh-cn":
        prompt = text_analyze_chn(text)
    else:
        return {"error": f"Unsupported language detected: {lang}"}
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        return {"error": f"AI generation failed: {str(e)}"}
    return {"language": lang, "analysis": response.text}
