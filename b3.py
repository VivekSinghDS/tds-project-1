import requests 
from typing import Optional 

def run_b3(url: str, output_path: str, params: Optional[dict] = {}, headers: Optional[dict] = {}):
    try:
        if not url.startswith('http'):
            url = "http://" + url
        response = requests.get(url, params = params, headers = headers)
        response.raise_for_status()
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(response.content))
    except requests.exceptions.RequestException as e:
        raise 