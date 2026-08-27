# Terra - Enterprise AI Knowledge & RAG Platform

[![CI Pipeline](https://github.com/Hishhiki/Terra/actions/workflows/ci.yml/badge.svg)](https://github.com/Hishhiki/Terra/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![gRPC](https://img.shields.io/badge/gRPC-HTTP%2F2-244c5a?logo=grpc&logoColor=white)](https://grpc.io/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-FC521F)](https://www.trychroma.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Terra** is a high-performance, microservice-based enterprise search and question-answering platform powered by **Local RAG (Retrieval-Augmented Generation)** over **gRPC (HTTP/2)** with real-time streaming and complete data privacy.

---

## System Architecture

Terra employs a decoupled microservices architecture with low-latency binary communication over **gRPC / Protocol Buffers**:

```text
[ User / Modern Web Browser ]
              │
              ▼  (HTTP / Server-Sent Events)
┌─────────────────────────────────────────────────────────┐
│              1. API Gateway (FastAPI)                   │
│  - Static Web UI hosting & Dropzone file uploads        │
│  - Document parser (.pdf, .docx, .txt)                  │
│  - Real-time token streaming proxy via SSE              │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼  [ gRPC / Protobuf over HTTP/2 ]
┌─────────────────────────────────────────────────────────┐
│              2. ML Engine (gRPC Server)                 │
│  - Word-aware semantic chunking with overlap            │
│  - ChromaDB persistent vector database (Embeddings)     │
│  - Local Qwen 2.5 (1.5B) LLM inference via Ollama       │
│  - Server-Streaming generation with source attribution  │
└─────────────────────────────────────────────────────────┘
```

---

## Key Features

* **Ultra-Fast Binary Protocol:** Inter-service RPC communication via HTTP/2 and Google Protocol Buffers (`protos/terra.proto`).
* **100% Private Local RAG:** Zero external API calls. All document ingestion, vector embeddings, and language model inference run strictly on-premise.
* **Smart Word-Aware Chunking:** Intelligent text segmentation respecting natural word boundaries with dynamic overlap, eliminating clipped sentences.
* **Modern Web Interface:** Responsive dark-mode single-page application featuring drag-and-drop file ingestion, live typewriter token streaming, and interactive source citations.
* **One-Command Orchestration:** Ready for multi-container deployment via Docker Compose.
* **Anti-Hallucination Guardrails:** Strict grounded prompt engineering ensuring answers are synthesized exclusively from verified corporate records.

---

## Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **API Gateway** | `FastAPI`, `Uvicorn`, `Pydantic` | Web interface, file ingestion & SSE proxy |
| **Inter-Service** | `gRPC`, `Protocol Buffers (proto3)` | High-throughput binary RPC communication |
| **Vector Store** | `ChromaDB`, `all-MiniLM-L6-v2` | Persistent semantic vector indexing & retrieval |
| **LLM Inference**| `Ollama`, `Qwen 2.5 (1.5B)` | Local generative language modeling |
| **Parsers** | `pypdf`, `python-docx` | Multi-format document text extraction |
| **DevOps & CI** | `Docker`, `Docker Compose`, `GitHub Actions` | Automated containerization and CI pipeline |

---

## Quickstart Guide

### Option 1: Docker Compose (Recommended)

Ensure Docker Desktop is running, then execute:

```bash
docker compose up --build
```

Access the interactive web application at `http://localhost:8000`

---

### Option 2: Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hishhiki/Terra.git
   cd Terra
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Compile Protocol Buffers:**
   ```bash
   # Windows:
   .\compile_proto.bat
   ```

5. **Start the ML gRPC Engine (Terminal 1):**
   ```bash
   python -m services.ml_engine.main
   ```

6. **Start the API Gateway (Terminal 2):**
   ```bash
   python -m services.api_gateway.main
   ```

7. Open `http://localhost:8000` in your browser.

---

## API Endpoints

### REST & Web
- `GET /` — Serves the interactive Web Application.
- `GET /api/health` — Health check status endpoint.
- `POST /api/upload` — Ingests `.pdf`, `.docx`, or `.txt` files and indexes them in ChromaDB.
- `POST /api/chat/stream` — Streams model tokens and citations via Server-Sent Events (`text/event-stream`).

### gRPC Contract (`protos/terra.proto`)
- `rpc StreamChat (ChatRequest) returns (stream ChatChunkResponse)`
- `rpc IndexDocument (DocumentUploadRequest) returns (DocumentUploadResponse)`

---

## Author
- **GitHub:** [@Hishhiki](https://github.com/Hishhiki)

## License
This project is open-source and licensed under the [MIT License](LICENSE).
