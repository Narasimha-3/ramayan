

import google.generativeai as genai



genai.configure(api_key="AIzaSyDGEhvcZdGAUZXl2wFsw_IpCLpqLb9zaac")
model = genai.GenerativeModel('gemini-1.5-pro')


def ramayandata(prompt):
    response = model.generate_content(prompt)
    return response.text

