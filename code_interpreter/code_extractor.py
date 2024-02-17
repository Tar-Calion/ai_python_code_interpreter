import re


class CodeExtractor:

    def extract(self, markdown: str):
        # Check if there is more than one code block in the markdown
        if markdown.count("<CODE>") > 1:
            raise ValueError("More than one code block found in the markdown text")

        # Extract the code between <CODE> and </CODE> from the markdown
        code_match = re.search(r'<CODE>([\s\S]*)</CODE>', markdown)

        # If there is no <CODE> in the text, throw an error
        if code_match is None:
            raise ValueError("No code block found in the markdown text")

        # Extract the code between the <CODE> and </CODE> tags
        code_block = code_match.group(1).strip()

        # remove optional ```python\n and \n``` from the code block
        code_block = re.sub(r'```python', '', code_block)
        code_block = re.sub(r'```', '', code_block)

        return code_block.strip()

    def extract_error_line(self, code, stderr: str):
        # Extract the line number from the error message
        line_number_match = re.search(r'File "<string>", line (\d+)', stderr)

        # If there is no line number in the error message, return None
        if line_number_match is None:
            return None

        # Extract the line number from the error message
        line_number = int(line_number_match.group(1))

        # Extract the line from the code block
        code_lines = code.split("\n")
        error_line = code_lines[line_number - 1]

        return error_line
