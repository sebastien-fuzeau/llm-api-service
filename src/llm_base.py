from typing import Any, Dict, List, AsyncGenerator
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    async def chat_stream(
            self, messages: List[Dict[str, Any]]
    ) -> AsyncGenerator[str, None]:
        pass
