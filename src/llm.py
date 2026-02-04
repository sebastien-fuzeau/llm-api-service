from __future__ import annotations

from src.llm_base import BaseLLMClient

import os
from typing import Any, Dict, List, Optional

import httpx
import json

import logging

logger = logging.getLogger("llm")

class LLMClient(BaseLLMClient):
    """
    Client minimal pour un endpoint OpenAI-compatible Chat Completions.
    Variables d'environnement utilisées :
      - OPENAI_API_KEY (obligatoire)
      - MODEL (défaut: gpt-4.1-mini)
      - OPENAI_BASE_URL (défaut: https://api.openai.com/v1)
      - REQUEST_TIMEOUT_SECONDS (défaut: 30)
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: Optional[str] = None,
            base_url: Optional[str] = None,
            timeout_seconds: Optional[float] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL", "gpt-4.1-mini")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        timeout_env = os.getenv("REQUEST_TIMEOUT_SECONDS", "30")
        self.timeout_seconds = timeout_seconds if timeout_seconds is not None else float(timeout_env)

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY manquant (mets-le dans .env)")

    async def chat(self, messages: List[Dict[str, Any]]) -> str:
        logger.info("LLM response received")
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": self.model, "messages": messages}

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            res = await client.post(url, headers=headers, json=payload)

            # Gestion “claire” des erreurs fréquentes
            if res.status_code == 401:
                raise RuntimeError("401 Unauthorized: clé API invalide ou non autorisée.")
            if res.status_code == 429:
                raise RuntimeError("429 Too Many Requests: quota/crédits insuffisants ou rate limit.")
            if res.status_code >= 400:
                raise RuntimeError(f"Erreur API {res.status_code}: {res.text}")

            data = res.json()

        return data["choices"][0]["message"]["content"]

    async def chat_stream(self, messages: List[Dict[str, Any]]):
        """
        Stream les tokens de réponse un par un depuis l'API LLM.
        Cette méthode est un générateur asynchrone.
        """
        logger.info("LLM streaming started", extra={"model": self.model})
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,  # 🔑 activation du streaming côté API
        }

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                    "POST", url, headers=headers, json=payload
            ) as response:

                if response.status_code == 401:
                    raise RuntimeError("401 Unauthorized")
                if response.status_code == 429:
                    raise RuntimeError("429 Rate limit / quota")
                if response.status_code >= 400:
                    raise RuntimeError(
                        f"Erreur API {response.status_code}"
                    )

                async for line in response.aiter_lines():
                    if not line or not line.startswith("data:"):
                        continue

                    data = line.removeprefix("data: ").strip()

                    if data == "[DONE]":
                        break

                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"]

                    if "content" in delta:
                        yield delta["content"]
        logger.info("LLM streaming finished")