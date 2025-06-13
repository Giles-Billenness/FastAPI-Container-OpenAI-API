# FastAPI Container OpenAI API

This project provides a FastAPI-based API and a conversational barista chatbot demo using OpenAI's function calling and tool use. You can run the API in a Docker container or interact with the barista assistant in the terminal.

## Features

- **OpenAI API integration**: Use GPT-4 function calling for tool-augmented conversations.
- **Barista chatbot**: Chat with an AI barista that can search a coffee menu, check the weather, and place orders.
- **Tool calling**: The assistant can automatically invoke Python functions for menu search, weather lookup, and order placement.
- **FastAPI endpoints**: Expose OpenAI-powered endpoints for text generation and code assistance.
- **Docker support**: Easily build and run the API in a containerized environment.

## Quickstart

### 1. Clone the repository

```sh
git clone https://github.com/Giles-Billenness/FastAPI-Container-OpenAI-API.git
cd FastAPI-Contrainer-OpenAI-API
```

### 2. Set up your environment

- Create a `.env` file with your OpenAI API key:

  ```env
  OPENAI_API_KEY=sk-...
  ```

- (Optional) Create a virtual environment and install dependencies:

  ```sh
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  pip install -r requirements.txt  # or use pyproject.toml with pip, uv, or poetry
  ```

### 3. Run the Barista Chatbot in the Terminal

```sh
uv run barrista.py
```

- Interact with the assistant in natural language.
- The assistant can search the menu, check the weather, and place coffee orders using function calling.

### 4. Run the FastAPI Server (for API endpoints)

```sh
uv run fastapi dev main.py
```

- Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

### 5. Docker Usage

#### Build the Docker image

```sh
docker build -t fastapi-openai .
```

#### Run the Docker container

```sh
docker run --env-file .env -p 8000:8000 fastapi-openai
```

- The `--env-file .env` flag loads your OpenAI API key.
- The `-p 8000:8000` flag maps port 8000 to your machine.
- Access the API at [http://localhost:8000](http://localhost:8000).

## Example Conversation

```
You: hello whats the weather like in london?
Barista: Right now in London, it's 16°C and cloudy. This kind of weather is cool and a bit overcast—perfect for a comforting hot drink, like a classic latte or maybe a cozy cappuccino.

You: id like a coffee with foam
Barista: Here are two coffees with foam: Cappuccino and Flat White. Would you like to order one?

You: please order me a cappuccino
Barista: Your cappuccino order has been placed! Enjoy!

You: bye
Barista: Goodbye! Have a great day!
```

## Project Structure

- `main.py` — FastAPI endpoints and OpenAI integration
- `barrista.py` — Terminal-based barista chatbot demo
- `instructions.py` — System prompts and workflow instructions
- `Dockerfile` — Container build instructions
- `.env` — Your OpenAI API key (not committed)
- `README.md` — This file

## Requirements

- Python 3.12+
- OpenAI API key
- (Optional) Docker

## License

MIT
