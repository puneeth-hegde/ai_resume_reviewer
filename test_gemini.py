import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "Summarize: Artificial Intelligence is transforming industries."
response = model.generate_content(prompt)
print(response.text)
