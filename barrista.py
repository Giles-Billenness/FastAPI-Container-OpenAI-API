from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json


load_dotenv()# Load environment variables from .env file

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class OpenAIRequest(BaseModel):
    prompt: str

# uv run barrista.py

Example_use = """
    Welcome to the Barista Chatbot! Type 'bye' to exit.
    You: hello whats the weather like in london?
    Barista: Right now in London, it's 16°C and cloudy. This kind of weather is cool and a bit overcast—perfect for a comforting hot drink, like a classic latte or maybe a cozy cappuccino.

    If you’d like, I can also recommend some specific coffee or tea options that pair well with the current weather. Would you like suggestions or to see the menu?
    You: id like a coffee with foam
    Barista: Great choice! Here are two coffees with foam that you might enjoy:

    1. Cappuccino – Espresso with steamed milk and a generous layer of foam. This is a classic, cozy option, especially on a cloudy day.
    2. Flat White – Velvety espresso with microfoam milk, giving it a creamy texture and smooth taste.

    Would you like to order one of these, or would you like more details about either option?
    You: please order me a cappuccino
    Order placed: Cappuccino (id: 2) for $3.0
    Barista: Your cappuccino order has been placed! You’ll soon have a delicious espresso with steamed milk and foam, perfect for the cloudy London weather.

    If you’d like something to go with your coffee—like a pastry or snack—just let me know. Otherwise, enjoy your cappuccino, and feel free to ask if you need anything else!
    You: bye
    Barista: Goodbye! Have a great day!
    """

# --- Toy Barista Chatbot Data and Tools ---
# Fake coffee menu database
COFFEE_MENU = [
    {
        "id": 1,
        "name": "Espresso",
        "description": "Strong and bold espresso shot.",
        "price": 2.5,
        "popularity": 90,
        "allergens": []
    },
    {
        "id": 2,
        "name": "Cappuccino",
        "description": "Espresso with steamed milk and foam.",
        "price": 3.0,
        "popularity": 85,
        "allergens": ["milk"]
    },
    {
        "id": 3,
        "name": "Latte",
        "description": "Smooth espresso with lots of steamed milk.",
        "price": 3.5,
        "popularity": 80,
        "allergens": ["milk"]
    },
    {
        "id": 4,
        "name": "Mocha",
        "description": "Espresso with chocolate and steamed milk.",
        "price": 4.0,
        "popularity": 75,
        "allergens": ["milk", "soy"]
    },
    {
        "id": 5,
        "name": "Americano",
        "description": "Espresso with hot water for a lighter taste.",
        "price": 2.8,
        "popularity": 70,
        "allergens": []
    },
    {
        "id": 6,
        "name": "Flat White",
        "description": "Velvety espresso with microfoam milk.",
        "price": 3.2,
        "popularity": 65,
        "allergens": ["milk"]
    },
    {
        "id": 7,
        "name": "Iced Coffee",
        "description": "Chilled coffee served over ice.",
        "price": 3.0,
        "popularity": 60,
        "allergens": []
    },
    {
        "id": 8,
        "name": "Caramel Macchiato",
        "description": "Espresso, steamed milk, and caramel drizzle.",
        "price": 4.2,
        "popularity": 78,
        "allergens": ["milk"]
    }
]

# Fake weather database
WEATHER_DATA = {
    "london": {"temperature": 16, "condition": "cloudy"},
    "new york": {"temperature": 22, "condition": "sunny"},
    "paris": {"temperature": 18, "condition": "rainy"},
    "tokyo": {"temperature": 20, "condition": "clear"},
    "sydney": {"temperature": 25, "condition": "sunny"},
}

def search_items(query_string: str) -> List[Dict[str, Any]]:
    """Search the coffee menu for items matching the query string (case-insensitive word match)."""
    query = query_string.lower()
    results = []
    for item in COFFEE_MENU:
        if query in item["name"].lower() or query in item["description"].lower():
            results.append(item)
    return results

def get_weather(city: str) -> Dict[str, Any]:
    """Return the preset weather for a given city (case-insensitive)."""
    return WEATHER_DATA.get(city.lower(), {"temperature": None, "condition": "unknown"})

