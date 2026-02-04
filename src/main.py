from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI

from src.llm import LLMClient
from src.schemas import ChatRequest, ChatResponse

from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

import logging
from src.logging_config import setup_logging

from fastapi import Request, HTTPException
from src.rate_limiter import RateLimiter

# Charge les variables d'environnement depuis le fichier .env (si présent)
load_dotenv()

setup_logging()
logger = logging.getLogger("api")

app = FastAPI(title="LLM API Service", version="0.1.0")

chat_limiter = RateLimiter(max_requests=30, window_seconds=60)
stream_limiter = RateLimiter(max_requests=10, window_seconds=60)


# On instancie le client une seule fois au démarrage
llm = LLMClient()


@app.get("/health")
def health() -> dict:
    logger.info("Health check called")
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    client_ip = request.client.host

    if not chat_limiter.allow(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded for /chat",
        )

    logger.info(
        "Chat request received",
        extra={"messages_count": len(req.messages)},
    )

    content = await llm.chat(req.messages)

    logger.info(
        "Chat response sent",
        extra={"response_length": len(content)},
    )

    return ChatResponse(content=content)

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    client_ip = request.client.host

    if not stream_limiter.allow(client_ip):
        logger.warning(
            "Streaming rate limit exceeded",
            extra={"ip": client_ip},
        )
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded for /chat/stream",
        )
    
    logger.info(
        "Streaming chat started",
        extra={"messages_count": len(req.messages)},
    )

    async def token_generator():
        token_count = 0
        try:
            async for token in llm.chat_stream(req.messages):
                token_count += 1
                logger.debug("Token streamed", extra={"token_index": token_count})
                yield token
        except Exception as e:
            logger.error(
                "Streaming error",
                extra={"error": str(e)},
            )
            yield f"\n[ERREUR] {str(e)}\n"
        finally:
            logger.info("Streaming chat finished",
                        extra={"tokens_streamed": token_count},
                        )

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )

# Lancement (en terminal):
# uvicorn src.main:app --reload --port 8000
