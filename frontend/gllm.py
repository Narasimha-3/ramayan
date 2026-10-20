import textwrap

import os
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')


def waterdata(query, summary = "this is the first call"):
    prompt = f'''
    You are a bot who assists users with their query regarding ancient indian god rama and the ramayana and nothing else.
    Each of your responses should be atleast 300 tokens long.
    You will be provided with a user query, your job is to generate an appropriate response to user query in markdown format\
    and also generate an entire summary of query and your response and in following json format at the end of response:
    --your response--
    {{
    "summary" : --your summary--
    }}
    the following is the previously generated summary by you:
    {summary}
    the following is the user query:
    "query" : {query}
    NOTE : GIVE JSON AT THE END AND NO OTHER TEXT AFTER JSON, ILL BE SPLITTING YOUR RESPONSE ON "{" AND "}" TO GET SUMMARY SO BE PRECISE WITH OUTPUT FORMAT
    '''
    response = model.generate_content(prompt)
    responsen = response.text
    # .split("{")[0]
    # summaryn = response.text.split("{")[1]
    return responsen

