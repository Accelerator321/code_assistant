from utils.utils import process_folder
from dotenv import load_dotenv
import os
from tools import search_code
from agent import get_code_help
import json
import subprocess
from utils.utils import apply_changes, refresh_backup




load_dotenv()

workspace = "D:\\code assistant\\react-tw-sample"
branch_name = "code_assistant-accelerator4321"
backup_file = "backup.json"





if __name__ =="__main__":
    while(True):
        refresh_backup(backup_file, workspace)
        process_folder(workspace)
        query = input("Please Enter your Query\n")


        result = get_code_help(query, workspace)
        print(result)



