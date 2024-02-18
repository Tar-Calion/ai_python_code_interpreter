from code_interpreter.code_executor import PythonCodeExecutor
from code_interpreter.code_extractor import CodeExtractor
from model_client.gemini_pro import GeminiProClient
from code_interpreter.response import Response, ResponseType
from model_client.model_client import ModelClient


class ChatLoop:
    """This class represents a main chat loop that drives the conversation between the user and the model. 
    It is responsible for confirming the next prompts, calling the code interpreter and processing results.
    """

    def __init__(self, model_client: ModelClient, assignment: str):
        self.client = model_client
        self.assignment = assignment

    def start_main_loop(self):
        introduction = "Here is your assignment:\n<ASSIGNMEN>\n"

        additional_instructions = (
            "\n</ASSIGNMENT>\n"
            "First, write your reasoning for the solution. Then, write the code to solve the assignment.\n"
            "Use only Python standard libraries if possible.\n"
            "The code should be runnable without the main() method and should print the solution to the console.\n"
            "Enclose the Python code block inside of <CODE> and </CODE> XML tags.\n"
        )

        next_prompt = introduction + self.assignment + additional_instructions

        while True:

            next_prompt = self._prepare_next_prompt(next_prompt)

            # get response from LLM
            model_response = self.client.send_message(next_prompt)

            print("\nResponse received from the model:")
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
        print("\nPlease confirm the following prompt:")
        print(next_prompt)
        confirmation = input("Do you want to send this prompt to the model? (y/n/<your additional instructions>)\n")

        if confirmation.lower() == "y":
            return next_prompt
        elif confirmation.lower() == "n":
            print("Prompt execution not confirmed. Exiting...")
            exit()
        else:
            print(f"Additional instructions added to the prompt: {confirmation}")
            return next_prompt + "\nAdditional instructions added by the user: " + confirmation

    def _process_response(self, response) -> Response:

        if "<ANSWER>" in response:
            return Response(ResponseType.ANSWER, response)

        # extracting the code block from the response
        codeExtractor = CodeExtractor()
        code_block = codeExtractor.extract(response)

        print("\nCode block extracted from the response:")
        print(code_block)

        return Response(ResponseType.CODE, code_block)

    def _format_standard_output(self, stdout):
        return f"This is standard output of the code:\n<STANDARD_OUTPUT>\n{stdout}\n</STANDARD_OUTPUT>\n"

    def _format_error_output(self, stderr):
        return f"This is the error:\n<ERROR>\n{stderr}\n</ERROR>\n"

    def _process_code_block(self, code_block):

        # confirm execution of the code block
        confirmation = input("\nDo you want to execute the code block? (y/n)\n")

        if confirmation.lower() != "y":
            print("Code block execution not confirmed. Exiting...")
            exit()

        # execute the code block
        codeExecutor = PythonCodeExecutor()
        stdout, stderr = codeExecutor.execute(code_block)

        print("\nCode block executed. Here is the output:")
        print(stdout)
        print("Errors:")
        print(stderr)

        if stderr:
            codeExtractor = CodeExtractor()
            error_line = codeExtractor.extract_error_line(code_block, stderr)
            return (
                "The code execution failed.\n"
                f"{self._format_standard_output(stdout) if stdout else ""}"
                f"{self._format_error_output(stderr)}"
                f"{f'The error occurred in the following line of the code:\n{error_line}\n' if error_line else ''}"
                "Please provide the whole corrected code between the XML tags <CODE> and </CODE>."

            )
        else:
            return (
                "The code execution succeeded.\n"
                f"{self._format_standard_output(stdout)}"
                "Please provide the answer to the assignment between the XML tags <ANSWER> and </ANSWER>.\n"
                "If you think the answer is not correct, please provide the corrected code between the XML tags <CODE> and </CODE> instead."
            )
