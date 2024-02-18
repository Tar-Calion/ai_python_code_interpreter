import unittest
from unittest.mock import Mock, patch, call
from code_interpreter.chat_loop import ChatLoop
from code_interpreter.response import Response, ResponseType


class TestChatLoop(unittest.TestCase):
    def setUp(self):
        self.mock_model_client = Mock()
        self.mock_model_client.send_message.return_value = "Test model response"
        initial_prompt = "initial prompt"
        self.chat_loop = ChatLoop(self.mock_model_client, initial_prompt)

    # Test _prepare_next_prompt method
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_prepare_next_prompt_confirmed(self, mock_print, mock_input):
        next_prompt = "Test prompt"
        result = self.chat_loop._prepare_next_prompt(next_prompt)
        self.assertEqual(result, next_prompt)
        mock_print.assert_has_calls([call("Please confirm the following prompt:"), call(next_prompt)])
        mock_input.assert_called_once_with("Do you want to send this prompt to the model? (y/n)\n")

    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    @patch('builtins.exit')
    def test_prepare_next_prompt_not_confirmed(self, mock_exit, mock_print, mock_input):
        next_prompt = "Test prompt"
        self.chat_loop._prepare_next_prompt(next_prompt)
        mock_print.assert_has_calls([call("Please confirm the following prompt:"), call(
            next_prompt), call("Prompt execution not confirmed. Exiting...")])
        mock_input.assert_called_once_with("Do you want to send this prompt to the model? (y/n)\n")
        mock_exit.assert_called_once()

    # Test _process_response method
    @patch('builtins.print')
    def test_process_response_answer(self, mock_print):
        response = "<ANSWER>Test answer</ANSWER>"
        result = self.chat_loop._process_response(response)
        self.assertEqual(result.type, ResponseType.ANSWER)
        self.assertEqual(result.text, response)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_process_response_code(self, mock_print):
        response = "Here is some code: <CODE>```python\ndef hello():\n    print('Hello, world!')\n```</CODE>"
        result = self.chat_loop._process_response(response)
        self.assertEqual(result.type, ResponseType.CODE)
        self.assertEqual(result.text, "def hello():\n    print('Hello, world!')")
        mock_print.assert_has_calls([call("Code block extracted from the response:"), call("def hello():\n    print('Hello, world!')")])

    # Test _process_code_block method
    @patch('builtins.input', return_value='y')
    def test_process_code_block_successful_execution(self, mock_input):
        code_block = "print('Hello, world!')"
        result = self.chat_loop._process_code_block(code_block)
        self.assertTrue("The code execution succeeded." in result)
        mock_input.assert_called_once_with("Do you want to execute the code block? (y/n)\n")

    @patch('builtins.input', return_value='y')
    def test_process_code_block_failed_execution(self, mock_input):
        code_block = "print(Hello, world!)"  # This code will cause a SyntaxError
        result = self.chat_loop._process_code_block(code_block)
        self.assertTrue("The code execution failed." in result)
        mock_input.assert_called_once_with("Do you want to execute the code block? (y/n)\n")

    @patch('builtins.input', return_value='n')
    @patch('builtins.exit')
    def test_process_code_block_not_confirmed(self, mock_exit, mock_input):
        code_block = "print('Hello, world!')"
        self.chat_loop._process_code_block(code_block)
        mock_input.assert_called_once_with("Do you want to execute the code block? (y/n)\n")
        mock_exit.assert_called_once()

    # Test start_main_loop method
    @patch.object(ChatLoop, '_prepare_next_prompt', return_value="Prepared prompt")
    @patch.object(ChatLoop, '_process_response', return_value=Response(type=ResponseType.ANSWER, text="Test answer"))
    @patch.object(ChatLoop, '_process_code_block', return_value="Processed code block")
    def test_start_main_loop_answer_response(self, mock_process_code_block, mock_process_response, mock_prepare_next_prompt):

        with self.assertRaises(SystemExit):
            self.chat_loop.start_main_loop()

        mock_prepare_next_prompt.assert_called_once()
        self.mock_model_client.send_message.assert_called_once_with("Prepared prompt")
        mock_process_response.assert_called_once_with("Test model response")
        mock_process_code_block.assert_not_called()

    @patch.object(ChatLoop, '_prepare_next_prompt', return_value="Prepared prompt")
    @patch.object(ChatLoop, '_process_response', return_value=Response(type=ResponseType.CODE, text="Test code block"))
    @patch.object(ChatLoop, '_process_code_block', return_value="Processed code block")
    def test_start_main_loop_code_response(self, mock_process_code_block, mock_process_response, mock_prepare_next_prompt):
        # _process_code_block will raise SystemExit
        mock_process_code_block.side_effect = SystemExit

        with self.assertRaises(SystemExit):
            self.chat_loop.start_main_loop()

        mock_prepare_next_prompt.assert_called_once()
        self.mock_model_client.send_message.assert_called_once_with("Prepared prompt")
        mock_process_response.assert_called_once_with("Test model response")
        mock_process_code_block.assert_called_once_with("Test code block")

    @patch.object(ChatLoop, '_prepare_next_prompt', return_value="Prepared prompt")
    @patch.object(ChatLoop, '_process_response', return_value=Response(type=None, text="Unknown response"))
    @patch.object(ChatLoop, '_process_code_block', return_value="Processed code block")
    def test_start_main_loop_unknown_response(self, mock_process_code_block, mock_process_response, mock_prepare_next_prompt):
        with self.assertRaises(SystemExit):
            self.chat_loop.start_main_loop()
        mock_prepare_next_prompt.assert_called_once()
        self.mock_model_client.send_message.assert_called_once_with("Prepared prompt")
        mock_process_response.assert_called_once_with("Test model response")
        mock_process_code_block.assert_not_called()


if __name__ == '__main__':
    unittest.main()
