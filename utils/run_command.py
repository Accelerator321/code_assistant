import subprocess

import os
def run_command(command):
    command = command.replace("\\","/")
    print(command)
    # return "y"
    output_file = os.popen(command)

    output = output_file.read()

    output_file.close()

    # Display the output
    
    return output

# Example usage:

if __name__ =="__main__":
    cmd = r'git -C "D:\code assistant\react-tw-sample" branch -a | findstr "code_assistant_123"'
    print(run_command(cmd))  # Runs 'git --version'
