# mrt-caller

MRT Blue Line arrival notifier — returns next train times as plain text, designed for iPhone automation via Apple Shortcuts.

## API

```
GET /health                                                               → health check (no auth)
GET /v2/next-train?mrt_depart_station=BL22                               → both directions
GET /v2/next-train?mrt_depart_station=BL22&mrt_destination=lak_song      → หลักสอง only
GET /v2/next-train?mrt_depart_station=BL22&mrt_destination=lak_song      → ท่าพระ only
```

Auth: all endpoints except `/health` require:
```
X-API-Key: <MRT_API_KEY>
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

Terminus stations with no service in a direction return:

```
🚇 หลักสอง (BL38) → หลักสอง
⛔ ไม่มีบริการในทิศทางนี้
```

## Run

```bash
# Start
docker compose up --detach

# Rebuild after code changes
docker compose up --detach --build

# Logs
docker compose logs -f
```

## Test

```bash
uv run pytest -v
```

## Stack

Python 3.12 · FastAPI · uv · Docker Compose (`restart: always`) · Cloudflare Tunnel
