import base64
import os
from google import genai
from google.genai import types
import dotenv
dotenv.load_dotenv()

API=os.environ.get("GEMINI_API_KEY")
PWD=os.path.dirname(os.path.abspath(__file__))

markdown_file = open(PWD + "/converting.md", "r")
markdown_content = markdown_file.read()

SYSTEM_PROMPT = """
You are a helpful assistant that translates markdown to latex.
Never change the language used even if it is not consistent.
Say nothing else than the latex code.
Make sure to keep the same structure as the markdown.
"""

content = f"""{SYSTEM_PROMPT}
Please convert the following markdown to latex:
{markdown_content}
"""

client = genai.Client(api_key=API)
response = client.models.generate_content(
    model="gemini-2.0-pro-exp-02-05", contents=content
)

result = response.text
if result.startswith("```"):
  result = result[9:-3]
print(result)
