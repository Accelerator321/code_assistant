import subprocess
from utils.utils import parse_agent_response
import os
# def execute(command):
  
#     output_file = os.popen(command)

#     output = output_file.read()

#     output_file.close()
    
#     return output
def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    return stdout.strip() if stdout else stderr.strip() 


def create_branch(response):
    
    print(response)
    params = parse_agent_response(response)
    print("parsed", params)
    branch_name =params.get("branch_name", "code_assistant-accelerator4321")
    workspace = params.get("workspace","xyz")
    
    
    check_cmd = f'git -C "{workspace}" branch --list {branch_name}'
    existing_branch = execute(check_cmd)

    if existing_branch:  
        
        cmd = f'git -C "{workspace}" checkout {branch_name}'
    else:
        # Branch does not exist, create and checkout
        cmd = f'git -C "{workspace}" checkout -b {branch_name}'

    return execute(cmd)


def get_commit_log(response):
    params = parse_agent_response(response)
    workspace = params.get("workspace","xyz")
    
    commit_count = params.get("commit_count", "10")  # Default to last 10 commits
    
    cmd = f'git -C "{workspace}" log -n {commit_count} --pretty=format:"%h - %s"'
    return execute(cmd)


def revert_commit(response):
    
    params = parse_agent_response(response)
    
    workspace = params.get("workspace","xyz")
    
    commit_hash = params.get("commit_hash", "")
    
    if not commit_hash:
        return "❌ Error: No commit hash provided for revert."
    
    cmd = f'git -C "{workspace}" revert {commit_hash} --no-edit'
    return execute(cmd)

def commit_changes(response):
    
    params = parse_agent_response(response)
    
    workspace = params.get("workspace","xyz")

    if workspace=="xyz": "Could not commit. Something went wrong. Possible error=> If you are providing comment inside json remove comments because it cause parsing errors."
   
    commit_message = params.get("commit_message", "No commit message provided")  
    execute(f'git -C "{workspace}" add .')
    cmd = f'git -C "{workspace}" commit -m "{commit_message}"'
    return execute(cmd)


import os
if __name__ =="__main__":
    workspace = "D:\\code assistant\\react-tw-sample"
    branch_name = "code_assistant-accelerator4321"
    cmd = f'git -C "{workspace}" checkout -b {branch_name}'
    output_file = os.popen(cmd)

    output = output_file.read()
    print(output,"out")
    output_file.close()
