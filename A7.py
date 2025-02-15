
import requests
from dotenv import load_dotenv 
import os
load_dotenv()
def run_a7(input_path: str, output_path: str):
    # Load the email content
    if os.environ.get('AUTH'):
        input_path = "." + input_path if input_path[0] != '.' else input_path
        output_path = "." + output_path if output_path[0] != '.' else output_path

    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(input_path) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {input_path} or {output_path}")
    
    with open(input_path, "r", encoding="utf-8") as f:
        email_content = f.read()

    prompt = f"""Extract the sender's email address from the following email message and return only the email address:
    ---
    {email_content}
    ---
    Return only the email address, nothing else.
    """
    AIPROXY_TOKEN = os.environ.get('AIPROXY_TOKEN')
    # # Call the LLM API
    response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AIPROXY_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",  # Replace with the correct model
                "messages": [{"role": "user", "content": prompt}],
            },
        ).json()
    # Extract the email address from the response
    sender_email = response["choices"][0]["message"]["content"].strip()
    # Write to output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sender_email)

    
