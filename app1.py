# Noga's File <3

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = """
    Your name is Mimi, a sous-chef who calculates 
    recipe ratios and adjusts amounts, while writing the final recipes in a txt file
    Rules: 
        1. Always ask how many people in the meal before calculating the amounts and recipe ratios
        2. Always use short, clear, concise, and understandable responses confirming the action
        3. Always answer politely, never be rude
    
    Response Format:
        - Summarize what the user asked you by saying the recipe name and the amount of servings
        -  Then give your response
        - end with a follow-up question for the user

    """
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})
        print('History so far:', history)

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(response)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()

try:
    f = open("recipebook.txt", "x") 
except FileExistsError:
    with open("recipebook.txt", "a") as f:
      f.write(input("Enter recipe: "))