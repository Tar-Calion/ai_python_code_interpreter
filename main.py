# This script starts a chat with the LLM where you can solve a problem using Python code.
# The code that LLM generates is executed and the result is shown to the user.
# In case of an error, the error message is provided to the LLM with the request to fix the code.
# The chat continues until the code executes successfully and the LLM confirms the solution (in <ANSWER></ANSWER> tags).

from code_interpreter.chat_loop import ChatLoop
from model_client.gemini_pro import GeminiProClient

assignment = input("Enter the assignment:\n")

chat_loop = ChatLoop(GeminiProClient(), assignment)
chat_loop.start_main_loop()
