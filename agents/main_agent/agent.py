from .tools import *
from shared_tools import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain import hub
from agents.git_agent import git_agent
import os
from agents.git_agent.git_tools import *
load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize Gemini Model
api_key= os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3,google_api_key=api_key)

instructions = """
# First, ensure you are on the branch "code_assistant-accelerator4321" using git_branch tool.

## Search Codebase
- Use the search_tool to fetch relevant code chunks from the codebase and determine which files need modification.
- Try different search queries to get more context.
- You can use search_tool multiple times with different queries. Keep your search queries elaborate for better results.

## Performing Code Modification
- Use '<Delim-Line-i>' to track the line number of a file. This delimiter is file-specific (e.g., `<Delim-line-1>` in `src/main.py` differs from `<Delim-line-1>` in `src/app.py`).
- Modify the code logically based on the user query.
- If code needs to be deleted, **comment it out instead of removing it**.

## File Modification and Commit
- Before using file_modification_tool, **show the user all planned changes** and ask for consent using user_input_tool.
- The modification field should contain **the entire file content, not just a patch**.
- After applying all modifications, commit changes using git_commit_tool with:
  - `commit message = user query`

## Revert Operations
- Use git_revert_tool when the user wants to revert changes.
- The user will usually provide a commit-related message.
- Check the git log to determine which commit to revert.
- Ask the user for confirmation before running git_agent.

## Important
dont use ``` or ` when providing input to tools. It creates parse errors. And tool malfunctions.
When generation workspace or filepath - dont write "c:\\local" use "c:/local".
This is done to avoid escape seqeunce erros.
"""



prompt_template = PromptTemplate(
    input_variables=["query", "workspace", "instructions"],
    template="""
    **Workspace:** {workspace}

    **Task:** {query}

    **Instructions:**  
    {instructions}

    """
)




tools = [read_file_tool, search_tool, user_input_tool, file_modification_tool, git_branch_tool,
         git_commit_tool, git_revert_commit_tool, git_log_tool
         ]

# Corrected: Use `create_react_agent` instead of `initialize_agent`
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt ,
    
)

# Wrap it with an AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,  # ✅ Add this line
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=50,

)


# Define the function
def get_code_help(query, workspace):
    response = agent_executor.invoke({
        "input": prompt_template.format(query = query, workspace= workspace, instructions=instructions)
    })
    return response
