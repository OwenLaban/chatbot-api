"""Test API chatbot. LLM selalu di-mock supaya tidak butuh API key."""

import json

from app.models import ChatResponse


def _jawaban(pesan: str) -> ChatResponse:
    return ChatResponse(
        balasan=f"Echo: {pesan}",
        topik="umum",
        sentimen="netral",
        butuh_eskalasi=False,
    )


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_mengembalikan_structured_output(client, monkeypatch):
    monkeypatch.setattr("app.main.balas", lambda history, pesan: _jawaban(pesan))

    response = client.post(
        "/chat", json={"session_id": "s1", "message": "Halo"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "balasan": "Echo: Halo",
        "topik": "umum",
        "sentimen": "netral",
        "butuh_eskalasi": False,
    }


def test_chat_menyimpan_memory(client, monkeypatch):
    monkeypatch.setattr("app.main.balas", lambda history, pesan: _jawaban(pesan))

    client.post("/chat", json={"session_id": "s1", "message": "Halo"})
    response = client.get("/sessions/s1")

    assert response.status_code == 200
    assert response.json() == {
        "session_id": "s1",
        "messages": [
            {"role": "user", "content": "Halo"},
            {"role": "assistant", "content": "Echo: Halo"},
        ],
    }


def test_chat_mengirim_history_sebelumnya(client, monkeypatch):
    panggilan = []

    def fake_balas(history, pesan):
        panggilan.append((history, pesan))
        return _jawaban(pesan)

    monkeypatch.setattr("app.main.balas", fake_balas)

    client.post("/chat", json={"session_id": "s1", "message": "Halo"})
    client.post("/chat", json={"session_id": "s1", "message": "Siapa aku?"})

    assert len(panggilan) == 2
    assert len(panggilan[0][0]) == 0

    history_kedua = panggilan[1][0]
    assert [(m.role, m.content) for m in history_kedua] == [
        ("user", "Halo"),
        ("assistant", "Echo: Halo"),
    ]


def test_session_terisolasi(client, monkeypatch):
    monkeypatch.setattr("app.main.balas", lambda history, pesan: _jawaban(pesan))

    client.post("/chat", json={"session_id": "s1", "message": "Halo dari S1"})
    client.post("/chat", json={"session_id": "s2", "message": "Halo dari S2"})

    s1 = client.get("/sessions/s1").json()["messages"]
    s2 = client.get("/sessions/s2").json()["messages"]

    assert s1[0]["content"] == "Halo dari S1"
    assert s2[0]["content"] == "Halo dari S2"


def test_session_tidak_ditemukan(client):
    response = client.get("/sessions/tidak-ada")
    assert response.status_code == 404


def test_hapus_session(client, monkeypatch):
    monkeypatch.setattr("app.main.balas", lambda history, pesan: _jawaban(pesan))
    client.post("/chat", json={"session_id": "s1", "message": "Halo"})

    response = client.delete("/sessions/s1")

    assert response.status_code == 200
    assert response.json() == {"status": "deleted", "session_id": "s1"}
    assert client.get("/sessions/s1").status_code == 404
    assert client.delete("/sessions/s1").status_code == 404


def test_validasi_input(client):
    kosong = client.post("/chat", json={"session_id": "s1", "message": ""})
    tanpa_session = client.post("/chat", json={"message": "Halo"})

    assert kosong.status_code == 422
    assert tanpa_session.status_code == 422


def test_memory_tersimpan_di_file(client, monkeypatch, data_file):
    monkeypatch.setattr("app.main.balas", lambda history, pesan: _jawaban(pesan))
    client.post("/chat", json={"session_id": "s1", "message": "Halo"})

    assert data_file.exists()
    data = json.loads(data_file.read_text(encoding="utf-8"))
    assert data["s1"] == [
        {"role": "user", "content": "Halo"},
        {"role": "assistant", "content": "Echo: Halo"},
    ]
