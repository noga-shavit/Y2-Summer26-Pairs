import os
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
    print('You: (type exit to quit)')
    system_message = """
You are Mama, an on-hand assistant chef
Your job is to hep the user while cooking with any issues with ingredients, temp, cooking, or anything else, and advise them in cases of emergency

Rules:
- Always adhere to main kitchen rules: sanitation, cleanliness, clean ingredients, and organized work
- Always check up on the user after every prompt, to make sure no crises happened
- 

Response format:
- Start by summarizing what the user said,
- Then give your response in a concise, understandable, and relevent way.
- End with one follow-up question for the user on their topic or previous question.
"""
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            print('Exiting chat...')
            break
        history.append({'role': 'user', 'content': user_input})
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=500,
            temperature=0.8,
            system=system_message,
            messages=history,
        )

        reply = response.content[0].text
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})
run_chat()