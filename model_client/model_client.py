class ModelClient:
    """Abstract client for interacting with a generative model."""

    def send_message(self, prompt: str) -> str:
        """Send a message to the model and return its response."""
        pass
