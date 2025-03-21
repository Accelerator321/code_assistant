from tools import *
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import re
from langchain.prompts import PromptTemplate


load_dotenv()

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

agent = initialize_agent(
    tools=[read_file_tool,search_tool, user_input_tool, file_modification_tool,git_branch_tool,
           git_commit_tool,git_log_tool, git_revert_commit_tool ],
    llm=llm,
    verbose=True,
    handle_parsing_errors=True,
    input_key= "input",
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# Example Query
# query = "change main section to have grid display. and remove navbar"
# query = "change navbar to have dark display"
query = "make the entire project to have dark theme"
# Before making modifcation remove "<Delim-Line-i> " from the "modification" and "actual_code" fields
# without changin start and end field of any of "response["changes"][i]".
# response["changes"] is list of chnage which contains many chnages object. so you can generate partialpatches of modifcations

# modification code will be put in place of actual_code in file, with help of start and end.
# Like start =10, end = 12
# so new code = old_code[0:start]+modification+ old_code[end:len(old_code)].
# modification code may seem to have synatactic error because it is part of the code. But when we finally put that in file so it new_code should become syntax free. write accordingly
# Whenever providing file_path ALways provide full path to filemodifcation tool.

instructions = """

#use git_branch_tool first to ensure you are on branch nameed "code_assistant-accelerator4321".

Search_codebase=>
Use the search_tool to fetch relevant code chunks from codebase, And deduce which files need to be modified,
You can try different serach query to get more context.
You can use search_tool mutiple times with diffrent words. Keep your serach query elaborate for better results.


Performing code modification=>
'<Delim-Line-i>' use this delimeter to keep track of line number for a file, it is needed for tracking start and end line of actual code for This Delimeter is subjected to filepath, for example
<Delim-line-1> for src/main.py has different meanining from <Delim-Line-1> for src/app.py.

Use your logic to provide correct code for user query.
If some code needs to deleted. Generate changes that comments them instead of removing the code.

file_modification and commit->
Before using file_modification_tool show user all the chnages for each file that you are gonna do and then ask user consent via user_input_tool for make chnages.


modifcation filed should contain code for entire file, Not just a patch.

Only after doing all the modifcations required for fullfilling the task  commit the changes with commit message = query using git_commit_tool
example-> commit message = "query"


Revert Operation->
User git_revert_tool when user wants to revert some operations.
In most cases user will provide the message that relates to the commit message he wants to revert,
You have to check logs and deduce which commit user wants to revert and ask user is this the commit you want to delete? and then if user says yes provide the corresponding hash to git_revert_tool.

Important=>
If you are providing input to Tools. If providing json never add comments inside json. I causes parsing erros. and tools are not able to fetch params.
You are to write entire code. Dont give instructions like "Put Main Section Code here" Do it yoursef.

"""
prompt_template = PromptTemplate(
    input_variables=["query","workspace",  "instructions"],
    template="""
    **workspace:** {workspace}

    **Task:** {query}

    **Instructions:**  
    {instructions}
    
    Use the tools to modify the code accordingly.
    """
)

def get_code_help(query,workspace):
  global template, agent
  formatted_prompt = prompt_template.format(workspace=workspace, query=query,instructions=instructions)
  
  response = agent.run({"input": formatted_prompt})

  return response

  

