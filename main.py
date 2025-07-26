from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Configure the new OpenAI client (v1.0+)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class RequestBody(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "AI Content Generator is online."}

@app.post("/generate")
def generate_content(request: RequestBody):
    prompt = f"Write a motivational, business, or fitness tip about: {request.topic}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        content = response.choices[0].message.content.strip()
        return {"topic": request.topic, "content": content}
    
    except Exception as e:
        return {
            "error": str(e),
            "hint": "Check if your OPENAI_API_KEY is set correctly in Render."
        }
