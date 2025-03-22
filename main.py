from utils.utils import process_folder
from dotenv import load_dotenv
import os
from agents.main_agent.tools import search_code
from agents import get_code_help
import json
import subprocess
from utils.utils import apply_changes, refresh_backup
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize Gemini Model




workspace = "D:\\code assistant\\react-tw-sample"
branch_name = "code_assistant-accelerator4321"
backup_file = "backup.json"



 

if __name__ =="__main__":
    # out= execute(f'git -C "{workspace}" checkout {branch_name}')
    # print(out ,"yp", out, "yp")

    refresh_backup(backup_file, workspace)
    process_folder(workspace)
    while(True):
        
        
        query = input("Please Enter your Query\n")


        result = get_code_help(query, workspace)
        print(result)



