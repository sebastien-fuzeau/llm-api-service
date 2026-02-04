from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI

from src.llm import LLMClient
from src.schemas import ChatRequest, ChatResponse

from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

# Charge les variables d'environnement depuis le fichier .env (si présent)
load_dotenv()

app = FastAPI(title="LLM API Service", version="0.1.0")

# On instancie le client une seule fois au démarrage
llm = LLMClient()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    content = await llm.chat(req.messages)
    return ChatResponse(content=content)

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def token_generator() -> AsyncGenerator[str, None]:
        try:
            async for token in llm.chat_stream(req.messages):
                yield token
        except Exception as e:
            yield f"\n[ERREUR] {str(e)}\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )

# Lancement (en terminal):
# uvicorn src.main:app --reload --port 8000
