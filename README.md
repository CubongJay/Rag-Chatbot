# RAG Chatbot

A session-isolated Retrieval-Augmented Generation (RAG) backend. Upload documents, ask questions, get answers grounded in your files — with full observability via Langfuse.

## Features

- **Document ingestion**: Upload `.txt` and `.pdf` files
- **Async processing**: Non-blocking uploads with background chunking + embedding
- **Vector search**: Dense retrieval via pgvector (PostgreSQL extension)
- **Session isolation**: Chunks scoped per session — no cross-talk between chats
- **RAG answers**: LLM responses grounded in retrieved document context
- **Observability**: Full traces of retrieval + LLM calls via Langfuse
- **Status polling**: `PENDING → PROCESSING → SUCCESS/FAILED` lifecycle

## Tech Stack

| Layer | Tech |
|-------|------|
| API | FastAPI (async) |
| Database | PostgreSQL 15 + pgvector |
| Embeddings | OpenAI `text-embedding-3-small` |
| LLM | OpenAI GPT-4o-mini via LangChain |
| Observability | Langfuse Cloud |
| Migrations | Alembic |
| Package manager | uv |
| Container | Docker + Docker Compose |

## Architecture

Clean Architecture — dependencies point inward:

```
┌─────────────────────────────────────────────┐
│              API Layer (FastAPI)            │
│  endpoints → handlers → use cases           │
├─────────────────────────────────────────────┤
│            Use Case Layer                   │
│  UploadDocumentUseCase                      │
│  ProcessDocumentUseCase (background)        │
│  GenerateAIResponseUseCase                  │
├─────────────────────────────────────────────┤
│            Domain Layer                     │
│  Entities: Document, DocumentChunk          │
│  Interfaces: DocumentRepository, LLMService │
├─────────────────────────────────────────────┤
│          Infrastructure Layer               │
│  SQLAlchemy repos, OpenAI service, pgvector │
└─────────────────────────────────────────────┘
```

### RAG Flow

```
Upload → save file → PENDING record
         ↓ (background task)
       extract text (pypdf / plain read)
         ↓
       chunk → embed → store in pgvector
         ↓
       SUCCESS with chunk_count

Chat → embed query
     ↓
   retrieve top-k chunks (pgvector similarity, session-scoped)
     ↓
   inject into prompt → LLM → response
     ↓ (traced via Langfuse)
```

## Setup

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- (Optional) Langfuse Cloud account for observability

### Quick Start

1. Clone and enter:
   ```bash
   git clone <repo-url>
   cd RAG-Chatbot
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   ```
   Fill in `OPENAI_API_KEY` and Langfuse keys.

3. Start services:
   ```bash
   docker compose up --build
   ```

4. Enable pgvector (first run only):
   ```bash
   docker compose exec db psql -U postgres -d chatbotDb -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```

5. Run migrations:
   ```bash
   docker compose exec web alembic upgrade head
   ```

6. Health check:
   ```bash
   curl http://localhost:8000/healthcheck
   ```

## API Usage

All endpoints require an `X-API-Key` header.

### Upload a document

```bash
curl -X POST "http://localhost:8000/rag-context/documents/upload?session_id=<uuid>" \
  -H "X-API-Key: your-key" \
  -F "file=@solar_system.pdf"
```

Response:
```json
{
  "document_id": "...",
  "file_path": "uploads/...",
  "status": "pending"
}
```

### Poll document status

```bash
curl -H "X-API-Key: your-key" \
  http://localhost:8000/rag-context/documents/status/<document_id>
```

Returns `status`, `chunk_count`, and `error_message`.

### Chat with RAG

```bash
curl -X POST http://localhost:8000/sessions/<session_id>/messages/ \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"content": "What is Jupiter'\''s Great Red Spot?", "sender": "user", "message_type": "user"}'
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **pgvector over Chroma** | Unified data layer in Postgres — one backup, ACID transactions, JOIN-based filtering by session/status |
| **BackgroundTasks over Celery** | Zero infra overhead for a portfolio project. Trade-off: no retries, no durability. Documented path to migrate. |
| **Session-scoped chunks** | Denormalized `session_id` on `document_chunks` — avoids JOIN on hot retrieval path |
| **Async throughout** | `aembed_documents`, async SQLAlchemy sessions, non-blocking LLM calls |
| **Langfuse Cloud** | Full observability without local infra — traces retrieval + LLM in one place |

## Testing

```bash
docker compose exec web pytest src/tests/
```

## API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Langfuse traces: https://cloud.langfuse.com

