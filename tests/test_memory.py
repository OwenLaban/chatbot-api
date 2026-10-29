"""Test unit penyimpanan memory (tanpa FastAPI)."""

import json

from app import memory
from app.models import ChatMessage


def test_ambil_pesan_session_kosong(data_file):
    assert memory.ambil_pesan("tidak-ada") == []


def test_simpan_dan_ambil_pesan(data_file):
    memory.simpan_pesan("s1", "user", "Halo")
    memory.simpan_pesan("s1", "assistant", "Hai")

    pesan = memory.ambil_pesan("s1")

    assert pesan == [
        ChatMessage(role="user", content="Halo"),
        ChatMessage(role="assistant", content="Hai"),
    ]
    data = json.loads(data_file.read_text(encoding="utf-8"))
    assert data["s1"][0] == {"role": "user", "content": "Halo"}


def test_sesi_lain_tetap_ada_setelah_hapus(data_file):
    memory.simpan_pesan("s1", "user", "Halo")
    memory.simpan_pesan("s2", "user", "Hai")

    assert memory.hapus_session("s1") is True
    assert memory.hapus_session("s1") is False
    assert memory.ambil_pesan("s1") == []
    assert memory.ambil_pesan("s2")[0].content == "Hai"
