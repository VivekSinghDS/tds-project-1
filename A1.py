import os
import subprocess
import requests

def install_uv():
    """Check if `uv` is installed, and install it if necessary."""
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Installing uv...")
        subprocess.run(["pip", "install", "uv"], check=True)

def download_script(url: str, filename: str = "datagen.py"):
    """Download the script from the given URL and save it locally."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded {filename} successfully.")
    else:
        raise Exception(f"Failed to download script: {response.status_code}")

def run_script(email: str):
    """Run the downloaded script with the given email as an argument."""
    process = subprocess.run(
        ["uv", "run", "datagen.py", email],
        capture_output=True,
        text=True
    )
    if process.returncode == 0:
        print(f"Script executed successfully:\n{process.stdout}")
    else:
        print(f"Error executing script:\n{process.stderr}")

def read_file(filepath: str):
    """Read the contents of the file synchronously."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def run_a1(script_url: str, email: str):
    """Run the script and check if email appears in /data/format.md."""
    
    # install_uv()
    download_script(script_url)
    run_script(email)

    content = read_file("/data/format.md")
    return email in content