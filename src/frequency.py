"""
MRT Blue Line — train frequency (headway) logic.
Source: BEM official frequency table (2026-09-14).

Returns the current gap in minutes between trains based on day type and time.
"""
from __future__ import annotations

from datetime import datetime

import pytz

TZ = pytz.timezone("Asia/Bangkok")


def _hm(h: int, m: int = 0) -> int:
    """Convert hour/minute to absolute minutes from midnight."""
    return h * 60 + m


# ── Frequency windows ──────────────────────────────────────────────────────────
# Each entry: (start_abs, end_abs, gap_minutes)
# Matched first-fit; last entry is the catch-all.

_WEEKDAY_WINDOWS = [
    (_hm(5, 30), _hm(7,  0), 5),
    (_hm(7,  0), _hm(9,  0), 7),   # peak directional split simplified to 7
    (_hm(9,  0), _hm(16, 30), 7),
    (_hm(16, 30), _hm(17,  0), 5),
    (_hm(17,  0), _hm(20,  0), 4),
    (_hm(20,  0), _hm(21,  0), 5),
    (_hm(21,  0), _hm(24, 30), 7),  # covers until ~00:30
]

_SATURDAY_WINDOWS = [
    (_hm(6,  0), _hm(16,  0), 7),
    (_hm(16, 0), _hm(21,  0), 6),
    (_hm(21, 0), _hm(24, 30), 7),
]

_SUNDAY_WINDOWS = [
    (_hm(6,  0), _hm(17,  0), 7),
    (_hm(17, 0), _hm(21,  0), 7),
    (_hm(21, 0), _hm(24, 30), 7),
]


def current_gap(now: datetime) -> int:
    """
    Return train headway in minutes for the given datetime.

    Uses Asia/Bangkok timezone. Falls back to 7 minutes if outside all windows.
    """
    now_bkk = now.astimezone(TZ)
    weekday = now_bkk.weekday()  # 0=Mon, 6=Sun

    h, m = now_bkk.hour, now_bkk.minute
    now_abs = h * 60 + m
    if now_abs < 5 * 60:
        now_abs += 24 * 60  # past-midnight zone

    if weekday < 5:
        windows = _WEEKDAY_WINDOWS
    elif weekday == 5:
        windows = _SATURDAY_WINDOWS
    else:
        windows = _SUNDAY_WINDOWS

    for start, end, gap in windows:
        if start <= now_abs < end:
            return gap

    return 7  # default outside service hours


def gap_label(gap: int) -> str:
    """Human-readable label for the current frequency period."""
    if gap <= 4:
        return "Peak"
    if gap <= 5:
        return "ช่วงเช้า/เย็น"
    return "Off-peak"
