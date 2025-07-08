# MiniVault API

A lightweight local REST API that simulates a core feature of ModelVault: receiving a prompt and returning a generated response.

## Features
- **POST /generate**: Accepts a prompt and returns a response (stubbed or from a local Hugging Face LLM)
- **Logging**: All prompt/response pairs are logged to `logs/log.jsonl`.
- **Modular FastAPI codebase**: Clean, extensible structure.
- **Docker & Compose**: Easy local setup, with optional Ollama integration.
- **Postman Collection**: For easy API testing.
- **Local LLM (distilGPT2)**: Use a local Hugging Face model for real text generation and streaming (no cloud APIs).

## Quickstart

### 1. Clone & Enter Directory
```bash
cd MiniVault-API
```

### 2. Run with Docker (Recommended)
```bash
# Build and start API + Ollama (for local LLM, optional)
./setup.sh
```
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Ollama: http://localhost:11434 (if enabled)

### 3. Run Locally (No Docker)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Test the API
```bash
curl -X POST http://localhost:8000/generate \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "Hello, world!"}'
```

Or import the included Postman collection from `postman-collection/`.

## API Usage

### Endpoint: `POST /generate`

#### Request Body (Stubbed, any other prompt)
```json
{
  "prompt": "Write a short poem about the ocean"
}
```
**Response:**
```json
{
  "response": "Stubbed response for: 'Write a short poem about the ocean'"
}
```

#### Request Body (Use Local LLM)
```json
{
  "prompt": "Write a short poem about the ocean",
  "use_llm": true
}
```
**Response:**
```json
{
  "response": "<generated text from distilGPT2>"
}
```

#### Request Body (Streaming, Stubbed)
```json
{
  "prompt": "Write a short poem about the ocean",
  "stream": true
}
```
**Response:**
- Plain text, streamed word-by-word.

#### Request Body (Streaming, Local LLM)
```json
{
  "prompt": "Write a short poem about the ocean",
  "use_llm": true,
  "stream": true
}
```
**Response:**
- Plain text, streamed token-by-token from the local Hugging Face model.

---

## ⚠️ First-time LLM Use
- The first time you use `"use_llm": true`, the model will be downloaded from Hugging Face (requires internet).
- After that, it will run fully offline from the `./models/` directory.

## Project Structure
```

MiniVault-API/
├── app/
│   ├── main.py         # FastAPI entry point
│   ├── routes.py       # API endpoints
│   ├── model.py        # Stubbed/LLM response generator
│   ├── logger.py       # JSONL logger
│   └── hf_model.py     # Hugging Face LLM loader/generator
├── logs/
│   └── log.jsonl       # Prompt/response logs
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── setup.sh
├── README.md
└── postman-collection/
    └── MiniVault-API.postman_collection.json
```

## Design Notes & Tradeoffs
- **Stubbed by default**: The response is hardcoded for simplicity. Use `"use_llm": true` for real LLM output.
- **Streaming**: Both stubbed and LLM responses support streaming (plain text, not JSON).
- **No cloud APIs**: Fully offline after first model download.
- **Modular**: Easy to extend for more endpoints or features.

## Future Improvements
- Add more local model options or configuration.
- Add streaming in JSONL or SSE format.
- Add CLI or more test scripts.

---

**Made with ❤️ for ModelVault Take-Home.** 