from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64, examples=["demo-1"])
    message: str = Field(
        min_length=1,
        max_length=2000,
        examples=["Halo, saya butuh bantuan soal login."],
    )


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatResponse(BaseModel):
    balasan: str = Field(min_length=1, max_length=4000)
    topik: Literal["umum", "teknis", "lainnya"]
    sentimen: Literal["positif", "netral", "negatif"]
    butuh_eskalasi: bool


class SessionResponse(BaseModel):
    session_id: str
    messages: list[ChatMessage]
