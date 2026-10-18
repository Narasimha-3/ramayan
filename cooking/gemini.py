
# import google.generativeai as genai

# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# model = genai.GenerativeModel('gemini-1.5-pro')

# def ramayandata(prompt):
#     response = model.generate_content(prompt)
#     # print(response.text)
#     # with open('ayodhyakanda.txt', 'a') as f:
#     #     f.write("jai_balayya_ew\n")
#     #     f.write(response.text)
#     #     f.write("jai_balayya_ew\n")
#     return response.text

import os
from google import genai

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def ramayandata(prompt):
    # response = client.models.generate_content(
    # model="models/gemini-2.5-flash",
    # contents=prompt
    # )
    pp = ""
    try:
        pp = prompt.split("---------\n")[1]
    except:
        pp = prompt
    return pp