import unittest
from code_interpreter.code_extractor import CodeExtractor


class TestCodeExtractor(unittest.TestCase):
    def test_extract_no_code_block(self):
        markdown = "This is a markdown text without a code block."
        extractor = CodeExtractor()
        with self.assertRaises(ValueError) as context:
            extractor.extract(markdown)
        self.assertTrue("No code block found in the markdown text" in str(context.exception))

    def test_extract_multiple_code_blocks(self):
        markdown = "<CODE>```python\nprint('Hello, world!')\n```</CODE>\nSome text\n<CODE>```python\nprint('Goodbye, world!')\n```</CODE>"
        extractor = CodeExtractor()
        with self.assertRaises(ValueError) as context:
            extractor.extract(markdown)
        self.assertTrue("More than one code block found in the markdown text" in str(context.exception))

    def test_extract_single_code_block(self):
        markdown = "Some text\n<CODE>\n```python\nprint('Hello, world!')\n```</CODE>\nSome more text"
        extractor = CodeExtractor()
        code_block = extractor.extract(markdown)
        self.assertEqual(code_block, "print('Hello, world!')")

    def test_extract_single_code_block_without_backticks(self):
        markdown = "Some text\n<CODE>print('Hello, world!')</CODE>\nSome more text"
        extractor = CodeExtractor()
        code_block = extractor.extract(markdown)
        self.assertEqual(code_block, "print('Hello, world!')")

    def test_extract_multiple_backticks_inside_code_block(self):
        markdown = "Some text\n<CODE>```python\nprint('Hello, world!')```\nOther block:```python print()```</CODE>\nSome more text"
        extractor = CodeExtractor()
        code_block = extractor.extract(markdown)
        self.assertEqual(code_block, "print('Hello, world!')\nOther block: print()")

    def test_extract_error_line_no_error(self):
        extractor = CodeExtractor()
        code = "print('Hello, world!')"
        stderr = ""
        error_line = extractor.extract_error_line(code, stderr)
        self.assertIsNone(error_line)

    def test_extract_error_line_no_line_number(self):
        extractor = CodeExtractor()
        code = "print('Hello, world!')\nraise ValueError('An error occurred')"
        stderr = "Traceback (most recent call last):\n  File \"<string>\", in <module>\nValueError: An error occurred"
        error_line = extractor.extract_error_line(code, stderr)
        self.assertIsNone(error_line)

    def test_extract_error_line_with_error(self):
        extractor = CodeExtractor()
        code = "print('Hello, world!')\nraise ValueError('An error occurred')"
        stderr = "Traceback (most recent call last):\n  File \"<string>\", line 2, in <module>\nValueError: An error occurred"
        error_line = extractor.extract_error_line(code, stderr)
        self.assertEqual(error_line, "raise ValueError('An error occurred')")

    def test_extract_error_line_with_multiple_lines(self):
        extractor = CodeExtractor()
        code = "print('Hello, world!')\nprint('Another line')\nraise ValueError('An error occurred')"
        stderr = "Traceback (most recent call last):\n  File \"<string>\", line 3, in <module>\nValueError: An error occurred"
        error_line = extractor.extract_error_line(code, stderr)
        self.assertEqual(error_line, "raise ValueError('An error occurred')")


if __name__ == '__main__':
    unittest.main()
