def run_a8(input_path: str, output_path: str):
    import requests
    import base64
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if os.environ.get('AUTH'):
        input_path = "." + input_path if input_path[0] != '.' else input_path
        output_path = "." + output_path if output_path[0] != '.' else output_path

    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(input_path) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {input_path} or {output_path}")
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        

    # Getting the Base64 string
    base64_image = encode_image(input_path)
    AIPROXY_TOKEN = os.environ.get('AIPROXY_TOKEN')
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",  # Replace with the correct model
            "messages": [{"role": "user", "content": [
                {
                    "type": 'text',
                    'text': 'Given the image, give me the largest number present in it without spaces. Give me only that number and nothing other than that'
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                }
            ]}],
        },
    ).json()
    content = response["choices"][0]["message"]["content"].strip()
    print(content,  ' is this one')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    