def order_item(item_id: int) -> str:
    """Simulate ordering a coffee item by id. Prints to console and returns a confirmation string."""
    item = next((i for i in COFFEE_MENU if i["id"] == item_id), None)
    if item:
        msg = f"Order placed: {item['name']} (id: {item['id']}) for ${item['price']}"
        print(msg)
        return msg
    else:
        return f"Item with id {item_id} not found."

# --- Barista Chatbot API Endpoints ---

class SearchRequest(BaseModel):
    query: str

class WeatherRequest(BaseModel):
    city: str

class OrderRequest(BaseModel):
    item_id: int

@app.post("/barista/search")
def barista_search(request: SearchRequest):
    results = search_items(request.query)
    return {"results": results}

@app.post("/barista/weather")
def barista_weather(request: WeatherRequest):
    weather = get_weather(request.city)
    return {"weather": weather}

@app.post("/barista/order")
def barista_order(request: OrderRequest):
    confirmation = order_item(request.item_id)
    return {"confirmation": confirmation}

# --- Barista Chatbot Tool Specs for OpenAI Function Calling ---
barista_tools = [
    {
        "type": "function",
        "name": "search_items",
        "description": "Search the coffee menu for items matching the query string.",
        "parameters": {
            "type": "object",
            "properties": {
                "query_string": {"type": "string", "description": "The search term for coffee menu items."}
            },
            "required": ["query_string"]
        }
    },
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the preset weather for a given city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to get weather for."}
            },
            "required": ["city"]
        }
    },
    {
        "type": "function",
        "name": "order_item",
        "description": "Order a coffee item by its id.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {"type": "integer", "description": "The id of the coffee item to order."}
            },
            "required": ["item_id"]
        }
    }
]

barista_prompt = """
        You are a helpful conversational barista assistant. Take in the users input and respond with helpful recommendations about available coffee, local weather if requested (changing recommendations if needed), and ordering.
        Use the available tools to help the user order coffee, check the menu, and get weather info. Use tools when factual information is needed, such as searching for coffee items, getting weather data or when actions need to be taken like ordering an item.
        Your thinking should be thorough and so it's fine if it's very long. You can think step by step before and after each action you decide to take.
        """

def main():
    print("Welcome to the Barista Chatbot! Type 'bye' to exit.")
    # user_name = input("What's your name? ")
    # print(f"Hello, {user_name}! How can I help you with your coffee order today?")
    messages = [
        {"role": "system", "content": barista_prompt}
    ]
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "bye" or user_input == "":
            print("Barista: Goodbye! Have a great day!")
            break
        while messages and messages[-1].get("type") == "function_call_output":
            messages.pop()
        messages.append({"role": "user", "content": user_input})
        response = client.responses.create(
            model="gpt-4.1-2025-04-14",
            input=messages,
            tools=barista_tools,
            tool_choice="auto"
        )
        assistant_reply = response.output_text
        function_calls = response.output if hasattr(response, "output") and isinstance(response.output, list) else []
        if function_calls:
            for function_call in function_calls:
                tool_name = getattr(function_call, "name", None)
                args = json.loads(function_call.arguments)
                if tool_name == "search_items":
                    tool_result = search_items(args["query_string"])
                elif tool_name == "get_weather":
                    tool_result = get_weather(args["city"])
                elif tool_name == "order_item":
                    tool_result = order_item(args["item_id"])
                else:
                    tool_result = "Unknown tool."
                messages.append({
                    "type": "function_call",
                    "name": function_call.name,
                    "arguments": function_call.arguments,
                    "call_id": function_call.call_id
                })
                messages.append({
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": str(tool_result)
                })
            response = client.responses.create(
                model="gpt-4.1-2025-04-14",
                input=messages,
                tools=barista_tools,
                tool_choice="auto"
            )
            assistant_reply = response.output_text
        if not assistant_reply or assistant_reply.strip() == "":
            if function_calls:
                print("Barista (tool result):", str(tool_result))
            else:
                print("Barista: (No response from model)")
        else:
            print(f"Barista: {assistant_reply}")
        messages.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    main()