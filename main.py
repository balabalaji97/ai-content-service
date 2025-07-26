from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/cinematika-7b"  # ✅ Confirmed working model

class RequestBody(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "AI Content Generator using OpenRouter is online."}

@app.post("/generate")
def generate_content(request: RequestBody):
    prompt = f"Write a motivational, business, or fitness tip about: {request.topic}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",  # Required, can be any domain
        "X-Title": "AI Content Generator"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        if "choices" not in result:
            return {
                "error": "Unexpected response from OpenRouter",
                "raw_response": result
            }

        content = result["choices"][0]["message"]["content"].strip()
        return {"topic": request.topic, "content": content}

    except Exception as e:
        return {
            "error": str(e),
            "hint": "Check if OPENROUTER_API_KEY is valid and model is correct."
        }
