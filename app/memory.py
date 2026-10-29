"""Penyimpanan memory percakapan berbasis file JSON.

Satu file menyimpan semua sesi:

    {
      "demo-1": [
        {"role": "user", "content": "Halo"},
        {"role": "assistant", "content": "Hai! Ada yang bisa dibantu?"}
      ]
    }
"""

import json
import os
from pathlib import Path
from typing import Literal

from app.models import ChatMessage

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "conversations.json"


def _path_data() -> Path:
    """Lokasi file memory. Bisa dioverride lewat env CHATBOT_DATA_FILE."""
    return Path(os.getenv("CHATBOT_DATA_FILE", str(DEFAULT_DATA_FILE)))


def _baca_semua() -> dict[str, list[dict[str, str]]]:
    """Baca seluruh isi file memory. Kembalikan {} jika file belum ada."""
    path = _path_data()
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _tulis_semua(data: dict[str, list[dict[str, str]]]) -> None:
    """Tulis seluruh data ke file JSON, buat folder induk bila perlu."""
    path = _path_data()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ambil_pesan(session_id: str) -> list[ChatMessage]:
    """Kembalikan riwayat pesan sebuah sesi."""
    data = _baca_semua()
    pesan_list = data.get(session_id, [])
    return [ChatMessage(**pesan) for pesan in pesan_list]


def simpan_pesan(
    session_id: str,
    role: Literal["user", "assistant"],
    content: str,
) -> None:
    """Tambahkan satu pesan ke sesi, lalu simpan ke file."""
    data = _baca_semua()
    data.setdefault(session_id, []).append({"role": role, "content": content})
    _tulis_semua(data)


def hapus_session(session_id: str) -> bool:
    """Hapus satu sesi. Kembalikan True jika ada, False jika tidak ada."""
    data = _baca_semua()
    if session_id not in data:
        return False

    del data[session_id]
    _tulis_semua(data)
    return True
