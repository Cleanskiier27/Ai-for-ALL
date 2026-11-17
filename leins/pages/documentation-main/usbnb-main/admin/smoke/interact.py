#!/usr/bin/env python3
import os
"""
NetworkBuster M2M Nexus - Redundant Interaction Script
Moon 2 Mars Deep Space AI Network

Usage:
  python interact.py status          - Get live system state from middleware
  python interact.py push <cpu> <mem> - Manually push telemetry to middleware
  python interact.py simulate         - Run continuous AI node simulation
  python interact.py open             - Open the Nexus UI in browser
"""

import sys
import json
import time
import random
import urllib.request
import urllib.error
import webbrowser

MIDDLEWARE_HOST = "http://localhost:8080"
API_KEY = os.environ.get("NETWORKBUSTER_API_KEY", "")
HEADERS = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}

def make_request(method, path, body=None):
    url = MIDDLEWARE_HOST + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"[ERROR] Middleware unreachable: {e}")
    return None

def status():
    print("Querying Moon 2 Mars Nexus state...")
    data = make_request("GET", "/api/system-state")
    if data:
        print(f"\n  CPU Usage : {data.get('cpu')}%")
        print(f"  MEM Usage : {data.get('memory')}%")
        print(f"  Source    : {data.get('source', 'Unknown')}")
    print()

def push(cpu, mem):
    print(f"Pushing telemetry => CPU: {cpu}% | MEM: {mem}%")
    result = make_request("POST", "/api/m2m/telemetry", {"cpu": float(cpu), "memory": float(mem)})
    if result:
        print(f"[OK] Middleware acknowledged: {result.get('status')}")

def simulate():
    print("Initializing Moon 2 Mars AI Node Simulation...")
    print("Press Ctrl+C to terminate uplink.\n")
    while True:
        cpu = round(random.uniform(70.0, 99.9), 1)
        mem = round(random.uniform(60.0, 85.0), 1)
        result = make_request("POST", "/api/m2m/telemetry", {"cpu": cpu, "memory": mem})
        if result:
            print(f"[{time.strftime('%H:%M:%S')}] Transmitted -> CPU {cpu}% | MEM {mem}%")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Link lost. Retrying...")
        time.sleep(2)

def open_ui():
    url = "http://localhost:5173"
    print(f"Opening Nexus UI at {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "status":
        status()
    elif args[0] == "push" and len(args) == 3:
        push(args[1], args[2])
    elif args[0] == "simulate":
        simulate()
    elif args[0] == "open":
        open_ui()
    else:
        print(__doc__)
