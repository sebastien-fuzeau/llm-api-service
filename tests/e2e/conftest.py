import os
import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="session", autouse=True)
def set_mock_mode():
    """
    Force le LLM en mode mock pour tous les tests E2E.
    """
    os.environ["LLM_MODE"] = "mock"
    yield
    os.environ.pop("LLM_MODE", None)


@pytest.fixture(scope="session")
def client():
    """
    Client HTTP FastAPI pour tests end-to-end.
    """
    return TestClient(app)
