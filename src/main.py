"""
mrt-caller — MRT Blue Line arrival notifier

Endpoints:
  GET /health                                                         → health check (no auth required)
  GET /v2/next-train?mrt_depart_station=BL22[&mrt_destination=lak_song]  → any station

Auth: all endpoints except /health require header:
  X-API-Key: <MRT_API_KEY from env>
"""
from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from src.router_v2 import router as router_v2

app = FastAPI(title="mrt-caller", version="0.5.0")

_API_KEY = os.environ.get("MRT_API_KEY", "")


@app.middleware("http")
async def require_api_key(request: Request, call_next):
    # /health is public
    if request.url.path == "/health":
        return await call_next(request)
    # all other routes need the key
    key = request.headers.get("X-API-Key", "")
    if not _API_KEY or key != _API_KEY:
        return PlainTextResponse("Unauthorized", status_code=401)
    return await call_next(request)


@app.get("/health")
def health():
    return JSONResponse({"ok": True})


# v2 routes: any of the 38 Blue Line stations
app.include_router(router_v2, prefix="/v2")
