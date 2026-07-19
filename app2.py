import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY was not found in the .env file")

client = Anthropic(api_key=api_key)


system_message = """
You are Recipe Finder Agent

Your job is to help the user find suitable recipes.

Rules:
- Suggest no more than 3 recipes.
- Consider the user's available ingredients, allergies, dietary restrictions,
  preferred cuisine, cooking time, and difficulty level.
- Keep the answers short and clear.
- Do not adjust ingredient quantities because Agent 3 handles that.
- Do not provide live cooking assistance because Agent 2 handles that.
- Do not claim that you searched the internet unless real search results
  were provided.
- Do not provide full cooking steps until the user chooses a recipe.

For each recipe include:
1. Recipe name
2. Short description
3. Main ingredients
4. Estimated time
5. Difficulty
6. Why it matches the user's request
"""


def run_recipe_agent():
    history = []

    print("Recipe Finder Agent")
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

        history.append({
            "role": "user",
            "content": user_input
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            temperature=0.3,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text

        print(f"\nAgent 1:\n{reply}\n")

        history.append({
            "role": "assistant",
            "content": reply
        })

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        print(
            f"Tokens used: "
            f"Input {input_tokens} | "
            f"Output {output_tokens} | "
            f"Total {input_tokens + output_tokens}\n"
        )


if __name__ == "__main__":
    run_recipe_agent()