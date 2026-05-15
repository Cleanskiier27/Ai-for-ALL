from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import time

app = Flask(__name__)
CORS(app) # Allow Vite frontend to fetch data

# ---------------------------------------------------------
# IN-MEMORY STATE MANAGER (The M2M Broker)
# ---------------------------------------------------------
system_state = {
    "telemetry": {
        "cpu": 0.0,
        "memory": 0.0,
        "last_updated": 0
    },
    "ledger_events": [],
    "active_machines": 0
}

API_KEY = "NEXUS-77X-AUTH"

# Middleware to check auth on M2M routes
@app.before_request
def check_m2m_auth():
    if request.path.startswith('/api/m2m'):
        key = request.headers.get('X-API-KEY')
        if key != API_KEY:
            return jsonify({"error": "Unauthorized Access. Invalid API Key."}), 401

# ---------------------------------------------------------
# 1. INGESTION LAYER (Machines POST data here)
# ---------------------------------------------------------
@app.route('/api/m2m/telemetry', methods=['POST'])
def ingest_telemetry():
    data = request.json
    
    system_state["telemetry"]["cpu"] = data.get("cpu", 0.0)
    system_state["telemetry"]["memory"] = data.get("memory", 0.0)
    system_state["telemetry"]["last_updated"] = time.time()
    system_state["active_machines"] += 1
    
    return jsonify({"status": "Telemetry Ingessed successfully."}), 200

# ---------------------------------------------------------
# 2. DISTRIBUTION LAYER (Vite UI GETs data here)
# ---------------------------------------------------------
@app.route('/api/system-state', methods=['GET'])
def get_system_state():
    # If no machines are pushing data, fallback to local host metrics
    if time.time() - system_state["telemetry"]["last_updated"] > 5:
        return jsonify({
            "cpu": psutil.cpu_percent(interval=None),
            "memory": psutil.virtual_memory().percent,
            "source": "Local Fallback"
        }), 200
        
    return jsonify({
        "cpu": system_state["telemetry"]["cpu"],
        "memory": system_state["telemetry"]["memory"],
        "source": "M2M Network"
    }), 200

if __name__ == '__main__':
    print("NetworkBuster M2M Middleware Online. Port 8080.")
    app.run(host='0.0.0.0', port=8080)
