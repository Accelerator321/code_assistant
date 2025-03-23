from langchain.tools import Tool
import base64
def user_input(text):
    print(text, end="-> ")
    inp = input()
    return inp


user_input_tool = Tool(
    name="take_user_input",
    func=user_input,
    description="This tool can be used to take input from user",
)

import subprocess
import json
from langchain.tools import tool
from utils.utils import parse_agent_response

@tool
def render_code_changes_tool(changes):
    """
    Takes changes, reads actual code from file paths, and passes them to the UI renderer.
    
    Each change should be a dictionary with "file_path" and "modification" fields.
    params:format :  {"changes": List[{"file_path":str,"modification":str }]}
    """
    print("Raw changes:", changes)
    changes = parse_agent_response(changes)
    print("Parsed changes:", changes)
    changes = changes["changes"]
    # Read actual code from files
    for change in changes:
        file_path = change.get("file_path")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                change["actual_code"] = f.read()
        except FileNotFoundError:
            change["actual_code"] = "File not found"
        except Exception as e:
            change["actual_code"] = f"Error reading file: {str(e)}"

        change["filename"] = file_path  # Rename "file_path" to "filename" for consistency

    # Convert to JSON and encode as Base64
    encoded_json = base64.b64encode(json.dumps(changes).encode()).decode()

    # Pass Base64 string as an argument
    subprocess.run(["python", "ui.py", "--files", encoded_json])