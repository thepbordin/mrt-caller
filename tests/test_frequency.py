"""Tests for frequency.py — peak/off-peak gap logic."""
from datetime import datetime

import pytz

from src.frequency import current_gap

TZ = pytz.timezone("Asia/Bangkok")


def bkk(weekday_offset, hh, mm=0):
    """weekday_offset: 0=Mon 14 Sep 2026, 5=Sat, 6=Sun"""
    day = 14 + weekday_offset  # Mon=14, ..., Sat=19, Sun=20 Sep 2026
    # Keep within September
    month = 9
    if day > 20:
        day -= 7
    return TZ.localize(datetime(2026, month, day, hh, mm))


# ── Weekday ────────────────────────────────────────────────────────────────────

def test_weekday_early_morning():
    assert current_gap(bkk(0, 6, 0)) == 5      # 06:00 → early

def test_weekday_rush_hour():
    assert current_gap(bkk(0, 8, 0)) == 7      # 08:00 → AM peak window

def test_weekday_midday():
    assert current_gap(bkk(0, 12, 0)) == 7     # 12:00 → off-peak

def test_weekday_late_afternoon():
    assert current_gap(bkk(0, 16, 45)) == 5    # 16:45 → transition

def test_weekday_pm_peak():
    assert current_gap(bkk(0, 17, 30)) == 4    # 17:30 → PM peak

def test_weekday_evening():
    assert current_gap(bkk(0, 20, 30)) == 5    # 20:30 → post-peak

def test_weekday_late_night():
    assert current_gap(bkk(0, 22, 0)) == 7     # 22:00 → late


# ── Saturday ───────────────────────────────────────────────────────────────────

def test_saturday_morning():
    assert current_gap(bkk(5, 9, 0)) == 7

def test_saturday_afternoon():
    assert current_gap(bkk(5, 14, 0)) == 7

def test_saturday_evening():
    assert current_gap(bkk(5, 17, 0)) == 6

def test_saturday_night():
    assert current_gap(bkk(5, 22, 0)) == 7


# ── Sunday ─────────────────────────────────────────────────────────────────────

def test_sunday_morning():
    assert current_gap(bkk(6, 9, 0)) == 7

def test_sunday_evening():
    assert current_gap(bkk(6, 18, 0)) == 7

def test_sunday_night():
    assert current_gap(bkk(6, 22, 0)) == 7
