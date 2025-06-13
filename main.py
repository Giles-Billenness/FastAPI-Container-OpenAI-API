from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

from instructions import SYS_PROMPT_SWEBENCH, python_bash_patch_tool, STARTER_PROMPT

load_dotenv()# Load environment variables from .env file

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class OpenAIRequest(BaseModel):
    prompt: str
    # model: str = "gpt-3.5-turbo"
    # max_tokens: int = 100

@app.post("/openai/generate")
def generate_text(request: OpenAIRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/openai/instruction")
def generate_instruction(request: OpenAIRequest):
    try:
        response = client.responses.create(
            instructions=SYS_PROMPT_SWEBENCH,
            model="gpt-4.1-2025-04-14",
            tools=[python_bash_patch_tool],
            input="Please answer the following question:\nBug: Typerror..."
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

code_snippet = """
Im getting this error when trying to build the docker image with the command: docker build -t fastapi-openai .
ERROR: error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
"""

@app.get("/openai/code")
def generate_response_get():
    try:
        response = client.responses.create(
            instructions=STARTER_PROMPT,
            model="gpt-4.1-2025-04-14",
            input=code_snippet
        )
        return {"response": response.output_text} #will give {"response": "..." }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/openai/codePost")
def generate_response_post(request: OpenAIRequest):
    try:
        response = client.responses.create(
            instructions=STARTER_PROMPT,
            model="gpt-4.1-2025-04-14",
            input=request.prompt
        )
        return {"response": response.output_text} #will give {"response": "..." }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#do a post request to /openai/codePost with raw json body {"prompt": "your code snippet here"} not query params


@app.get("/")# test endpoint
def hello():
    api_key = os.getenv("OPENAI_API_KEY")
    return {"message": f"Hello, FastAPI! OpenAI API key is set. {api_key}" if api_key else "Hello, FastAPI! OpenAI API key is not set."}


def main():
    print("Hello from fastapi-Container-openai-api!")


if __name__ == "__main__":
    main()
