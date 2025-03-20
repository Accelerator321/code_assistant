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
    tools=[search_tool, user_input_tool, file_modification_tool,git_branch_tool,
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

instructions = """
Use the tool to fetch relevant code and modify it to accomplish the task.


#use git_branch_tool first to ensure you are on branch nameed "code_assistant-accelerator4321".

Before using file_modification_tool ask user consent via user_input_tool for make chnages.
Before making modifcation remove "<Delim-Line-i> " from the "modification" filed
After using_file_modification commit the changes with commit message = query+| +timestamp using git_commit_tool
example-> commit message = "query|2025-03-20 17:25"
'<Delim-Line-i>' use this delimeter to keep track of line number.
Whenever providing file_path ALways provide full path to filemodifcation tool.
User git_revert_tool when user wants to revert some operations.
In most cases user will provide the message that relates to the commit message he wants to revert,
You have to check logs and deduce which commit user wants to revert and ask user is this the commit you want to delete? and then if user says yes provide the corresponding hash to git_revert_tool.





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

  

