"""
MRT Blue Line — full-line timetable (v2), all 38 BL stations.
Source: BEM official timetable (2026-09-14).

Times are "HH:MM" strings; a last train after midnight (e.g. "00:30")
means 00:30 on the following day.

BL38 หลักสอง is the terminus — no lak_song departures.
BL01 ท่าพระ is the loop junction — it has departures in BOTH directions.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import pytz

TZ = pytz.timezone("Asia/Bangkok")

DIRECTION_LAK_SONG = "lak_song"   # → หลักสอง BL38
DIRECTION_THA_PHRA = "tha_phra"   # → ท่าพระ BL01 (loop via บางซื่อ)
ALL_DIRECTIONS = [DIRECTION_LAK_SONG, DIRECTION_THA_PHRA]

DIRECTION_LABELS = {
    DIRECTION_LAK_SONG: "หลักสอง",
    DIRECTION_THA_PHRA: "ท่าพระ",
}


def _wd(lf: str, ll: str, tf: str, tl: str):
    """Build the directions dict for a normal (two-way) station."""
    return {
        "lak_song": {"weekday": {"first": lf, "last": ll},
                     "weekend": {"first": tf, "last": tl}},
    }


# fmt: off
STATIONS: dict[str, dict] = {
    "BL38": {"name_th": "หลักสอง",       "name_en": "Lak Song",
             "directions": {"lak_song": None,
                            "tha_phra": {"weekday": {"first": "05:30", "last": "23:08"},
                                          "weekend": {"first": "05:57", "last": "23:08"}}}},
    "BL37": {"name_th": "บางแค",         "name_en": "Bang Khae",
             "directions": _wd("05:32", "00:30", "06:01", "00:27")
                 | {"tha_phra": {"weekday": {"first": "05:32", "last": "23:10"},
                                  "weekend": {"first": "06:00", "last": "23:10"}}}},
    "BL36": {"name_th": "ภาษีเจริญ",     "name_en": "Phasi Charoen",
             "directions": _wd("05:36", "00:28", "05:59", "00:25")
                 | {"tha_phra": {"weekday": {"first": "05:34", "last": "23:12"},
                                  "weekend": {"first": "06:01", "last": "23:12"}}}},
    "BL35": {"name_th": "เพชรเกษม48",    "name_en": "Phetkasem 48",
             "directions": _wd("05:40", "00:26", "05:57", "00:23")
                 | {"tha_phra": {"weekday": {"first": "05:36", "last": "23:14"},
                                  "weekend": {"first": "05:56", "last": "23:14"}}}},
    "BL34": {"name_th": "บางหว้า",       "name_en": "Bang Wa",
             "directions": _wd("05:38", "00:24", "05:55", "00:21")
                 | {"tha_phra": {"weekday": {"first": "05:38", "last": "23:16"},
                                  "weekend": {"first": "05:58", "last": "23:16"}}}},
    "BL33": {"name_th": "บางไผ่",        "name_en": "Bang Phai",
             "directions": _wd("05:44", "00:22", "06:01", "00:20")
                 | {"tha_phra": {"weekday": {"first": "05:40", "last": "23:18"},
                                  "weekend": {"first": "06:00", "last": "23:18"}}}},
    "BL01": {"name_th": "ท่าพระ",        "name_en": "Tha Phra",
             "directions": {"lak_song": {"weekday": {"first": "05:43", "last": "00:18"},
                                          "weekend": {"first": "05:59", "last": "00:18"}},
                            "tha_phra": {"weekday": {"first": "05:43", "last": "23:19"},
                                          "weekend": {"first": "05:59", "last": "23:19"}}}},
    "BL32": {"name_th": "อิสรภาพ",       "name_en": "Itsaraphap",
             "directions": _wd("05:51", "00:18", "05:57", "00:16")
                 | {"tha_phra": {"weekday": {"first": "05:45", "last": "23:22"},
                                  "weekend": {"first": "05:56", "last": "23:22"}}}},
    "BL31": {"name_th": "สนามไชย",       "name_en": "Sanam Chai",
             "directions": _wd("05:48", "00:16", "06:02", "00:13")
                 | {"tha_phra": {"weekday": {"first": "05:47", "last": "23:24"},
                                  "weekend": {"first": "05:58", "last": "23:24"}}}},
    "BL30": {"name_th": "สามยอด",        "name_en": "Sam Yot",
             "directions": _wd("05:53", "00:14", "06:00", "00:12")
                 | {"tha_phra": {"weekday": {"first": "05:49", "last": "23:26"},
                                  "weekend": {"first": "06:00", "last": "23:26"}}}},
    "BL29": {"name_th": "วัดมังกร",      "name_en": "Wat Mangkon",
             "directions": _wd("05:51", "00:12", "05:58", "00:10")
                 | {"tha_phra": {"weekday": {"first": "05:51", "last": "23:28"},
                                  "weekend": {"first": "05:55", "last": "23:28"}}}},
    "BL28": {"name_th": "หัวลำโพง",      "name_en": "Hua Lamphong",
             "directions": _wd("06:00", "00:10", "05:56", "00:08")
                 | {"tha_phra": {"weekday": {"first": "05:53", "last": "23:30"},
                                  "weekend": {"first": "05:57", "last": "23:30"}}}},
    "BL27": {"name_th": "สามย่าน",       "name_en": "Sam Yan",
             "directions": _wd("05:57", "00:08", "06:01", "00:05")
                 | {"tha_phra": {"weekday": {"first": "05:55", "last": "23:32"},
                                  "weekend": {"first": "05:59", "last": "23:32"}}}},
    "BL26": {"name_th": "สีลม",          "name_en": "Si Lom",
             "directions": _wd("05:59", "00:06", "06:00", "00:04")
                 | {"tha_phra": {"weekday": {"first": "05:57", "last": "23:34"},
                                  "weekend": {"first": "06:01", "last": "23:34"}}}},
    "BL25": {"name_th": "ลุมพินี",       "name_en": "Lumphini",
             "directions": _wd("05:57", "00:04", "05:58", "00:02")
                 | {"tha_phra": {"weekday": {"first": "05:59", "last": "23:35"},
                                  "weekend": {"first": "05:55", "last": "23:35"}}}},
    "BL24": {"name_th": "คลองเตย",       "name_en": "Khlong Toei",
             "directions": _wd("05:55", "00:03", "05:56", "00:00")
                 | {"tha_phra": {"weekday": {"first": "05:54", "last": "23:37"},
                                  "weekend": {"first": "05:57", "last": "23:37"}}}},
    "BL23": {"name_th": "ศูนย์การประชุมฯ", "name_en": "Queen Sirikit National Convention Centre",
             "directions": _wd("05:54", "00:01", "05:55", "23:58")
                 | {"tha_phra": {"weekday": {"first": "05:55", "last": "23:39"},
                                  "weekend": {"first": "05:59", "last": "23:39"}}}},
    "BL22": {"name_th": "สุขุมวิท",      "name_en": "Sukhumvit",
             "directions": _wd("05:58", "23:58", "05:59", "23:56")
                 | {"tha_phra": {"weekday": {"first": "05:58", "last": "23:42"},
                                  "weekend": {"first": "06:02", "last": "23:42"}}}},
    "BL21": {"name_th": "เพชรบุรี",      "name_en": "Phetchaburi",
             "directions": _wd("05:56", "23:56", "05:57", "23:54")
                 | {"tha_phra": {"weekday": {"first": "05:53", "last": "23:44"},
                                  "weekend": {"first": "06:04", "last": "23:44"}}}},
    "BL20": {"name_th": "พระราม9",       "name_en": "Phra Ram 9",
             "directions": _wd("05:54", "23:54", "05:55", "23:52")
                 | {"tha_phra": {"weekday": {"first": "05:55", "last": "23:45"},
                                  "weekend": {"first": "06:05", "last": "23:45"}}}},
    "BL19": {"name_th": "ศูนย์วัฒนธรรมฯ", "name_en": "Thailand Cultural Centre",
             "directions": _wd("05:55", "23:52", "06:05", "23:50")
                 | {"tha_phra": {"weekday": {"first": "05:54", "last": "23:48"},
                                  "weekend": {"first": "06:01", "last": "23:48"}}}},
    "BL18": {"name_th": "ห้วยขวาง",      "name_en": "Huai Khwang",
             "directions": _wd("05:59", "23:50", "06:03", "23:47")
                 | {"tha_phra": {"weekday": {"first": "05:56", "last": "23:50"},
                                  "weekend": {"first": "05:55", "last": "23:50"}}}},
    "BL17": {"name_th": "สุทธิสาร",      "name_en": "Sutthisan",
             "directions": _wd("05:57", "23:48", "06:01", "23:45")
                 | {"tha_phra": {"weekday": {"first": "05:58", "last": "23:52"},
                                  "weekend": {"first": "05:57", "last": "23:52"}}}},
    "BL16": {"name_th": "รัชดาภิเษก",     "name_en": "Ratchadaphisek",
             "directions": _wd("05:55", "23:46", "05:59", "23:43")
                 | {"tha_phra": {"weekday": {"first": "05:56", "last": "23:54"},
                                  "weekend": {"first": "05:59", "last": "23:54"}}}},
    "BL15": {"name_th": "ลาดพร้าว",      "name_en": "Lat Phrao",
             "directions": _wd("05:53", "23:44", "05:57", "23:42")
                 | {"tha_phra": {"weekday": {"first": "05:58", "last": "23:56"},
                                  "weekend": {"first": "05:55", "last": "23:56"}}}},
    "BL14": {"name_th": "พหลโยธิน",      "name_en": "Phahon Yothin",
             "directions": _wd("05:58", "23:42", "05:55", "23:39")
                 | {"tha_phra": {"weekday": {"first": "05:57", "last": "23:58"},
                                  "weekend": {"first": "05:57", "last": "23:58"}}}},
    "BL13": {"name_th": "สวนจตุจักร",    "name_en": "Chatuchak Park",
             "directions": _wd("05:56", "23:39", "05:59", "23:37")
                 | {"tha_phra": {"weekday": {"first": "05:56", "last": "00:01"},
                                  "weekend": {"first": "05:59", "last": "00:01"}}}},
    "BL12": {"name_th": "กำแพงเพชร",     "name_en": "Kamphaeng Phet",
             "directions": _wd("05:54", "23:37", "05:57", "23:35")
                 | {"tha_phra": {"weekday": {"first": "05:54", "last": "00:03"},
                                  "weekend": {"first": "05:55", "last": "00:03"}}}},
    "BL11": {"name_th": "บางซื่อ",       "name_en": "Bang Sue",
             "directions": _wd("05:52", "23:35", "05:55", "23:33")
                 | {"tha_phra": {"weekday": {"first": "05:56", "last": "00:05"},
                                  "weekend": {"first": "05:57", "last": "00:05"}}}},
    "BL10": {"name_th": "เตาปูน",        "name_en": "Tao Poon",
             "directions": _wd("05:50", "23:33", "05:53", "23:30")
                 | {"tha_phra": {"weekday": {"first": "05:55", "last": "00:07"},
                                  "weekend": {"first": "05:59", "last": "00:07"}}}},
    "BL09": {"name_th": "บางโพ",         "name_en": "Bang Pho",
             "directions": _wd("05:55", "23:31", "05:58", "23:29")
                 | {"tha_phra": {"weekday": {"first": "05:57", "last": "00:09"},
                                  "weekend": {"first": "06:00", "last": "00:09"}}}},
    "BL08": {"name_th": "บางอ้อ",        "name_en": "Bang O",
             "directions": _wd("05:52", "23:28", "05:56", "23:26")
                 | {"tha_phra": {"weekday": {"first": "05:53", "last": "00:11"},
                                  "weekend": {"first": "05:55", "last": "00:11"}}}},
    "BL07": {"name_th": "บางพลัด",       "name_en": "Bang Plad",
             "directions": _wd("05:50", "23:27", "06:02", "23:24")
                 | {"tha_phra": {"weekday": {"first": "05:51", "last": "00:13"},
                                  "weekend": {"first": "05:57", "last": "00:13"}}}},
    "BL06": {"name_th": "สิรินธร",       "name_en": "Sirindhorn",
             "directions": _wd("05:48", "23:25", "06:00", "23:22")
                 | {"tha_phra": {"weekday": {"first": "05:50", "last": "00:15"},
                                  "weekend": {"first": "05:59", "last": "00:15"}}}},
    "BL05": {"name_th": "บางยี่ขัน",     "name_en": "Bang Yi Khan",
             "directions": _wd("05:46", "23:23", "05:58", "23:20")
                 | {"tha_phra": {"weekday": {"first": "05:49", "last": "00:17"},
                                  "weekend": {"first": "06:01", "last": "00:17"}}}},
    "BL04": {"name_th": "บางขุนนนท์",    "name_en": "Bang Khun Non",
             "directions": _wd("05:43", "23:20", "05:55", "23:17")
                 | {"tha_phra": {"weekday": {"first": "05:49", "last": "00:20"},
                                  "weekend": {"first": "05:55", "last": "00:20"}}}},
    "BL03": {"name_th": "ไฟฉาย",         "name_en": "Fai Chai",
             "directions": _wd("05:41", "23:18", "06:00", "23:16")
                 | {"tha_phra": {"weekday": {"first": "05:44", "last": "00:22"},
                                  "weekend": {"first": "05:57", "last": "00:22"}}}},
    "BL02": {"name_th": "จรัญฯ13",       "name_en": "Charan 13",
             "directions": _wd("05:39", "23:16", "05:58", "23:13")
                 | {"tha_phra": {"weekday": {"first": "05:40", "last": "00:24"},
                                  "weekend": {"first": "06:00", "last": "00:24"}}}},
}
# fmt: on


def _resolve_station(station: str) -> str:
    """Accept 'BL22', 'bl22', or '22' → canonical 'BL22'."""
    s = station.strip().upper()
    if not s.startswith("BL"):
        s = "BL" + s
    if s not in STATIONS:
        raise ValueError(f"Unknown station '{station}'. Use BL01–BL38.")
    return s


def _to_abs_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def next_trains_v2(
    now: datetime,
    station: str,
    direction: str,
    gap_min: int = 5,
    count: int = 3,
) -> list[datetime]:
    """
    Return the next `count` train departures from `station` toward `direction`.

    Args:
        now:       Timezone-aware datetime (Asia/Bangkok preferred).
        station:   "BL01"–"BL38", case-insensitive; "1"–"38" also accepted.
        direction: "lak_song" (→ หลักสอง BL38) or "tha_phra" (→ ท่าพระ BL01).
        gap_min:   Train headway in minutes.
        count:     Maximum trains to return.

    Returns:
        List of tz-aware datetimes (Asia/Bangkok).
        Empty if the station has no service in that direction or service has ended.

    Raises:
        ValueError: on unknown station or direction.
    """
    code = _resolve_station(station)
    if direction not in ALL_DIRECTIONS:
        raise ValueError(f"Unknown direction '{direction}'. Use: {ALL_DIRECTIONS}")

    sched = STATIONS[code]["directions"][direction]
    if sched is None:  # e.g. BL38 has no lak_song departures
        return []

    now_bkk = now.astimezone(TZ)
    day = sched["weekday" if now_bkk.weekday() < 5 else "weekend"]
    first_abs = _to_abs_minutes(day["first"])
    last_abs = _to_abs_minutes(day["last"])
    if last_abs < first_abs:      # last train after midnight
        last_abs += 24 * 60

    now_abs = now_bkk.hour * 60 + now_bkk.minute
    if now_abs < 5 * 60:          # past-midnight zone (00:xx–04:xx)
        now_abs += 24 * 60

    results: list[datetime] = []
    t = first_abs
    while t <= last_abs and len(results) < count:
        if t > now_abs:
            base_date = now_bkk.date()
            if t >= 24 * 60:
                base_date += timedelta(days=1)
            results.append(
                TZ.localize(datetime(base_date.year, base_date.month, base_date.day,
                                     (t // 60) % 24, t % 60))
            )
        t += gap_min

    return results


def station_label(station: str) -> str:
    """Return e.g. 'สุขุมวิท (BL22)'."""
    code = _resolve_station(station)
    return f"{STATIONS[code]['name_th']} ({code})"


def last_train_str_v2(station: str, direction: str, is_weekday: bool) -> str:
    """Return the last-train time for a direction, e.g. '23:58'."""
    code = _resolve_station(station)
    sched = STATIONS[code]["directions"][direction]
    if sched is None:
        return "—"
    last = sched["weekday" if is_weekday else "weekend"]["last"]
    h, m = last.split(":")
    return f"{int(h) % 24:02d}:{m}"
