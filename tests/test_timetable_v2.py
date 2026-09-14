"""Tests for timetable_v2.py — all 38 BL stations."""
from datetime import datetime

import pytest
import pytz

from src.timetable_v2 import STATIONS, next_trains_v2, station_label

TZ = pytz.timezone("Asia/Bangkok")

MONDAY   = (2026, 9, 14)   # a weekday
SATURDAY = (2026, 9, 13)   # a weekend day


def bkk(day_tuple, hh, mm):
    return TZ.localize(datetime(*day_tuple, hh, mm))


def test_all_38_stations_present():
    assert len(STATIONS) == 38


# ── first trains ──────────────────────────────────────────────────────────────

def test_bl22_weekday_lak_song_first_train():
    result = next_trains_v2(bkk(MONDAY, 5, 0), "BL22", "lak_song", count=1)
    assert result[0].hour == 5 and result[0].minute == 58


def test_bl10_weekend_tha_phra_first_train():
    result = next_trains_v2(bkk(SATURDAY, 5, 0), "BL10", "tha_phra", count=1)
    assert result[0].hour == 5 and result[0].minute == 59


# ── no service ────────────────────────────────────────────────────────────────

def test_bl38_lak_song_no_service():
    assert next_trains_v2(bkk(MONDAY, 8, 0), "BL38", "lak_song") == []


# ── validation ────────────────────────────────────────────────────────────────

def test_invalid_station_raises():
    with pytest.raises(ValueError):
        next_trains_v2(bkk(MONDAY, 8, 0), "BL99", "lak_song")


def test_invalid_direction_raises():
    with pytest.raises(ValueError):
        next_trains_v2(bkk(MONDAY, 8, 0), "BL22", "nowhere")


# ── aliases ───────────────────────────────────────────────────────────────────

def test_alias_numeric_22():
    a = next_trains_v2(bkk(MONDAY, 8, 0), "22", "lak_song")
    b = next_trains_v2(bkk(MONDAY, 8, 0), "BL22", "lak_song")
    assert a == b and len(a) > 0


def test_alias_lowercase_bl22():
    a = next_trains_v2(bkk(MONDAY, 8, 0), "bl22", "lak_song")
    b = next_trains_v2(bkk(MONDAY, 8, 0), "BL22", "lak_song")
    assert a == b and len(a) > 0


# ── station_label ─────────────────────────────────────────────────────────────

def test_station_label():
    assert station_label("BL22") == "สุขุมวิท (BL22)"
    assert station_label("bl22") == "สุขุมวิท (BL22)"
