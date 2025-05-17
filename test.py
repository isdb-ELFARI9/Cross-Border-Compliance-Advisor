import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Read the API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")
    print("HIIII " + api_key)
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set.")
        print("   Set it with:\n    export OPENAI_API_KEY=\"your_key_here\"")
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Get user prompt from command-line arguments
    if len(sys.argv) < 2:
        print("❌ Error: No prompt provided.")
        print("   Usage:\n    python3 script.py \"Your prompt here\"")
        sys.exit(1)

    user_prompt = sys.argv[1]

    try:
        # Make a chat completion call to gpt-3.5-turbo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        content = response.choices[0].message.content.strip()
        print("✅ Success! GPT-3.5-turbo responded:\n")
        print(content)
        sys.exit(0)

    except Exception as e:
        print("❌ Failed to call gpt-3.5-turbo.")
        print("Error message:", e)
        sys.exit(2)

if __name__ == "__main__":
    main()
