# FastAPI Contrainer OpenAI API

uv run fastapi dev main.py

1. Build the Docker image:
`docker build -t fastapi-openai .`

2. Run the Docker container:
`docker run --env-file .env -p 8000:8000 fastapi-openai`

The --env-file .env flag loads your OpenAI API key from the .env file.
The -p 8000:8000 flag maps port 8000 on your machine to the container.

You can then access your API at <http://localhost:8000>.
