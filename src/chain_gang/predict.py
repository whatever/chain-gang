import os

from llama_cpp import Llama
from typing import Any


MODEL_PATH = os.getenv("LLAMA_MODEL_PATH")


class LlamaPredictor(object):
    """Llama Predictor"""

    def __init__(self):
        """..."""

        self.llama = Llama(
            model_path=MODEL_PATH,
            chat_format="chatml",
            verbose=False,
        )

    def generate(self, text: str) -> Any:
        """Return a response"""
        return self.llama(text)
