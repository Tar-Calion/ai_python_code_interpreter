

import os
from code_interpreter.chat_loop import ChatLoop

# project_name = input("Enter project name: ")
project_name = "aoc_2015_day6_part2"

# create project directory if it doesn't exist
project_dir = "projects/" + project_name
os.makedirs(project_dir, exist_ok=True)

print("Project directory created")
print("Please save the puzzle in " + project_dir + "/puzzle.txt and the input file in " + project_dir + "/input.txt")

# input("Press any key to continue...")

# read puzzle and input files
with open(project_dir + "/puzzle.txt", "r") as f:
    puzzle = f.read()

whole_input_data = ""
with open(os.path.join(project_dir, "input.txt"), "r") as f:
    whole_input_data = f.read()

# get 10 lines of the input data as string
input_data_excerpt = ""
with open(os.path.join(project_dir, "input.txt"), "r") as f:
    for i in range(10):
        input_data_excerpt += f.readline()

# check puzzle and input data exists
if not puzzle:
    print("Puzzle not found. Please save the puzzle in " + project_dir + "/puzzle.txt")
    exit()

if not whole_input_data:
    print("Input data not found. Please save the input data in " + project_dir + "/input.txt")
    exit()


initial_prompt = f"""We want to solve the following puzzle using Python code. Here is the puzzle:
<PUZZLE>
{puzzle}
</PUZZLE>

The code should load the input from the file "{project_dir}/input.txt". Here is the extract from that file:
<INPUT DATA EXCERPT>
{input_data_excerpt}
</INPUT DATA EXCERPT>
"""

chat_loop = ChatLoop()
chat_loop.main_loop(initial_prompt)