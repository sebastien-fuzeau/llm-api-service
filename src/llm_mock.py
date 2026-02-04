import asyncio
from typing import Any, Dict, List, AsyncGenerator

from src.llm_base import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    """
    LLM simulé pour le développement, les tests et la CI.
    """

    async def chat(self, messages: List[Dict[str, Any]]) -> str:
        user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        return f"[MOCK] Réponse simulée à: {user_msg}"

    async def chat_stream(
            self, messages: List[Dict[str, Any]]
    ) -> AsyncGenerator[str, None]:
        text = await self.chat(messages)
        for word in text.split():
            await asyncio.sleep(0.5)  # simule latence
            yield word + " "
