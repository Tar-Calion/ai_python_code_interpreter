import unittest
from code_interpreter.code_executor import PythonCodeExecutor


class TestPythonCodeExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = PythonCodeExecutor()

    def test_execute_no_output(self):
        code = "a = 1"
        stdout, stderr = self.executor.execute(code)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")

    def test_execute_with_stdout(self):
        code = "print('Hello, world!')"
        stdout, stderr = self.executor.execute(code)
        self.assertEqual(stdout, "Hello, world!\n")
        self.assertEqual(stderr, "")

    def test_execute_with_stderr(self):
        code = "import sys; print('Hello, world!', file=sys.stderr)"
        stdout, stderr = self.executor.execute(code)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "Hello, world!\n")

    def test_execute_with_exception(self):
        code = "def test_function():\n    raise ValueError('An error occurred')\ntest_function()"
        stdout, stderr = self.executor.execute(code)
        self.assertEqual(stdout, "")
        self.assertTrue(stderr.endswith("ValueError: An error occurred\n"))

    def test_execute_with_nested_exception(self):
        code = "try:\n    raise ValueError('An error occurred')\nexcept Exception as e:\n    raise ValueError('Another error occurred')"
        stdout, stderr = self.executor.execute(code)
        self.assertEqual(stdout, "")
        self.assertTrue(stderr.find("ValueError: An error occurred") != -1)
        self.assertTrue(stderr.endswith("ValueError: Another error occurred\n"))


if __name__ == '__main__':
    unittest.main()
