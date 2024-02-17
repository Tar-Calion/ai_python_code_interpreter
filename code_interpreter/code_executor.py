import io
import sys
import traceback


class PythonCodeExecutor():
    def execute(self, code: str) -> str:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        sys_stdout_original = sys.stdout
        sys_stderr_original = sys.stderr

        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer

        try:
            exec(code)
        except Exception as e:
            traceback.print_exc(file=stderr_buffer)

        sys.stdout = sys_stdout_original
        sys.stderr = sys_stderr_original

        stdout_value = stdout_buffer.getvalue()
        stderr_value = stderr_buffer.getvalue()

        return stdout_value, stderr_value
