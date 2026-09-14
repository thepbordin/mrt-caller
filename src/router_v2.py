"""
v2 router — any of the 38 MRT Blue Line stations, two directions.

GET /v2/next-train?mrt_depart_station=BL22&mrt_destination=lak_song
Plain-text response suitable for iOS Shortcuts notification.
"""
from __future__ import annotations

from datetime import datetime

import pytz
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse

from src.frequency import current_gap, gap_label
from src.timetable_v2 import (
    ALL_DIRECTIONS,
    DIRECTION_LABELS,
    STATIONS,
    last_train_str_v2,
    next_trains_v2,
    station_label,
)

TZ = pytz.timezone("Asia/Bangkok")

router = APIRouter()


@router.get("/next-train", response_class=PlainTextResponse)
def next_train_v2(
    mrt_depart_station: str = Query(
        ...,
        description="Station code BL01–BL38 (also '1'–'38', case-insensitive)",
        examples=["BL22"],
    ),
    mrt_destination: str | None = Query(
        default=None,
        description="'lak_song' or 'tha_phra' — omit to show both directions",
    ),
    count: int = Query(default=3, ge=1, le=5, description="Number of upcoming trains"),
    gap: int | None = Query(
        default=None,
        ge=1,
        le=30,
        description="Train headway in minutes — omit to auto-detect from time of day",
    ),
):
    """
    Returns next N train times at any Blue Line station.
    If mrt_destination is omitted, returns both directions.
    Plain-text response so Apple Shortcuts can display it directly.
    """
    try:
        label = station_label(mrt_depart_station)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if mrt_destination is not None and mrt_destination not in ALL_DIRECTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown direction '{mrt_destination}'. Use: {ALL_DIRECTIONS}",
        )

    now = datetime.now(TZ)
    is_weekday = now.weekday() < 5
    day_label = "วันธรรมดา" if is_weekday else "เสาร์-อาทิตย์/หยุด"
    gap_min = gap if gap is not None else current_gap(now)
    period = gap_label(gap_min)

    def render(direction: str) -> str:
        dest = DIRECTION_LABELS[direction]
        header = f"🚇 {label} → {dest}"
        try:
            trains = next_trains_v2(now, mrt_depart_station, direction,
                                    gap_min=gap_min, count=count)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        if not trains:
            if STATIONS[mrt_depart_station.strip().upper()]["directions"][direction] is None:
                return f"{header}\n⛔ ไม่มีบริการในทิศทางนี้"
            last = last_train_str_v2(mrt_depart_station, direction, is_weekday)
            return f"{header}\n⛔ หมดบริการแล้ว (สุดท้าย {last})"
        times_str = "  ".join(t.strftime("%H:%M") for t in trains)
        minutes_left = int((trains[0] - now).total_seconds() // 60)
        soon = f"อีก {minutes_left} นาที" if minutes_left > 0 else "กำลังมา!"
        return f"{header}\n⏱ {times_str}\n🕐 {soon}  {day_label} {period}  ทุก {gap_min} นาที"

    if mrt_destination:
        return render(mrt_destination)

    return "\n\n".join(render(d) for d in ALL_DIRECTIONS)
