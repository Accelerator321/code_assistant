import os

from dotenv import load_dotenv
import numpy as np
import google.generativeai as genai
import numpy as np

import uuid
import shutil
import datetime

import os
import json
import re



load_dotenv()


def get_gitignore_patterns(base_path):
    """ Reads .gitignore and returns a list of ignored file patterns. """
    gitignore_path = os.path.join(base_path, ".gitignore")
    git_path = os.path.join(base_path, ".git")
    ignored_patterns = set()
    ignored_patterns.add(gitignore_path)
    ignored_patterns.add(git_path)

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored_patterns.add(os.path.join(base_path,
                                                      line))  # Store full path
    return ignored_patterns


def is_ignored(file_path, ignored_patterns):
    """ Checks if a file should be ignored based on .gitignore patterns. """
    return any(file_path.startswith(pattern) for pattern in ignored_patterns)


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_embedding(text):
    """ Get Gemini embedding for the given text. """
    response = genai.embed_content(model="models/embedding-001",
                                   content=text,
                                   task_type="retrieval_document")
    return np.array(response["embedding"])


# embedding_dim = 768


def read_code(file_path):
    """ Reads code from a file safely. """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def chunk_code(code, file_path, chunk_size=80, overlap=20):
    """ Splits code into overlapping chunks based on characters (not tokens). """
    chunks = []
    start = 0
    code = code.split("\n")

    code = [f"<Delim-Line-{i+1}> {line}" for i, line in enumerate(code)]

    while start < len(code):
        end = min(start + chunk_size, len(code))
        chunk_text = code[start:end]

        chunks.append({
            "text": "\n".join(chunk_text),
            "file_path": file_path,
        })

        start += chunk_size - overlap

    return chunks


def process_folder(folder_path):
    
    """ Reads all files in a folder, excluding ignored files, and stores embeddings. """
    from db import add_to_db
    ignored_patterns = get_gitignore_patterns(folder_path)
    total_chunks = 0
    for root, _, files in os.walk(folder_path):

        for file in files:
            file_path = os.path.join(root, file)

            # Ignore files listed in .gitignore
            if is_ignored(file_path, ignored_patterns):
                # print(f"🚫 Skipping ignored file: {file_path}")
                continue

            code = read_code(file_path)
            if code is None:
                continue
            # print(code)

            chunks = chunk_code(code, file_path)

            for chunk in chunks:
                embedding = get_embedding(chunk["text"])

                
                
                add_to_db(embedding,{
                                "file_path": chunk["file_path"],
                                "chunk_text": chunk["text"]
                            })

            print(f"✅ Processed {file_path}: {len(chunks)} chunks")

            total_chunks += len(chunks)

    print(f"✅ Stored {total_chunks} chunks in FAISS from {folder_path}")




def apply_changes(response):
    res = parse_agent_response(response)
    if not res: return
    changes = res.get("changes",[])
    query = res.get("query","")
    changes_by_file = {}
    backup = {}

    # Grouping changes by file
    for change in changes:
        
        changes_by_file.setdefault(change['filepath'], []).append(change)

    # Applying changes to each file
    for file, file_changes in changes_by_file.items():
        file_changes.sort(key=lambda x: x['start'])

        
        if os.path.exists(file):
            with open(file, "r") as f:
                code = f.read()
            backup[file] = code
        else:
            code = ""
            

        code_lines = code.split("\n")
        new_code = ""
        start = 0

        
        for change in file_changes:
            new_code += "\n".join(code_lines[start:change['start']-1]) + "\n"
            new_code += change['modification'] + "\n"
            start = change['end']

        new_code += "\n".join(code_lines[start:])

        
        with open(file, "w") as f:
            f.write(new_code)

    
    backup_file = "backup.json"
    if not os.path.exists(backup_file):
        with open(backup_file, "w") as f:
            json.dump({}, f)

    with open(backup_file, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    with open(backup_file, "w") as f:

        stamp = query + " | time-> " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data[stamp] = backup

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate() 

def refresh_backup(backup_file, folder_path):
    if not os.path.exists(backup_file):
        with open(backup_file, "w") as f:
            json.dump({"folder_path": folder_path}, f, indent=4)
        return

    with open(backup_file, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

        if data.get("folder_path") != folder_path:
            f.seek(0)
            json.dump({"folder_path": folder_path}, f, indent=4)
            f.truncate()




def parse_agent_response(response):
    try:
        params = json.loads(response)
        return params
    except Exception as e:
        pass
    pattern = r'```json\s*([\s\S]*?)\s*```'

  
    match = re.search(pattern, response)
    ans = {}
    if match:
        json_content = match.group(1)
        try:
            parsed_json = json.loads(json_content)
            ans = parsed_json
        except json.JSONDecodeError:
            ans = {}
    return ans


def get_backup_commits():
    commits = []
    with open("backup.json") as f:
        data= json.load(f)
        commits = [key for key in data.keys() if key !="folder_path"]
    
    return json.dumps(commits)


def revert_commit(message):
    backup = {}
    with open("backup.json") as f:
        backup= json.load(f)
    
    if message not in backup: return "No such commit found"

    changes = backup[message]

    for file_path, code in changes.items():
        with open(file_path,"w") as f:
            f.write(code)

    commits = list(backup.keys())
    index = commits.index(message)
    
    backup = {key:backup[key] for key in commits[0:index]}

    with open("backup.json", "w") as f:
        json.dump(backup, f, indent=4)

    
    return "Commit reverted succesfully"

    
if __name__ =="__main__":
    commit= "comment navbar code | time-> 2025-03-20 16:05:28"
    print(revert_commit(commit))
    # print(revert_commit("change savbar to have black background and apply chnages time-> 2025-03-18 22:29:53"))