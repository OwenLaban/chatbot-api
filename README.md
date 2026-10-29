# Chatbot API

Chatbot dengan **memory percakapan** dan **structured output JSON**, dibangun
dengan FastAPI + Pydantic + LLM OpenAI-compatible (default: OpenRouter free).

> Status: 🚧 dalam pengerjaan — proyek portfolio #3, Minggu 9 dari roadmap
> AI Engineer 24 minggu.

## Masalah

Chatbot biasa memiliki dua kelemahan untuk dipakai di aplikasi nyata:

1. **Lupa konteks** — setiap request berdiri sendiri, padahal pengguna sering
   merujuk pesan sebelumnya (“produk itu”, “nama saya tadi siapa?”).
2. **Output teks bebas** — jawaban sulit diproses program lain. Aplikasi harus
   mem-parsing teks, dan hasilnya tidak konsisten.

Proyek ini menyelesaikan keduanya:

- riwayat percakapan disimpan per `session_id`;
- setiap jawaban divalidasi Pydantic sehingga selalu berbentuk JSON dengan
  field dan nilai yang sudah ditentukan.

## Fitur

- `POST /chat` — kirim pesan, dapat jawaban terstruktur, simpan percakapan.
- `GET /sessions/{session_id}` — lihat riwayat satu sesi.
- `DELETE /sessions/{session_id}` — hapus sesi.
- `GET /health` — cek status service.
- Memory per sesi disimpan di file JSON (`data/conversations.json`).
- Provider LLM dapat diganti lewat environment variable.
- Test memakai LLM palsu (mock), jadi **tidak butuh API key** saat `pytest`.

## Arsitektur

```text
┌────────┐   HTTP    ┌──────────────┐
│ Client │ ────────> │   FastAPI    │
└────────┘           │   main.py    │
                     └───┬──────┬───┘
                         │      │
                  memory │      │ llm
                         v      v
              conversations   OpenRouter / provider
                  .json        OpenAI-compatible
```

| Lapisan | File | Tanggung jawab |
|---|---|---|
| API | `app/main.py` | Routing HTTP + validasi request/response |
| Schema | `app/models.py` | Kontrak data dengan Pydantic |
| Memory | `app/memory.py` | Baca/tulis riwayat per sesi |
| LLM | `app/llm.py` | System prompt + panggilan model + parsing JSON |

## Struktur proyek

```text
chatbot-api/
├── app/
│   ├── __init__.py
│   ├── main.py       # endpoint FastAPI
│   ├── memory.py     # penyimpanan JSON
│   ├── llm.py        # klien LLM + prompt
│   └── models.py     # schema Pydantic
├── data/
│   └── .gitkeep
├── tests/
│   ├── conftest.py
│   └── test_chat.py
├── .env.example
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Menjalankan

Butuh Python 3.11+.

```powershell
cd chatbot-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Buka `.env`, lalu isi `LLM_API_KEY` dengan key OpenRouter:

- Buat key gratis di <https://openrouter.ai/keys>.
- **Jangan commit `.env`.** File ini sudah masuk `.gitignore`.
- Jangan pernah menempelkan API key ke chat, prompt, atau repository.

Jalankan server (port 8002 agar tidak bentrok dengan service lain di mesin ini):

```powershell
uvicorn app.main:app --reload --port 8002
```

Buka dokumentasi interaktif di <http://127.0.0.1:8002/docs>.

## Konfigurasi

| Variabel | Wajib | Default | Keterangan |
|---|---|---|---|
| `LLM_API_KEY` | ya | — | API key provider |
| `LLM_BASE_URL` | tidak | `https://openrouter.ai/api/v1` | Endpoint OpenAI-compatible |
| `LLM_MODEL` | tidak | `openrouter/free` | Nama model |
| `CHATBOT_DATA_FILE` | tidak | `data/conversations.json` | Lokasi file memory |

## Endpoint

| Method | Path | Keterangan |
|---|---|---|
| `GET` | `/health` | Status service |
| `POST` | `/chat` | Kirim pesan + simpan memory |
| `GET` | `/sessions/{session_id}` | Riwayat satu sesi |
| `DELETE` | `/sessions/{session_id}` | Hapus satu sesi |

### `POST /chat`

Request:

```json
{
  "session_id": "demo-1",
  "message": "Halo, saya Rina. Saya tidak bisa login."
}
```

Response `200`:

```json
{
  "balasan": "Halo Rina, maaf atas kendalanya. Apakah muncul pesan error tertentu?",
  "topik": "teknis",
  "sentimen": "negatif",
  "butuh_eskalasi": false
}
```

Schema jawaban:

| Field | Tipe | Nilai |
|---|---|---|
| `balasan` | string | Jawaban untuk pengguna |
| `topik` | enum | `umum`, `teknis`, `lainnya` |
| `sentimen` | enum | `positif`, `netral`, `negatif` |
| `butuh_eskalasi` | boolean | `true` jika perlu manusia |

### `GET /sessions/{session_id}`

```json
{
  "session_id": "demo-1",
  "messages": [
    {"role": "user", "content": "Halo, saya Rina."},
    {"role": "assistant", "content": "Halo Rina, ada yang bisa dibantu?"}
  ]
}
```

Mengembalikan `404` jika sesi belum ada.

### `DELETE /sessions/{session_id}`

```json
{
  "status": "deleted",
  "session_id": "demo-1"
}
```

Mengembalikan `404` jika sesi tidak ditemukan.

## Testing

```powershell
pytest -q
```

Test tidak memanggil LLM sungguhan: `app.main.balas` diganti fungsi palsu.
File memory diarahkan ke `tmp_path`, sehingga test tidak saling mengotori data.

Yang diuji:

- health check;
- bentuk response terstruktur;
- pesan tersimpan dan muncul di `GET /sessions/{id}`;
- history sebelumnya ikut dikirim ke LLM;
- isolasi antar-sesi;
- hapus sesi + `404`;
- validasi input;
- isi file JSON.

## Evaluasi manual

Diisi setelah implementasi selesai dan diuji dengan model sungguhan.

| Skenario | Hasil | Catatan |
|---|---|---|
| Sapaan biasa | TODO | |
| Ingat nama dari pesan sebelumnya | TODO | |
| Jawaban selalu JSON valid | TODO | |
| Sesi berbeda tidak tercampur | TODO | |
| Hapus sesi | TODO | |

## Keterbatasan

- File JSON belum aman untuk banyak worker/request bersamaan. Untuk produksi,
  gunakan database (SQLite/Postgres) atau lock.
- Belum ada autentikasi; siapa pun yang tahu `session_id` bisa membaca sesi.
- Riwayat tumbuh tanpa batas dan belum dipangkas berdasarkan token.
- Model gratis bisa lambat, kena rate limit, atau berubah tanpa pemberitahuan.
- Output JSON bergantung pada kepatuhan model. Validasi Pydantic menangkap
  bentuk yang salah, tetapi tidak menjamin isi jawaban benar.

## Yang dipelajari

- Memisahkan **API layer**, **storage**, dan **LLM client**.
- Menyimpan memory percakapan per sesi.
- Memaksa output terstruktur dengan system prompt + Pydantic.
- Menguji endpoint LLM tanpa API key dengan mock.
- Menjaga secret tetap di `.env`.
