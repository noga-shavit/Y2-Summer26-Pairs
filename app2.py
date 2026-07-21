import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY was not found in the .env file")

client = Anthropic(api_key=api_key)

system_message = """
your name is Momo, You are Recipe Finder Agent

Your job is to help the user find suitable recipes.

Rules:
- Always use web search when the user asks for recipes.
- Base your recommendations on real web search results.
- Recommend no more than 3 recipes.
- Include the real source link for every recipe.
- Never invent recipe names, sources, or links.
- Keep the answers short and clear.
- Do not adjust ingredient quantities because Agent3-Mama handles that.
- Do not provide live cooking assistance because Agent2 - Mimi handles that.
- Do not claim that you searched the internet unless real search results was provided.

For each recipe include:
1. Recipe name
2. Short description
3. Main ingredients
4. Estimated time
5. Difficulty
6. Why it matches the user's request
"""
def run_momo_step(user_input: str) -> str:
    """Takes a query from main.py and searches the web directly."""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0.3,
        system=system_message,
        messages=[{"role": "user", "content": user_input}],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 2
        }]
    )
    reply = ""
    for block in response.content:
        if block.type == "text":
            reply += block.text
    return reply


def run_recipe_agent():
    history = []
    print("Recipe Finder Agent-Momo")
    print("Describe the recipe you need.")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter a recipe request.")
            continue

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            temperature=0.3,
            system=system_message,
            messages=history,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 2
            }]
        )

        reply = ""
        for block in response.content:
            if block.type == "text":
                reply += block.text

        print(f"\nMomo:\n{reply}\n")
        history.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    run_recipe_agent()
