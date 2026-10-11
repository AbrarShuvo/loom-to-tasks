import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_client():
    key = os.getenv("GEMINI_API_KEY")
    if not key or key == "your_key_here":
        raise RuntimeError("GEMINI_API_KEY is missing in .env")
    return genai.Client(api_key=key)


def generate_text(prompt):
    model = os.getenv("GEMINI_MODEL")
    if not model or model == "your_model_here":
        raise RuntimeError("GEMINI_MODEL is missing in .env")
    client = get_client()
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text

def generate_structured(contents, schema, system_instruction=None):
    model = os.getenv("GEMINI_MODEL")
    if not model or model == "your_model_here":
        raise RuntimeError("GEMINI_MODEL is missing in .env")
    client = get_client()
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0,
        ),
    )
    return response.text
if __name__ == "__main__":
    try:
        print(generate_text("Reply with exactly: Gemini is working."))
    except Exception as error:
        print(f"Request failed: {type(error).__name__}: {error}")