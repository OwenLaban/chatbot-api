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

    TODO:
    1. history = memory.ambil_pesan(payload.session_id)
    2. jawaban = balas(history, payload.message)
    3. memory.simpan_pesan(payload.session_id, "user", payload.message)
    4. memory.simpan_pesan(payload.session_id, "assistant", jawaban.balasan)
    5. return jawaban

    Catatan: simpan pesan setelah LLM berhasil, agar memory tidak berisi
    pesan user tanpa balasan saat terjadi error.
    """
    raise NotImplementedError("TODO: implementasikan POST /chat")


@app.get("/sessions/{session_id}", response_model=SessionResponse)
def ambil_session(session_id: str) -> SessionResponse:
    """Kembalikan riwayat percakapan.

    TODO:
    1. messages = memory.ambil_pesan(session_id)
    2. Jika kosong: raise HTTPException(status_code=404,
       detail="Session tidak ditemukan")
    3. return SessionResponse(session_id=session_id, messages=messages)
    """
    raise NotImplementedError("TODO: implementasikan GET /sessions/{session_id}")


@app.delete("/sessions/{session_id}")
def hapus_session(session_id: str) -> dict[str, str]:
    """Hapus satu sesi.

    TODO:
    1. Jika memory.hapus_session(session_id) mengembalikan False:
       raise HTTPException(status_code=404, detail="Session tidak ditemukan")
    2. return {"status": "deleted", "session_id": session_id}
    """
    raise NotImplementedError("TODO: implementasikan DELETE /sessions/{session_id}")
