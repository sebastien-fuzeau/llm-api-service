from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx


class LLMClient:
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
