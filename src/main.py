from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI

from src.llm import LLMClient
from src.schemas import ChatRequest, ChatResponse

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

# Lancement (en terminal):
# uvicorn src.main:app --reload --port 8000
