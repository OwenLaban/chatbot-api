import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def data_file(tmp_path, monkeypatch):
    """Arahkan memory ke file sementara supaya test tidak saling bocor."""
    path = tmp_path / "conversations.json"
    monkeypatch.setenv("CHATBOT_DATA_FILE", str(path))
    return path


@pytest.fixture()
def client(data_file):
    from app.main import app

    return TestClient(app)
