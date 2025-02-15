import re
from typing import Dict, Any, Optional
from pathlib import Path
import json 
import requests
class TaskRouter:
    def __init__(self):
        # Import task implementations
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
        
        self.task_runners = {
            'A1': run_a1,
            'A2': run_a2,
            'A3': run_a3,
            'A4': run_a4,
            'A5': run_a5,
            'A6': run_a6,
            'A7': run_a7,
            'A8': run_a8,
            'A9': run_a9,
            'A10': run_a10
        }

    
    async def classify_task(self, task_description: str) -> Dict[str, Any]:
        """Use LLM to classify the task and extract parameters"""
        # Prompt engineering for the LLM
        print('prompt initialization')
        prompt = f"""Analyze this task description and match it to one of the following base tasks:

        A1: Install uv and run datagen.py script
        A2: Format markdown file using prettier
        A3: Count weekday occurrences in a dates file
        A4: Sort contacts JSON by name
        A5: Extract first lines from recent log files
        A6: Create index of markdown H1 headers
        A7: Extract sender email from message
        A8: Extract credit card number from image
        A9: Find similar comments using embeddings
        A10: Calculate total sales for ticket type

        Task description: """ + str(task_description) + """\n

        Return a JSON object with:
        1. base_task: The matching task ID (A1-A10)
        2. input_file: The input file path mentioned
        3. output_file: The output file path mentioned
        4. parameters: Any other parameters (e.g. weekday for A3, ticket_type for A10)

        Example for A3:
        {
            "base_task": "A3",
            "input_file": "./data/dates.txt",
            "output_file": "./data/dates-wednesdays.txt",
            "parameters": {"weekday": "Wednesday"}
        }
        """

        # Call your LLM here with the prompt
        response: str = await self.call_llm(prompt)
        first = response.find('{')
        last = response.rfind('}')
        response = response[first: last + 1]
        parsed = json.loads(response)
        
        return parsed

    def validate_paths(self, task_info: Dict[str, Any]) -> bool:
        """Validate that the input file exists and output path is writable"""
        input_path = Path(task_info['input_file'])
        output_path = Path(task_info['output_file'])
        
        if not input_path.exists():
            raise ValueError(f"Input file {input_path} does not exist")
            
        if not output_path.parent.exists():
            raise ValueError(f"Output directory {output_path.parent} does not exist")
            
        return True

    async def execute_task(self, task_description: str) -> bool:
        """Main method to process and execute a task"""
        try:
            # Parse the task
            print('before')
            task_info = await self.classify_task(task_description)
            print(task_info)
            # Validate paths
            self.validate_paths(task_info)
            
            # Get the appropriate runner
            task_id = task_info['base_task']
            if task_id not in self.task_runners:
                raise ValueError(f"Unknown task ID: {task_id}")
            
            runner = self.task_runners[task_id]
            
            # Execute the task
            result = runner(
                input_file=task_info['input_file'],
                output_file=task_info['output_file'],
                **task_info.get('parameters', {})
            )
            
            return True
            
        except Exception as e:
            print(f"Error executing task: {str(e)}")
            return False

# Example usage in FastAPI
from fastapi import FastAPI, HTTPException

app = FastAPI()
router = TaskRouter()

@app.get("/run")
async def run_task(task: str):
    print(task)
    success = await router.execute_task(task)
    if not success:
        raise HTTPException(status_code=500, detail="Task execution failed")
    return {"status": "success"}