# mrt-caller

MRT Blue Line arrival notifier — returns next train times as plain text, designed for iPhone geofence automation via Apple Shortcuts.

- **v1** (Tha Phra station, 3 platforms): `/` and `/v1`
- **v2** (any of the 38 Blue Line stations, 2 directions): `/v2`

## Station Layout

```
MRT ท่าพระ (BL01)

  ชั้น 2
  ├── ชานชาลา 1  →  หลักสอง (BL38) ตรง               05:43 – 00:18
  └── ชานชาลา 2  →  ท่าพระ (BL01)  ผ่านบางซื่อ        05:43 – 23:19

  ชั้น 3
  └── ชานชาลา 3-4 → หลักสอง (BL38) ผ่านบางซื่อ        05:43 – 00:18

  (เสาร์-อาทิตย์/วันหยุด: ขบวนแรก 05:59)
```

## v2 API (all 38 stations)

```
GET /v2/next-train?mrt_depart_station=BL22                  → both directions
GET /v2/next-train?mrt_depart_station=BL22&mrt_destination=lak_song  → หลักสอง
GET /v2/next-train?mrt_depart_station=BL22&mrt_destination=tha_phra  → ท่าพระ (loop)
```

### Query Params

| Param | Default | Values | Description |
|---|---|---|---|
| `mrt_depart_station` | *(required)* | `BL01`–`BL38` | Case-insensitive; `1`–`38` also accepted |
| `mrt_destination` | *(both)* | `lak_song` `tha_phra` | Omit to show both directions |
| `count` | `3` | `1`–`5` | Number of upcoming trains to show |
| `gap` | auto | `1`–`30` | Headway override — default is auto-detected from time of day (peak/off-peak) |

### Example Response

```
🚇 สุขุมวิท (BL22) → หลักสอง
⏱ 17:13  17:20  17:27
🕐 อีก 4 นาที  วันธรรมดา Peak  ทุก 7 นาที

🚇 สุขุมวิท (BL22) → ท่าพระ
⏱ 17:15  17:22  17:29
🕐 อีก 6 นาที  วันธรรมดา Peak  ทุก 7 นาที
```

Stations with no service in a direction (e.g. BL38 → หลักสอง, the terminus) return:

```
🚇 หลักสอง (BL38) → หลักสอง
⛔ ไม่มีบริการในทิศทางนี้
```

## v1 API (Tha Phra platforms)

```
GET /health                                  → health check (also at /v1/health)
GET /next-train                              → ทั้ง 3 ชานชาลา (also at /v1/next-train)
GET /next-train?mrt_destination=platform_1  → ชั้น 2 → หลักสอง ตรง
GET /next-train?mrt_destination=platform_2  → ชั้น 2 → ท่าพระ ผ่านบางซื่อ
GET /next-train?mrt_destination=platform_34 → ชั้น 3 → หลักสอง ผ่านบางซื่อ
```

### Query Params

| Param | Default | Values | Description |
|---|---|---|---|
| `mrt_destination` | *(all)* | `platform_1` `platform_2` `platform_34` | Omit to show all platforms |
| `gap` | `5` | `4`–`10` | Train headway in minutes (5 or 6 — to be locked after real-world observation) |
| `count` | `3` | `1`–`5` | Number of upcoming trains to show |

### Example Response

```
🚇 ชานชาลา 1 (ชั้น 2) → หลักสอง
⏱ 17:13  17:18  17:23
🕐 อีก 4 นาที

🚇 ชานชาลา 2 (ชั้น 2) → ท่าพระ ผ่านบางซื่อ
⏱ 17:13  17:18  17:23
🕐 อีก 4 นาที

🚇 ชานชาลา 3-4 (ชั้น 3) → หลักสอง ผ่านบางซื่อ
⏱ 17:13  17:18  17:23
🕐 อีก 4 นาที

วันธรรมดา  ทุก 5 นาที
```

## iPhone Shortcuts Setup

1. **Shortcuts** app → **+** → name: `MRT ท่าพระ`
2. Add action: **Get Contents of URL**
   - URL: `https://mrt-caller.thepbordin.tech/next-train?gap=5`
   - Method: `GET`
   - Headers:
     - `CF-Access-Client-Id`: *(your service token)*
     - `CF-Access-Client-Secret`: *(your service token secret)*
3. Add action: **Show Notification**
   - Title: `🚇 MRT ท่าพระ`
   - Body: **Contents of URL**
4. **Automation** tab → **+** → **Personal Automation** → **Arrive**
   - Location: MRT ท่าพระ (13.7278° N, 100.4773° E) · radius 100 m
   - Action: **Run Shortcut** → `MRT ท่าพระ`
   - Disable **Ask Before Running**

## Run

```bash
# Start
docker compose up --detach

# Rebuild after code changes
docker compose up --detach --build

# Logs
docker compose logs -f

# Test locally
curl "http://localhost:8700/next-train?gap=5"
```

## Test

```bash
uv run pytest -v   # 45 tests
```

## Stack

Python 3.12 · FastAPI · uv · Docker Compose (`restart: always`) · Cloudflare Tunnel
