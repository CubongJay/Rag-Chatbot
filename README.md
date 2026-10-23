
```markdown
# RAG Chatbot

A session-isolated Retrieval-Augmented Generation (RAG) backend. Upload documents, ask questions, get answers grounded in your files — with full observability via Langfuse.

[![Backend CI](https://github.com/CubongJay/Rag-Chatbot/actions/workflows/backend.yml/badge.svg)](https://github.com/CubongJay/Rag-Chatbot/actions/workflows/backend.yml)

## Cloud Deployment & CI/CD

This application is fully containerized and designed for production deployment on **Microsoft Azure**.

> **Note:** The live cloud environment has been deprovisioned to prevent unnecessary billing. However, the complete infrastructure and deployment pipeline are fully automated via GitHub Actions.

### Deployment Architecture
- **Compute:** Azure Container Apps (Serverless, auto-scaling)
- **Database:** Azure Database for PostgreSQL Flexible Server (with pgvector)
- **Image Registry:** Azure Container Registry (ACR)
- **Secrets Management:** Azure Key Vault (injected at runtime via Managed Identity)
- **LLM Provider:** Azure AI Foundry (via LangChain)
- **Frontend:** React / TypeScript (Deployed separately)

### CI/CD Pipeline (GitHub Actions)
Every push to the `master` branch triggers an automated pipeline that:
1. Runs `isort` and `black` for code quality.
2. Runs the `pytest` suite.
3. Authenticates to Azure securely using **OIDC (OpenID Connect)** — no long-lived passwords are stored in GitHub.
4. Builds the Docker image and pushes it to ACR.
5. Deploys the new revision to Azure Container Apps.

To redeploy the infrastructure from scratch, simply recreate the Azure resources, attach the OIDC federated credential, and push to `master`.

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
| Database | PostgreSQL 16 + pgvector |
| Embeddings | OpenAI `text-embedding-3-small` |
| LLM | Azure AI Foundry (via LangChain) |
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
│  SQLAlchemy repos, Azure LLM service        │
│  pgvector                                   │
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
- Azure AI Foundry endpoint and credential (or OpenAI API key)
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
   Fill in `AZURE_INFERENCE_ENDPOINT`, `AZURE_INFERENCE_CREDENTIAL`, and Langfuse keys.

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
| **Azure AI Foundry** | Abstracted LLM provider via `LLMService` interface — migrated from OpenAI to Azure without changing a single use case or domain entity. |
| **OIDC over Client Secrets** | GitHub Actions authenticates to Azure using short-lived federated credentials. No long-lived passwords are stored in GitHub. |

## Testing

```bash
uv run pytest
```

## API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Langfuse traces: https://cloud.langfuse.com
```