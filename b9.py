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

def is_allowed_path(file_path: str) -> bool:
    abs_path = os.path.abspath(file_path)
    return abs_path.startswith("/data/")

def fetch_content(input_path: str) -> str:
    if input_path.startswith("http://") or input_path.startswith("https://"):
        response = requests.get(input_path)
        response.raise_for_status()
        return response.text
    elif is_allowed_path(input_path):
        with open(input_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise PermissionError(f"Access outside /data/ is not allowed: {input_path}")

def run_b9(input_path: str, output_path: str):
    try:
        # Read the markdown content from either URL or local file
        markdown_text = fetch_content(input_path)
        
        # Prepare the prompt
        prompt = f"Convert the following Markdown to HTML:\n\n{markdown_text} \n\n Give me the html only"
        
        # Query GPT for conversion
        response = query_gpt(prompt)
        
        # Extract and save the HTML output
        if 'choices' in response and response['choices']:
            html_content = response['choices'][0]['message']['content'].strip()
            
            if is_allowed_path(output_path):
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(html_content)
                print(f"HTML file saved to {output_path}")
            else:
                raise PermissionError(f"Access outside /data/ is not allowed: {output_path}")
        else:
            print("Error: Unable to convert Markdown to HTML")
    except Exception as e:
        print(f"Error processing file: {e}")
