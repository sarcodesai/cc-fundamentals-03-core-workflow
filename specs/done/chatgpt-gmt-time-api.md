# ChatGPT GMT Time API

## Problem Statement

Build an HTTP server that ChatGPT can call via its Actions (custom GPT) feature to retrieve the current time in Greenwich Mean Time (GMT/UTC).

## Objectives

- Expose a simple HTTP endpoint that returns the current GMT time
- Provide an OpenAPI specification so ChatGPT can discover and call the endpoint
- Keep the implementation minimal and easy to deploy

## Technical Approach

**Stack: Python + FastAPI**

Why FastAPI:
- Auto-generates the OpenAPI spec that ChatGPT Actions require — zero extra work
- Minimal boilerplate for a single-endpoint API
- Python's `datetime` module handles UTC/GMT cleanly
- Easy local dev with `uvicorn`, easy to deploy anywhere

### Architecture

```
project root
├── main.py              # FastAPI app with /gmt-time endpoint
├── requirements.txt     # Dependencies (fastapi, uvicorn)
└── (existing files)
```

ChatGPT Actions flow:
```
ChatGPT  -->  HTTP GET /gmt-time  -->  FastAPI server  -->  JSON response
         <--  { "utc_now": "2026-02-22T14:30:00Z", "formatted": "14:30:00 GMT" }
```

## Implementation Plan

### Phase 1: Core Server

**File: `requirements.txt`**
```
fastapi>=0.115.0
uvicorn>=0.34.0
```

**File: `main.py`**
```python
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GMT Time API",
    description="Returns the current time in Greenwich Mean Time. Designed for use as a ChatGPT Action.",
    version="1.0.0",
    servers=[{"url": "http://localhost:8000", "description": "Local dev server"}],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get(
    "/gmt-time",
    summary="Get current GMT time",
    description="Returns the current date and time in Greenwich Mean Time (UTC).",
)
def get_gmt_time():
    now = datetime.now(timezone.utc)
    return {
        "utc_now": now.isoformat(),
        "formatted_time": now.strftime("%H:%M:%S GMT"),
        "formatted_date": now.strftime("%Y-%m-%d"),
        "day_of_week": now.strftime("%A"),
    }
```

Key details:
- `datetime.now(timezone.utc)` gives the canonical UTC time (equivalent to GMT)
- CORS allows requests from ChatGPT's domains
- The OpenAPI spec is auto-served at `/openapi.json` and docs at `/docs`
- Response includes both ISO 8601 and human-readable formats so ChatGPT can present it naturally

### Phase 2: ChatGPT Action Setup

Once the server is running and publicly reachable, configure it in ChatGPT:

1. Go to **ChatGPT → Explore GPTs → Create a GPT → Configure → Actions**
2. Click **"Import from URL"** and enter: `https://<your-domain>/openapi.json`
3. ChatGPT will auto-discover the `/gmt-time` endpoint from the spec
4. Set authentication to **None** (this is a public time endpoint)
5. Save the GPT

For local development, use a tunnel to expose localhost:
```bash
# Option A: ngrok
ngrok http 8000

# Option B: cloudflared
cloudflared tunnel --url http://localhost:8000
```

Then use the tunnel URL as the server URL in the OpenAPI spec and ChatGPT Action config.

## Testing Strategy

1. **Manual**: Run the server, hit `http://localhost:8000/gmt-time` in a browser or with `curl`
2. **OpenAPI validation**: Visit `http://localhost:8000/docs` to confirm the interactive Swagger UI works
3. **ChatGPT integration**: After tunnel/deploy, test by asking the custom GPT "What time is it in GMT?"

```bash
# Quick smoke test
curl http://localhost:8000/gmt-time
# Expected: {"utc_now":"2026-02-22T...Z","formatted_time":"14:30:00 GMT",...}
```

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Server starts at `http://localhost:8000`. OpenAPI spec at `http://localhost:8000/openapi.json`.

## Success Criteria

- [ ] `GET /gmt-time` returns correct UTC time in JSON
- [ ] `/openapi.json` serves a valid OpenAPI spec
- [ ] CORS headers allow ChatGPT domains
- [ ] ChatGPT can successfully call the endpoint and report the time
