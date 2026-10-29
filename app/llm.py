"""Klien LLM OpenAI-compatible.

Default provider: OpenRouter (https://openrouter.ai) dengan model gratis.
Konfigurasi lewat environment:

    LLM_BASE_URL=https://openrouter.ai/api/v1
    LLM_API_KEY=...
    LLM_MODEL=recursive/flint-v1.0:free

Catatan: `openrouter/free` adalah auto-router dan bisa memilih model non-chat
(misalnya model safety yang membalas "User Safety: safe"). Untuk tugas JSON,
pakai model chat gratis yang spesifik.
"""

import os

from app.models import ChatMessage, ChatResponse

MODEL_DEFAULT = "recursive/flint-v1.0:free"
BASE_URL_DEFAULT = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT = """Kamu adalah asisten customer support yang ramah dan ringkas.
Jawab dalam bahasa Indonesia.

Selalu balas HANYA dengan satu JSON object valid, tanpa markdown fence dan
tanpa teks tambahan, dengan schema:

{
  "balasan": "jawaban untuk pengguna (string)",
  "topik": "umum" | "teknis" | "lainnya",
  "sentimen": "positif" | "netral" | "negatif",
  "butuh_eskalasi": true | false
}

Aturan:
- Jangan menambah field di luar schema.
- "butuh_eskalasi" bernilai true hanya jika masalah perlu ditangani manusia,
  misalnya bug parah, permintaan refund, atau pengguna sangat marah.
- Jika informasi kurang, tanyakan lewat field "balasan". Jangan mengarang.
"""


def _client():
    """Buat client OpenAI-compatible dari environment."""
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError(
            "LLM_API_KEY belum diisi. Salin .env.example menjadi .env."
        )

    from openai import OpenAI

    return OpenAI(
        base_url=os.getenv("LLM_BASE_URL", BASE_URL_DEFAULT),
        api_key=api_key,
    )


def balas(history: list[ChatMessage], pesan_baru: str) -> ChatResponse:
    """Kirim system prompt + history + pesan baru, lalu validasi jawaban JSON.

    history berisi pesan sebelumnya (tanpa pesan_baru). Output model divalidasi
    dengan ChatResponse sehingga bentuknya dijamin sesuai schema.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + [{"role": m.role, "content": m.content} for m in history] + [
        {"role": "user", "content": pesan_baru}
    ]

    response = _client().chat.completions.create(
        model=os.getenv("LLM_MODEL", MODEL_DEFAULT),
        messages=messages,
        temperature=0.3,
    )

    content = response.choices[0].message.content
    return ChatResponse.model_validate_json(content)
