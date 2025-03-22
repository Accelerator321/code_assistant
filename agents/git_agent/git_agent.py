from shared_tools import user_input_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain import hub
from .git_tools import *
from utils.utils import parse_agent_response
from langchain.tools import Tool

load_dotenv()

# Initialize Gemini Model
api_key= os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3,google_api_key=api_key)

instructions = """
You are agent that help with git related task. You also help in reverting chnages preformed by user.

#create brach or checkout
git_branch tool is used to crate branch and checkout branch, if branch exists already in branch then operation is succesfull.

Dont kepp using any tool consequetively for more than 3 times(Retry theresold of the tools).
Means- tool use- AAAA not valid but use AAABA valid.

#Manager agent will tell you when to commit changes.
- commit changes using git_commit_tool

## Revert Operations
- Use git_revert_tool when the user wants to revert changes.
- The user will usually provide a commit-related message.
- Check the git log to determine which commit to revert.
- Ask the user for confirmation before running git_revert_tool.

#important
-Tools wont return success or failure message, You have the understand the sentiment of tool's response with your reasoning.
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



# Define the tools
tools = [user_input_tool,
         git_branch_tool, git_commit_tool, git_log_tool, git_revert_commit_tool]


prompt = hub.pull("hwchase17/react")

git_agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt ,
)


agent_executor = AgentExecutor(
    agent=git_agent,
    tools=tools,  # ✅ Add this line
    verbose=True,
    handle_parsing_errors=True,
    # max_iterations=10,

)


def run_git_agent(response):
    params= parse_agent_response(response)
    query = params.get("query", "xyz")
    workspace=params.get("workspace","xyz")

    if query=="xyz": return "Invalid query"
    if workspace =="xyz": return "Please provide correct workspace"
    """ Use This too for git related tasks and for revrting commits or changes"""
    response = agent_executor.invoke({
        "input": prompt_template.format(query = query, workspace= workspace, instructions=instructions)
    })
    return response

git_agent = Tool(
    name= "Git agent",
    func= run_git_agent,
    description = """This is a git agent. Use this for git related tasks and revrting changes"
        Provide:
        "query": str #what needs to be done
        "workspace": str #path of workspace
    """
)
# if __name__=="__main__":

    

