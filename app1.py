# Noga's File <3

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def save_recipe(recipe):
    try:
        with open("recipebook.json", "r") as f:
            recipe_book = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        recipe_book = {"recipes": []}

    if not isinstance(recipe_book.get("recipes"), list):
        recipe_book["recipes"] = []

    recipes = recipe_book["recipes"]
    recipes.append(recipe)

    with open("recipebook.json", "w") as f:
        json.dump(recipe_book, f, indent=2)

def run_chat():
    print('Paste your recipe, then type SEND on a new line. Type exit to quit.')
    system_message = """
    Your name is Mimi, a recipe organizer.

    Rules:
        1. When the user pastes a complete recipe, extract its name, ingredient list,
           instructions, and notes.
        2. Preserve ingredient quantities and instruction details from the pasted recipe.
        3. If the recipe has no title, create a short descriptive name based on its
           main ingredient and preparation method.
        4. Do not invent missing ingredients, instructions, or notes. Use an empty
           list when there are no notes.
        5. Call the save_recipe tool once the recipe has been extracted.
        6. Only say that a recipe was saved after calling the tool.

    """
    tools = [
        {
            "name": "save_recipe",
            "description": "Save a structured recipe in recipebook.json.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "instructions": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "notes": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["name", "ingredients", "instructions", "notes"]
            }
        }
    ]
    history = []

    while True:
        print('>> ', end='')
        input_lines = []

        while True:
            line = input()

            if line.strip().lower() == 'send':
                break

            if line.strip().lower() == 'exit' and not input_lines:
                return

            input_lines.append(line)

        user_input = '\n'.join(input_lines).strip()

        if not user_input:
            print('Please paste a recipe before typing SEND.')
            continue

        history.append({'role': 'user', 'content': user_input})
        print('History so far:', history)

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1000,
            temperature=0.7,
            system=system_message,
            messages=history,
            tools=tools
        )

        reply_parts = []
        saved_recipes = []

        for block in response.content:
            if block.type == "text":
                reply_parts.append(block.text)
            elif block.type == "tool_use" and block.name == "save_recipe":
                save_recipe(block.input)
                saved_recipes.append(block.input["name"])

        if saved_recipes:
            reply_parts.append(
                f"Recipe saved in recipebook.json: {', '.join(saved_recipes)}"
            )

        reply = "\n".join(reply_parts)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()
