import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psutil
import time

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# IN-MEMORY STATE MANAGER (The M2M Broker)
# ---------------------------------------------------------
system_state = {
    "telemetry": {
        "cpu": 0.0,
        "memory": 0.0,
        "last_updated": 0
    },
    "active_machines": 0
}

API_KEY = os.environ.get("NETWORKBUSTER_API_KEY", "")
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# Middleware to check auth on M2M routes only
@app.before_request
def check_m2m_auth():
    if request.path.startswith('/api/m2m'):
        key = request.headers.get('X-API-KEY')
        if key != API_KEY:
            return jsonify({"error": "Unauthorized. Invalid API Key."}), 401

# ---------------------------------------------------------
# HTML TEMPLATE ROUTES (Front Door & Dashboard)
# ---------------------------------------------------------
ROUTE_MAP = {
    '/': 'index.html',
    '/dashboard': 'dashboard.html',
    '/liquidations': 'liquidations.html',
    '/forensics': 'forensics.html',
    '/yield_ops': 'yield_ops.html',
    '/lien_registry': 'lien_registry.html',
}

def serve_template(filename):
    try:
        return send_from_directory(TEMPLATES_DIR, filename)
    except Exception as e:
        return f"Template not found: {filename} — {e}", 404

@app.route('/')
def index():
    return serve_template('index.html')

@app.route('/dashboard')
def dashboard():
    return serve_template('dashboard.html')

@app.route('/liquidations')
def liquidations():
    return serve_template('liquidations.html')

@app.route('/forensics')
def forensics():
    return serve_template('forensics.html')

@app.route('/yield_ops')
def yield_ops():
    return serve_template('yield_ops.html')

@app.route('/sat_gpu')
def sat_gpu():
    return serve_template('sat_gpu.html')

@app.route('/nb_command')
def nb_command():
    return serve_template('nb_command.html')

@app.route('/lien_registry')
def lien_registry():
    return serve_template('lien_registry.html')

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
    return jsonify({"status": "Telemetry ingested successfully."}), 200

# ---------------------------------------------------------
# 2. DISTRIBUTION LAYER (Vite UI & external GETs data here)
# ---------------------------------------------------------
@app.route('/api/system-state', methods=['GET'])
def get_system_state():
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

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    return get_system_state()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "node": "NetworkBuster-M2M"}), 200

if __name__ == '__main__':
    print("NetworkBuster M2M Middleware Online. Port 8080.")
    app.run(host='0.0.0.0', port=8080)
