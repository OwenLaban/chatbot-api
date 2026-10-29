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
    """Baca seluruh isi file memory.

    TODO:
    1. Ambil path dari _path_data().
    2. Jika file belum ada, kembalikan {}.
    3. Baca teksnya, lalu json.loads.
    4. Kembalikan dict tersebut.
    """
    raise NotImplementedError("TODO: implementasikan _baca_semua()")


def _tulis_semua(data: dict[str, list[dict[str, str]]]) -> None:
    """Tulis seluruh data ke file JSON.

    TODO:
    1. Ambil path dari _path_data().
    2. Buat folder induknya: path.parent.mkdir(parents=True, exist_ok=True).
    3. Tulis dengan json.dumps(..., indent=2, ensure_ascii=False).
       Gunakan encoding="utf-8".
    """
    raise NotImplementedError("TODO: implementasikan _tulis_semua()")


def ambil_pesan(session_id: str) -> list[ChatMessage]:
    """Kembalikan riwayat pesan sebuah sesi.

    TODO:
    1. data = _baca_semua()
    2. Ambil data.get(session_id, []).
    3. Ubah setiap dict menjadi ChatMessage(**pesan).
    """
    raise NotImplementedError("TODO: implementasikan ambil_pesan()")


def simpan_pesan(
    session_id: str,
    role: Literal["user", "assistant"],
    content: str,
) -> None:
    """Tambahkan satu pesan ke sesi, lalu simpan ke file.

    TODO:
    1. data = _baca_semua()
    2. data.setdefault(session_id, []).append({"role": role, "content": content})
    3. _tulis_semua(data)
    """
    raise NotImplementedError("TODO: implementasikan simpan_pesan()")


def hapus_session(session_id: str) -> bool:
    """Hapus satu sesi. Kembalikan True jika ada, False jika tidak ada.

    TODO:
    1. data = _baca_semua()
    2. Jika session_id tidak ada, kembalikan False.
    3. Hapus key-nya, panggil _tulis_semua(data), kembalikan True.
    """
    raise NotImplementedError("TODO: implementasikan hapus_session()")
