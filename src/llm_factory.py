import os

from src.llm import LLMClient
from src.llm_mock import MockLLMClient
from src.llm_base import BaseLLMClient


def create_llm_client() -> BaseLLMClient:
    mode = os.getenv("LLM_MODE", "real").lower()

    if mode == "mock":
        return MockLLMClient()

    return LLMClient()
