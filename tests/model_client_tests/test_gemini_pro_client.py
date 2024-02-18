import unittest
from unittest.mock import Mock, MagicMock
from model_client.gemini_pro import GeminiProClient
from vertexai.preview.generative_models import GenerationResponse


class TestGeminiProClient(unittest.TestCase):
    def setUp(self):
        self.client = GeminiProClient()
        self.client.chat = Mock()

    def test_send_message_empty_prompt(self):
        with self.assertRaises(ValueError):
            self.client.send_message('')

    def test_send_message_none_prompt(self):
        with self.assertRaises(ValueError):
            self.client.send_message(None)

    def test_send_message_valid_prompt(self):
        mock_response = MagicMock()
        mock_response.candidates[0].content.parts[0].text = 'Mock response'
        self.client.chat.send_message.return_value = mock_response
        mock_message = MagicMock()
        mock_message.parts[0].text = 'Mock message'
        self.client.chat.history = [mock_message] * 10

        response = self.client.send_message('Hello')

        self.assertEqual(response, 'Mock response')
        self.client.chat.send_message.assert_called_once_with('Hello', generation_config={
            "max_output_tokens": 4000,
            "temperature": 0.9,
            "top_p": 1
        })


if __name__ == '__main__':
    unittest.main()
