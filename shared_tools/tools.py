from langchain.tools import Tool

def user_input(text):
    print(text, end="-> ")
    inp = input()
    return inp


user_input_tool = Tool(
    name="take_user_input",
    func=user_input,
    description="This tool can be used to take input from user",
)