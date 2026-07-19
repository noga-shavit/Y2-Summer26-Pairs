# Noga's File <3

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = """
    You are mimi, a motivation coach.

    Your job is to to encourage excitement and ambition.

    Rules:
    - Always answer politely
    - Always use emojis that are related to the answer
    - Never curse or use foul language 

    Response format:
    - Start with a one-sentence summary of what the user said.
    - Then give your response.
    - End with one follow-up question.
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