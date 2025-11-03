# RAG Chatbot

A backend microservice for storing chat conversations with AI integration.

## What it does

This service stores chat sessions and messages, with automatic AI responses using OpenAI. Built with FastAPI and PostgreSQL.

## Setup

### Prerequisites
- Docker and Docker Compose
- OpenAI API key

### Quick start

1. Clone the repo
```bash
git clone <repo-url>
cd RAG-Chatbot
```

2. Set up environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Generate your API keys
```bash
# Generate a secure API key
openssl rand -hex 32
# Copy the output to your .env file as API_KEY

# Get your OpenAI API key from https://platform.openai.com/api-keys
# Add it to your .env file as OPENAI_API_KEY
```

4. Start the services
```bash
docker-compose up --build
```

5. Check it's working
```bash
curl http://localhost:8000/healthcheck
```

## Configuration


See `.env.example` for all variables.

## API Usage

All endpoints need an API key in the `X-API-Key` header.

### Sessions

Create a session:
```bash
curl -X POST http://localhost:8000/sessions/ \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Chat", "is_favorite": false}'
```

Get all sessions:
```bash
curl -H "X-API-Key: your-key" http://localhost:8000/sessions/
```

### Messages

Send a message (gets AI response):
```bash
curl -X POST http://localhost:8000/sessions/{session_id}/messages/ \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello!", "sender": "user", "message_type": "user"}'
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

## Testing
pytest src/tests/

## Docker

The app runs in Docker with PostgreSQL. Check `docker-compose.yaml` for configuration.

## Architecture

Uses Clean Architecture with:
- Domain layer (entities, interfaces)
- Use cases (business logic)
- Infrastructure (database, external services)
- API layer (FastAPI endpoints)
