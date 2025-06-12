from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()# Load environment variables from .env file

app = FastAPI()

class OpenAIRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 100

@app.post("/openai/generate")
def generate_text(request: OpenAIRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not set.")
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")# test endpoint
def hello():
    api_key = os.getenv("OPENAI_API_KEY")
    return {"message": f"Hello, FastAPI! OpenAI API key is set. {api_key}" if api_key else "Hello, FastAPI! OpenAI API key is not set."}


def main():
    print("Hello from fastapi-contrainer-openai-api!")


if __name__ == "__main__":
    main()
