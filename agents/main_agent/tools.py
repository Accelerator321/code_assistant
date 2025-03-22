from db import search_code,retrieval_chain
from langchain.tools import Tool
from utils.utils import apply_changes, read_file




read_file_tool = Tool(
    name="read_file_tool",
    func=read_file,
    description="""Reads the file and retunr its content. provide it the path of file.
    Provide:
        "file_path": str #path of the file.
    """
)



search_tool = Tool(
    name="search_code",
    func=retrieval_chain.run,
    description="""Retrieves relevant code chunks based on the query. Its a retreival chain.
        
    """
)



file_modification_tool = Tool(
    name="file_modification_tool",
    func=apply_changes,
    description="""Applies code changes to user files.Necessary to ask user consent before applying.
    Never apply chnages without user consent
    provide:
    

           
                    "filepath": str,  # Path to the file being modified (full path)
                    "modification": str,  # New code 
                    
                "query":str # initial user query

    """
)


# "actual_code": str  # The original code that was replaced entire line.
#                                         return actaul code as it isa you read dont remove DELIMITER
#                     "start"
#                     : int,   # Start line number of actual code( return i of first occurance <Delim-line-i> in actual_code)
#                     "end": int,     # End line number actual code ( return j of last ocuurance <Delim-line-j> in actual_code)




