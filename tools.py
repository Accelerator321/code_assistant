from db import search_code
from langchain.tools import Tool
from utils.utils import apply_changes
from utils.run_command import run_command
from utils.git_utils import *


def user_input(text):
    print(text, end="-> ")
    inp = input()
    return inp

search_tool = Tool(
    name="search_code",
    func=search_code,
    description="Retrieves relevant code chunks based on the query.",
)



user_input_tool = Tool(
    name="take_user_input",
    func=user_input,
    description="This tool can be used to take input from user",
)

file_modification_tool = Tool(
    name="file_modification_tool",
    func=apply_changes,
    description="""Applies code changes to user files.Necessary to ask user consent before applying.
    Never apply chnages without user consent
    Input format
    ```json
        {{
            "changes": [
                {{

                    "filepath": str,  # Path to the file being modified (full path)
                    "modification": str,  # New code replacing the original entire line. modified code should strictly not have <Delim-Line-i>
                    "actual_code": str  # The original code that was replaced entire line.
                                        return actaul code as you read dont remove DELIMITER
                    "start": int,   # Start line number of actual code( return i of first occurance <Delim-line-i> in actual_code)
                    "end": int,     # End line number actual code ( return j of last ocuurance <Delim-line-j> in actual_code)
                }}
                }}
                "query": "initial user query"
            ]
        }}
        commit the chnages after using this tool. Commit mesage will be initial userQuery+|+timestamp
    """
)


git_branch_tool = Tool(
    name="git_branch_tool",
    func=create_branch,
    description="""
    Use this tool to create or switch to a Git branch. If the branch does not exist, it will be created.
    provide:
    "workspace": str #workspace path given in user query
    "branch_name": str #branch to create or visit default ("code_assistant-accelerator4321")
    """
)

git_log_tool = Tool(
    name="git_log_tool",
    func=get_commit_log,
    description="""
    Use this tool to retrieve commit logs from a Git repository.
    providyese params:
        "workspace": str #workspace path given in user query
        "limit": int  # Number of commits to retrieve (default is 10)
    
    """
)

git_commit_tool = Tool(
    name="git_commit_tool",
    func=commit_changes,
    description="""
    Use this tool to commit staged changes in a Git repository.
    provide :
    "workspace": str #workspace path given in user query 
    "commit_message": str #commit message
    """
)

git_revert_commit_tool = Tool(
    name="git_revert_commit_tool",
    func=revert_commit,
    description="""
    Use this tool to revert a specific commit in a Git repository.
    
    provide  
        "workspace": str #workspace path given in user query
        "commit_hash": str  # Commit hash to revert

    
    """
)


