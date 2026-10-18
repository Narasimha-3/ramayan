
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')


def ramayandata(prompt):
    response = model.generate_content(prompt)
    return response.text

