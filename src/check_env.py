import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key or key == "your_key_here":
    print("API key missing. Add it to your .env file.")
else:
    print(f"API key found ({len(key)} characters). Not printing it.")