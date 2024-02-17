from vertexai.preview.generative_models import GenerativeModel


class GeminiProClient:
    """Client for interacting with the Gemini Pro model."""

    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat()

    def __calculate_history_size(self) -> int:
        return sum(len(content.parts[0].text) for content in self.chat.history)

    def send_message(self, prompt: str) -> str:
        """Send a message to the model and return its response."""
        if not prompt:
            raise ValueError("Prompt cannot be empty or None")

        config = {
            "max_output_tokens": 4000,
            "temperature": 0.9,
            "top_p": 1
        }

        response = self.chat.send_message(prompt, generation_config=config)

        response_text = response.candidates[0].content.parts[0].text

        print(f"History messages count: {len(self.chat.history)}")
        print(f"History messages size: {self.__calculate_history_size()}")

        return response_text
