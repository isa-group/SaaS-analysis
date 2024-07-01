import pathlib
import textwrap
import os

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_text(prompt):
    return model.generate_content(prompt)

if __name__ == '__main__':
    prompt = "What is the meaning of life?"
    print(generate_text(prompt).text)