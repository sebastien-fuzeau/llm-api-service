import asyncio

from src.llm_mock import MockLLMClient


def test_chat_mock():
    llm = MockLLMClient()

    result = asyncio.run(
        llm.chat([{"role": "user", "content": "Hello"}])
    )

    assert "[MOCK]" in result
