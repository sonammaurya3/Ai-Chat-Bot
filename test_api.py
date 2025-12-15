import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print("API Key:", openai.api_key)  # check if None

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":"Hello"}]
    )
    print(response['choices'][0]['message']['content'])
except Exception as e:
    print("Error:", e)
