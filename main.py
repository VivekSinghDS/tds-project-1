import json 
import requests
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

import requests
from A1 import run_a1
from A2 import run_a2
from A3 import run_a3
from A4 import run_a4
from A5 import run_a5
from A6 import run_a6
from A7 import run_a7
from A8 import run_a8
from A9 import run_a9
from A10 import run_a10

from b2 import run_b2
from b3 import run_b3
from b7 import run_b7_1
from dotenv import load_dotenv 
import sqlite3
import duckdb 

load_dotenv()
# Setup FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def save_to_file(input_path: str, content: str):
    with open(input_path, 'w') as file:
        file.write(content)
AIPROXY_TOKEN = os.environ.get('AIPROXY_TOKEN')
FUNCTION_SCHEMAS = [    
    {
        "type": "function",
        "function": {
            "name": "run_a1",
            "description": "Install 'uv' if required and run a Python script from a given URL with the user's email as the only argument",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_url": {
                        "type": "string",
                        "description": "URL of the Python script to be executed",
                    },
                    "email": {
                        "type": "string",
                        "description": "Email address to be passed as an argument to the script",
                    }
                },
                "required": ["script_url", "email"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a2",
            "description": "Format the contents of an input file using prettier@3.4.2 and updating the file in-place",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Input file path to be updated"
                    },
                    "package": {
                        "type": "string",
                        "description": "name of the packae"
                    },
                    "version": {
                        "type": "string",
                        "description": "Version of the package"
                    }
                },
                "required": ["input_path", "package", "version"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_a3",
            "description": "Given an input file, count the total of weekday numbers asked by the user and then write the number to another file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Input file path from where the dates need to be read"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the results need to be written"
                    },
                    "weekday": {
                        "type": "string",
                        "description": "Day of the week"
                    }

                },
                "required": ["input_path", "output_path", "weekday"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_a4",
            "description": "Sort an array of contacts by last_name, then first_name, and write the result to another file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Input file path containing the array of contacts"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the sorted contacts should be written"
                    },
                    "keys": {
                        "type": "string",
                        "description": "required format: python list of keys that should be sorted"
                    }
                },
                "required": ["input_path", "output_path", "keys"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a5",
            "description": "Extract the first line of the 10 most recent .log files in a directory and write them to another file, ordered from most recent to least recent",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_directory": {
                        "type": "string",
                        "description": "Path to the directory containing log files"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the first lines of the most recent log files should be written"
                    },
                },
                "required": ["log_directory", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a6",
            "description": "Find all Markdown (.md) files in a directory, extract the first H1 heading from each file, and create an index mapping filenames to titles",
            "parameters": {
                "type": "object",
                "properties": {
                    "docs_directory": {
                        "type": "string",
                        "description": "Path to the directory containing Markdown files"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the index JSON should be written"
                    }
                },
                "required": ["docs_directory", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a7",
            "description": "Extract the sender's email address from an email message using an LLM and write it to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to the text file containing the email message"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the extracted email address should be written"
                    }
                },
                "required": ["input_path", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a8",
            "description": "Extract the credit card number from an image using an LLM and write it without spaces to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to the image file containing the credit card number"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the extracted credit card number should be written without spaces"
                    }
                },
                "required": ["input_path", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a9",
            "description": "Find the most similar pair of comments using embeddings and write them to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "Path to the text file containing a list of comments, one per line"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Output file path where the most similar pair of comments should be written, one per line"
                    },
                    "no_of_similar_texts": {
                        "type": "string",
                        "description": "Number of similar text pairs to return"
                    }
                },
                "required": ["input_file", "output_file", "no_of_similar_texts"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_a10",
            "description": "Calculate the total sales for a particular ticket type in an SQLite database and write the result to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "database_path": {
                        "type": "string",
                        "description": "Path to the SQLite database file containing ticket sales data"
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of the ticket"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path where the total sales amount for that type of tickets should be written"
                    }
                },
                "required": ["database_path", "type", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_b3",
            "description": "Scrape contents for a website",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "url to be scraped"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "path where the output needs to be saved"
                    },
                    "params": {
                        "type": "object",
                        "description": "query parameters for the request body"
                    },
                    "headers": {
                        "type": "object",
                        "description": "headers for the request"
                    }
                },
                "required": ['url', 'output_path', 'headers', 'params'],
                "additionalProperties": False
            },
            "strict": False
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_b7_1",
            "description": "function that will compress or resize an image",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "input file path or the url of an image"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "path where the file should be saved"
                    },
                    "width": {
                        "type": "number",
                        "description": "width to which the image needs to be compressed, 300 if not given anything"
                    },
                    "height": {
                        "type": "number",
                        "description": "height to which the image needs to be compressed, 300 if not given anything"
                    },
                },
                "required": ['source', 'output_path', 'width', 'height'],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_b2",
            "description": "Delete a particular file or directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "input file path or directory path"
                    },
                },
                "required": ['path'],
                "additionalProperties": False
            },
            "strict": True
        }
    }

]


async def query_gpt(user_input: str, tools: list) -> dict:
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",  # Replace with the correct model
            "messages": [{"role": "user", "content": user_input}],
            "tools": tools,
        },
    )
    print(response.content)
    return response.json()




@app.post("/run")
async def execute_query(task: str):
    try:
        response = dict(await query_gpt(task, FUNCTION_SCHEMAS))

        tool_call = response["choices"][0]["message"].get("tool_calls", None)
        if tool_call:
            tool_call = tool_call[0]
            function_name = tool_call["function"]['name']
            arguments = json.loads(tool_call['function']["arguments"])
            result = globals()[function_name](**arguments)
            return {"name": function_name, "arguments": arguments}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
@app.get("/read")
def read_file(path: str):
    # if os.environ.get('AUTH'):
    #     print('in here', os.environ.get('AUTH'), type(os.environ.get('AUTH')))
    #     path = "." + path
    # if not os.path.exists(path):
    #     raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return PlainTextResponse(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
