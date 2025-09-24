from fastapi import FastAPI, Body 
from langdetect import detect
from analyze import text_analyze_chn, text_analyze_eng
from google import genai

app = FastAPI() #creating FastAPI application obj ("server")
client = genai.client

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
    if lang == "en":
        prompt = text_analyze_eng(text)
    elif lang == "zh-cn":
        prompt = text_analyze_chn(text)
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    return {"language": lang, "analysis": response.text}
