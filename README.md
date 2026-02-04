# llm-api-service

API FastAPI minimaliste qui expose un endpoint `/chat` pour appeler un LLM
(OpenAI-compatible) et un endpoint `/health` pour vérifier que le service tourne.

## Pré-requis
- Python 3.11+

## Setup
```bash
python -m venv .venv
source .venv/Scripts/activate   # Git Bash / Windows
pip install -U pip
pip install -e ".[dev]"
cp .env.example .env
# mets ta clé OPENAI_API_KEY dans .env
