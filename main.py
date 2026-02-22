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
