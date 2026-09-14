"""
mrt-caller — MRT Blue Line arrival notifier

Endpoints:
  GET /health                              → health check (also at /v1/health)
  GET /next-train                          → v1: Tha Phra all 3 platforms (also at /v1/next-train)
  GET /v2/next-train?mrt_depart_station=BL22[&mrt_destination=lak_song]  → v2: any station
Returns plain text suitable for iOS Shortcuts notification.
"""
from __future__ import annotations

from fastapi import FastAPI

from src.router_v1 import router as router_v1
from src.router_v2 import router as router_v2

app = FastAPI(title="mrt-caller", version="0.4.0")

# v1 routes: kept at / for backward compat, also mounted at /v1
app.include_router(router_v1)
app.include_router(router_v1, prefix="/v1")

# v2 routes: any of the 38 Blue Line stations
app.include_router(router_v2, prefix="/v2")
