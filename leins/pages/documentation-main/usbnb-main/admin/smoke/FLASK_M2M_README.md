# NetworkBuster Flask M2M Middleware

**Moon 2 Mars Deep Space AI Network — Cislunar Nexus**

This is the central Machine-to-Machine (M2M) broker for the NetworkBuster OS. All AI nodes, bots, and hardware agents authenticate and push their telemetry through this middleware, which then distributes the aggregated data to the Vite React UI.

---

## Requirements

- Python 3.8+
- Flask
- flask-cors
- psutil

### Install Dependencies
```bash
pip install Flask flask-cors psutil
```

---

## Starting the Middleware

```bash
python server.py
```

The broker will come online at:
- **Local:** `http://localhost:8080`
- **Network:** `http://192.168.1.14:8080`

---

## API Reference

### Authentication
All M2M ingestion routes require the following header:

```
X-API-KEY: NEXUS-77X-AUTH
```

Requests without this key will receive a `401 Unauthorized` response.

---

### `POST /api/m2m/telemetry`
**Ingestion endpoint.** Used by machines to push telemetry data into the broker.

**Headers:**
```
X-API-KEY: NEXUS-77X-AUTH
Content-Type: application/json
```

**Body:**
```json
{
  "cpu": 87.3,
  "memory": 64.5
}
```

**Response (200 OK):**
```json
{
  "status": "Telemetry Ingested successfully."
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8080/api/m2m/telemetry \
  -H "X-API-KEY: NEXUS-77X-AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"cpu\": 87.3, \"memory\": 64.5}"
```

---

### `GET /api/system-state`
**Distribution endpoint.** Used by the Vite UI to fetch the latest aggregated telemetry. No API key required.

If no machine has pushed data in the last 5 seconds, the middleware automatically falls back to reading the **local machine's actual CPU and memory** via `psutil`.

**Response (200 OK) — M2M Source:**
```json
{
  "cpu": 87.3,
  "memory": 64.5,
  "source": "M2M Network"
}
```

**Response (200 OK) — Fallback Source:**
```json
{
  "cpu": 12.1,
  "memory": 55.3,
  "source": "Local Fallback"
}
```

**curl Example:**
```bash
curl http://localhost:8080/api/system-state
```

---

## Connecting a Machine (Node)

Any machine that needs to report into the Nexus must:

1. Have network access to `http://192.168.1.14:8080`
2. Know the API Key: `NEXUS-77X-AUTH`
3. POST JSON telemetry to `/api/m2m/telemetry` on a regular interval

### Example: Python Node (using no external libraries)
```python
import urllib.request, json, time

while True:
    payload = json.dumps({"cpu": 90.1, "memory": 70.4}).encode()
    req = urllib.request.Request(
        "http://192.168.1.14:8080/api/m2m/telemetry",
        data=payload,
        headers={"X-API-KEY": "NEXUS-77X-AUTH", "Content-Type": "application/json"},
        method="POST"
    )
    urllib.request.urlopen(req)
    time.sleep(2)
```

---

## Simulate a Deep Space AI Node

A pre-built simulator is included. Run it in a separate terminal:

```bash
python mock_machine.py
```

This will transmit randomized high-load telemetry (CPU 70–99%) every 2 seconds, simulating a Moon 2 Mars AI node under stress.

---

## CLI Interaction Tool

Use `interact.py` to manually communicate with the middleware from any terminal:

```bash
# Check current system state
python interact.py status

# Manually push telemetry values
python interact.py push 87.5 64.2

# Run continuous AI node simulation
python interact.py simulate

# Open the Nexus UI in browser
python interact.py open
```

---

## Architecture Overview

```
[ AI Node / Bot ]  --POST /api/m2m/telemetry--> [ Flask M2M Broker :8080 ]
                                                          |
                                                  [ State Manager ]
                                                          |
[ Vite React UI :5173 ] <--GET /api/system-state---------+
```

---

## Security Notes

- Change `API_KEY` in `server.py` from `NEXUS-77X-AUTH` to a strong secret before deploying to a wider network.
- This is a **development server**. For production deployment, run behind a WSGI server like `gunicorn`:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:8080 server:app
  ```
