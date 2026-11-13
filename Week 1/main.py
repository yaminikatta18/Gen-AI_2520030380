import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
)

print("Connecting to Gemini...")

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain Artificial Intelligence in 3 simple sentences."
    )

    print("\nGemini AI Response:")
    print(response.text)

except Exception as e:
    print("\nError:", e)

print("\nProgram finished.")