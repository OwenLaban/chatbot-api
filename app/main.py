"""Chatbot API — FastAPI + memory percakapan + structured output."""

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException  # noqa: E402

from app import memory
from app.llm import balas
from app.models import ChatRequest, ChatResponse, SessionResponse

app = FastAPI(
    title="Chatbot API",
    description="Chatbot dengan memory percakapan dan jawaban JSON terstruktur.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Balas satu pesan, lalu simpan percakapan.

    Pesan disimpan setelah LLM berhasil, agar memory tidak berisi pesan user
    tanpa balasan saat terjadi error.
    """
    history = memory.ambil_pesan(payload.session_id)
    jawaban = balas(history, payload.message)
    memory.simpan_pesan(payload.session_id, "user", payload.message)
    memory.simpan_pesan(payload.session_id, "assistant", jawaban.balasan)
    return jawaban


@app.get("/sessions/{session_id}", response_model=SessionResponse)
def ambil_session(session_id: str) -> SessionResponse:
    """Kembalikan riwayat percakapan, atau 404 jika sesi belum ada."""
    messages = memory.ambil_pesan(session_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Session tidak ditemukan")
    return SessionResponse(session_id=session_id, messages=messages)


@app.delete("/sessions/{session_id}")
def hapus_session(session_id: str) -> dict[str, str]:
    """Hapus satu sesi, atau 404 jika sesi tidak ditemukan."""
    if not memory.hapus_session(session_id):
        raise HTTPException(status_code=404, detail="Session tidak ditemukan")
    return {"status": "deleted", "session_id": session_id}
