import requests 
from typing import Optional 

def run_b3(url: str, params: Optional[dict] = {}):
    try:
        if not url.startswith('http'):
            url = "http://" + url
        response = requests.get(url, params = params)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise 