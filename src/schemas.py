from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]] = Field(
        ...,
        description="Liste de messages {role, content} (format OpenAI-compatible).",
        examples=[
            [
                {"role": "system", "content": "Tu es un assistant utile."},
                {"role": "user", "content": "Bonjour !"},
            ]
        ],
    )


class ChatResponse(BaseModel):
    content: str = Field(..., description="Texte de réponse généré par le modèle.")
