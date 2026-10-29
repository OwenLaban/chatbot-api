"""Test klien LLM tanpa memanggil jaringan."""

from types import SimpleNamespace

import pytest

from app import llm
from app.models import ChatMessage


class FakeCompletions:
    def __init__(self, content: str):
        self.content = content
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))]
        )


class FakeClient:
    def __init__(self, content: str):
        self.chat = SimpleNamespace(completions=FakeCompletions(content))


def test_client_tanpa_api_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="LLM_API_KEY"):
        llm._client()


def test_client_memakai_env(monkeypatch):
    import openai

    dibuat = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            dibuat.update(kwargs)

    monkeypatch.setenv("LLM_API_KEY", "kunci-uji")
    monkeypatch.setenv("LLM_BASE_URL", "https://contoh.test/v1")
    monkeypatch.setattr(openai, "OpenAI", FakeOpenAI)

    client = llm._client()

    assert isinstance(client, FakeOpenAI)
    assert dibuat == {
        "base_url": "https://contoh.test/v1",
        "api_key": "kunci-uji",
    }


def test_balas_mengirim_history_dan_memvalidasi_json(monkeypatch):
    fake = FakeClient(
        '{"balasan": "Hai", "topik": "umum", '
        '"sentimen": "positif", "butuh_eskalasi": false}'
    )
    monkeypatch.setattr(llm, "_client", lambda: fake)

    hasil = llm.balas([ChatMessage(role="user", content="Halo")], "Apa kabar?")

    assert hasil.balasan == "Hai"
    assert hasil.topik == "umum"
    assert hasil.sentimen == "positif"
    assert hasil.butuh_eskalasi is False

    messages = fake.chat.completions.kwargs["messages"]
    assert messages[0]["role"] == "system"
    assert messages[1] == {"role": "user", "content": "Halo"}
    assert messages[2] == {"role": "user", "content": "Apa kabar?"}
    assert fake.chat.completions.kwargs["model"] == llm.os.getenv(
        "LLM_MODEL", llm.MODEL_DEFAULT
    )


def test_balas_menolak_output_bukan_json(monkeypatch):
    monkeypatch.setattr(llm, "_client", lambda: FakeClient("bukan json"))

    with pytest.raises(ValueError):
        llm.balas([], "Halo")
