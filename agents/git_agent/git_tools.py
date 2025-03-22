
from .git_utils import *
from langchain.tools import Tool
git_branch_tool = Tool(
    name="git_branch_tool",
    func=create_branch,
    description="""
    Use this tool to create or switch to a Git branch. If the branch does not exist, it will be created.
    If branch already exists it will return already on branch
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
    provid params:
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