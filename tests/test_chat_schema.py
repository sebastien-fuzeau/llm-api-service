import pytest
from pydantic import ValidationError

from src.schemas import ChatRequest


def test_chat_request_requires_messages():
    with pytest.raises(ValidationError):
        ChatRequest()  # messages manquant


def test_chat_request_accepts_messages_list():
    req = ChatRequest(messages=[{"role": "user", "content": "Hello"}])
    assert req.messages[0]["role"] == "user"
