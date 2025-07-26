from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

class RequestBody(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "AI Content Generator using DeepSeek is online."}

@app.post("/generate")
def generate_content(request: RequestBody):
    prompt = f"Write a motivational, business, or fitness tip about: {request.topic}"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        if "choices" not in result:
            return {
                "error": "Unexpected response from DeepSeek",
                "raw_response": result
            }

        content = result["choices"][0]["message"]["content"].strip()
        return {"topic": request.topic, "content": content}

    except Exception as e:
        return {
            "error": str(e),
            "hint": "Check your DeepSeek API key or if the model is available."
        }
