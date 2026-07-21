import os
from dotenv import load_dotenv

load_dotenv()

# Clean imports of collaboration steps (ignoring the loops entirely!)
from app2 import run_momo_step
from app3 import run_mama_step
from app1 import run_mimi_step

def run_pipeline():
    print("🚀 Pipeline Initialized!")
    query = input("Ask Momo for a recipe to run the complete pipeline: ").strip()
    
    if not query:
        print("Please enter a valid recipe name.")
        return

    print("\n🔍 Step 1: Momo is running an internet search...")
    momo_result = run_momo_step(query)
    print(f"Momo output complete:\n{momo_result}\n")

    print("✍️ Step 2: Mama is formatting text templates and checking logs...")
    mama_history = []
    mama_reply, updated_history = run_mama_step(f"Here is a raw internet search result: {momo_result}", mama_history)
    print(f"Mama output complete:\n{mama_reply}\n")

    print("💾 Step 3: Mimi is running structured schema tools and saving to JSON...")
    mimi_result = run_mimi_step(momo_result)
    print(f"Mimi output complete:\n{mimi_result}\n")
    
    print("🏆 Collaboration complete! All records have been cleanly updated.")

if __name__ == "__main__":
    run_pipeline()
