# AI Python Code Interpreter
This project provides a simple terminal-based chat interface for solving problems that require code execution. The code is generated by a large language model (currently only Gemini Pro is supported) and executed on the user's machine. Each prompt and code execution need to be approved by the user. Errors during code execution are reported to the LLM, which is then asked to generate a new solution. You can also guide the LLM by providing additional information in each chat prompt (useful when the LLM is stuck in a loop). 

## ATTENTION
The code generated by the LLM is not safe and should be reviewed before execution. The LLM may generate code that is harmful to your computer.

## Installation
You need to log in to Google Cloud to use the Gemini Pro model. You can do this by running the following command in the terminal:
```bash
gcloud auth application-default login
```

## General Code Interpreter Chat
Run ``main.py`` to start a simple chat with the code interpreter. You will be asked to provide the text of the assignment.

## Use Case: Advent of Code Puzzle Solver
This use case is an example of how the code interpreter can be used for more complex problems that require specific prompt or input data. 

It is optimized for the [Advent of Code](https://adventofcode.com/) project, which is a series of small programming puzzles.

The main entry point for the project is the ``advent_of_code_solver.py`` script. This script prompts the user for a project name, creates a directory for the project, and reads the puzzle and input data from text files in the project directory. 


## Known Issues
- The LLM may stuck in a loop and return the same output over and over again.
- The LLM may lie and give a halucinated solution.
- Gemini Pro is not very good at following instructions and coding.

## Further Development
- Save the chat history and the generated code files in project directories
- Support different LLM clients
- Reduce chat context when it is getting too long
- Modus with auto-confirmation
- Produce multiple solutions and compare them
- Detect an infinite loop and reset the chat
- Handle invalid responses (nether code nor answer)
- Double-check the answer with a smarter model

