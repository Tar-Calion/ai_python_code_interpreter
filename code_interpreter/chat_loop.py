from code_interpreter.code_executor import PythonCodeExecutor
from code_interpreter.code_extractor import CodeExtractor
from model_client.gemini_pro import GeminiProClient
from code_interpreter.response import Response, ResponseType
from model_client.model_client import ModelClient


class ChatLoop:
    """This class represents a main chat loop that drives the conversation between the user and the model. 
    It is responsible for confirming the next prompts, calling the code interpreter and processing results.
    """

    def __init__(self, model_client: ModelClient, initial_prompt: str):
        self.client = model_client
        self.initial_prompt = initial_prompt

    def start_main_loop(self):

        additional_instructions = (
            "\nFirst, write your reasoning for the solution. Then, write the code to solve the puzzle.\n"
            "Use only Python standard libraries if possible.\n"
            "Add print() statements on key points of the code to help debugging.\n"
            "The code should be runnable without the main() method and should print the solution to the console.\n"
            "Enclose the Python code block inside of <CODE> and </CODE> tags.\n"
        )

        next_prompt = self.initial_prompt + additional_instructions

        while True:

            next_prompt = self._prepare_next_prompt(next_prompt)

            # get response from LLM
            model_response = self.client.send_message(next_prompt)

            print("Response received from the model:")
            print(model_response)

            response = self._process_response(model_response)

            if response.type == ResponseType.ANSWER:
                print("The response contains the answer. Exiting...")
                # TODO confirm exit or get another prompt from the user
                exit()
            elif response.type == ResponseType.CODE:
                next_prompt = self._process_code_block(response.text)
            else:
                print(f"Unknown response type: {response.type}. Exiting...")
                exit()

    def _prepare_next_prompt(self, next_prompt):
        # confirm with user
        print("Please confirm the following prompt:")
        print(next_prompt)
        confirmation = input("Do you want to send this prompt to the model? (y/n)\n")

        if confirmation.lower() != "y":
            print("Prompt execution not confirmed. Exiting...")
            exit()

        return next_prompt

    def _process_response(self, response) -> Response:

        if "<ANSWER>" in response:
            return Response(ResponseType.ANSWER, response)

        # extracting the code block from the response
        codeExtractor = CodeExtractor()
        code_block = codeExtractor.extract(response)

        print("Code block extracted from the response:")
        print(code_block)

        return Response(ResponseType.CODE, code_block)

    def _process_code_block(self, code_block):

        # confirm execution of the code block
        confirmation = input("Do you want to execute the code block? (y/n)\n")

        if confirmation.lower() != "y":
            print("Code block execution not confirmed. Exiting...")
            exit()

        # execute the code block
        codeExecutor = PythonCodeExecutor()
        stdout, stderr = codeExecutor.execute(code_block)

        print("Code block executed. Here is the output:")
        print(stdout)
        print("Errors:")
        print(stderr)

        if stderr:
            codeExtractor = CodeExtractor()
            error_line = codeExtractor.extract_error_line(code_block, stderr)
            return (
                "The code execution failed.\n"
                f"{"This is standard output:\n" + stdout if stdout else ""}"
                f"This is the error:\n{stderr}\n"
                f"{f'The error occurred in the following line of the code:\n{error_line}\n' if error_line else ''}"
                "Please correct the code so that it executes without errors and solves the assignment.\n"
                "You can use the print() function for debugging, then you will receive the standard output from me.\n"
                "If you are getting the same error over and over, try a different approach.\n"
                "Provide the whole corrected code between the XML tags <CODE> and </CODE>."

            )
        else:
            return (
                "The code execution succeeded.\n"
                f"{"This is standard output:\n" + stdout if stdout else ""}"
                "Please check if the result makes sense and provide the answer between the XML tags <ANSWER> and </ANSWER>.\n"
                "Otherwise correct the code and we will try again."
            )
