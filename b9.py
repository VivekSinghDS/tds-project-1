import requests

def query_gpt(user_input: str) -> dict:
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZHMxMDAwMDA1QGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.grlCTIxE_6nM1-sxRWMZOCooZ9Ndvrm7dlMjdr08Xug",
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
