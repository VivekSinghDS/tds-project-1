import requests
from dotenv import load_dotenv 
import os 
load_dotenv()
AIPROXY_TOKEN = os.environ.get('AIPROXY_TOKEN')
def query_gpt(user_input: str) -> dict:
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_input}],
        },
    )
    return response.json()

def markdown_to_html(markdown_text: str) -> str:

    prompt = f"Convert the following Markdown to HTML:\n\n{markdown_text} \n\n Give me the html only"
    response = query_gpt(prompt)
    
    if 'choices' in response and response['choices']:
        return response['choices'][0]['message']['content'].strip()
    else:
        return "Error: Unable to convert Markdown to HTML"

# Example Usage
# html_output = markdown_to_html("# Hello World\nThis is a **bold** text.")
# print(html_output)
