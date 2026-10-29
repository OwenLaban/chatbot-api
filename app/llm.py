"""Klien LLM OpenAI-compatible.

Default provider: OpenRouter (https://openrouter.ai) dengan model gratis.
Konfigurasi lewat environment:

    LLM_BASE_URL=https://openrouter.ai/api/v1
    LLM_API_KEY=...
    LLM_MODEL=openrouter/free
"""

import os

from app.models import ChatMessage, ChatResponse

MODEL_DEFAULT = "openrouter/free"
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
    """Buat client OpenAI-compatible dari environment.

    TODO:
    1. api_key = os.getenv("LLM_API_KEY")
    2. Jika kosong, raise RuntimeError(
           "LLM_API_KEY belum diisi. Salin .env.example menjadi .env."
       )
    3. from openai import OpenAI
    4. Kembalikan OpenAI(
           base_url=os.getenv("LLM_BASE_URL", BASE_URL_DEFAULT),
           api_key=api_key,
       )
    """
    raise NotImplementedError("TODO: implementasikan _client()")


def balas(history: list[ChatMessage], pesan_baru: str) -> ChatResponse:
    """Minta jawaban terstruktur dari LLM.

    history berisi pesan sebelumnya (tanpa pesan_baru). Fungsi ini harus
    mengirim system prompt + history + pesan_baru, lalu memvalidasi output.

    TODO:
    1. Susun messages:
           [{"role": "system", "content": SYSTEM_PROMPT}]
           + [{"role": m.role, "content": m.content} for m in history]
           + [{"role": "user", "content": pesan_baru}]
    2. Panggil:
           response = _client().chat.completions.create(
               model=os.getenv("LLM_MODEL", MODEL_DEFAULT),
               messages=messages,
               temperature=0.3,
           )
    3. content = response.choices[0].message.content
    4. Kembalikan ChatResponse.model_validate_json(content).
       Jika content bukan JSON valid, biarkan error yang jelas muncul.
    """
    raise NotImplementedError("TODO: implementasikan balas()")
