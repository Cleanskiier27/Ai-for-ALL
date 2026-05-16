#!/usr/bin/env python3
"""
NetworkBuster SSH Telemetry Miner
Moon 2 Mars Deep Space AI Network

Automatically SSHes into configured remote nodes, mines their
CPU/memory/disk telemetry, and injects it into the NB-M2M middleware.

Usage:
  python ssh_miner.py                  - Run all configured nodes continuously
  python ssh_miner.py --list           - List all configured nodes
  python ssh_miner.py --node NODE_ID   - Run a single node only
  python ssh_miner.py --once           - Single poll pass, then exit
"""

import sys
import time
import json
import threading
import urllib.request
import urllib.error

try:
    import paramiko
    SSH_AVAILABLE = True
except ImportError:
    SSH_AVAILABLE = False
    print("[WARN] paramiko not installed. Run: pip install paramiko")

# ---------------------------------------------------------
# NODE CONFIGURATION — Add your nodes here
# ---------------------------------------------------------
NODES = [
    {
        "id": "MOON-NODE-01",
        "host": "192.168.1.22",
        "port": 22,
        "user": "pi",
        "key_path": "~/.ssh/id_rsa",       # Use key auth (recommended)
        "password": None,                    # Or set a password string
        "label": "Luna Relay Alpha",
    },
    {
        "id": "SAT-GPU-07",
        "host": "192.168.1.33",
        "port": 22,
        "user": "admin",
        "key_path": "~/.ssh/id_rsa",
        "password": None,
        "label": "Satellite GPU Cluster B",
    },
]

MIDDLEWARE_URL = "http://localhost:8080/api/m2m/telemetry"
API_KEY        = "NEXUS-77X-AUTH"
POLL_INTERVAL  = 5  # seconds between polls

# Commands to run on each remote node (standard Linux)
REMOTE_COMMANDS = {
    "cpu":    "python3 -c \"import psutil; print(psutil.cpu_percent(interval=1))\" 2>/dev/null || top -bn1 | grep 'Cpu(s)' | awk '{print $2}'",
    "memory": "python3 -c \"import psutil; print(psutil.virtual_memory().percent)\" 2>/dev/null || free | awk 'NR==2{printf \"%.1f\", $3*100/$2}'",
}

def timestamp():
    return time.strftime('%H:%M:%S')

def push_to_middleware(node_id, cpu, mem):
    payload = json.dumps({"cpu": float(cpu), "memory": float(mem)}).encode()
    req = urllib.request.Request(
        MIDDLEWARE_URL, data=payload,
        headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status == 200
    except Exception as e:
        print(f"  [{timestamp()}] [{node_id}] Middleware push failed: {e}")
        return False

def ssh_exec(client, cmd):
    _, stdout, _ = client.exec_command(cmd)
    return stdout.read().decode().strip()

def mine_node(node):
    node_id = node["id"]
    
    if not SSH_AVAILABLE:
        print(f"  [{node_id}] SSH unavailable — paramiko missing.")
        return

    print(f"  [{timestamp()}] [{node_id}] Connecting to {node['user']}@{node['host']}:{node['port']}...")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        connect_kwargs = {
            "hostname": node["host"],
            "port":     node["port"],
            "username": node["user"],
            "timeout":  10,
        }
        if node.get("key_path"):
            import os
            connect_kwargs["key_filename"] = os.path.expanduser(node["key_path"])
        if node.get("password"):
            connect_kwargs["password"] = node["password"]
        
        client.connect(**connect_kwargs)
        print(f"  [{timestamp()}] [{node_id}] ✓ SSH uplink established.")

        while True:
            cpu = ssh_exec(client, REMOTE_COMMANDS["cpu"])
            mem = ssh_exec(client, REMOTE_COMMANDS["memory"])

            try:
                cpu_f = float(cpu)
                mem_f = float(mem)
            except ValueError:
                print(f"  [{timestamp()}] [{node_id}] ✗ Could not parse telemetry: cpu='{cpu}' mem='{mem}'")
                time.sleep(POLL_INTERVAL)
                continue

            ok = push_to_middleware(node_id, cpu_f, mem_f)
            status = "✓" if ok else "✗"
            print(f"  [{timestamp()}] [{node_id}] {status} CPU: {cpu_f}% | MEM: {mem_f}%")

            time.sleep(POLL_INTERVAL)

    except paramiko.AuthenticationException:
        print(f"  [{timestamp()}] [{node_id}] ✗ Auth failed. Check key/password config.")
    except paramiko.NoValidConnectionsError:
        print(f"  [{timestamp()}] [{node_id}] ✗ Cannot connect to {node['host']}:{node['port']}.")
    except Exception as e:
        print(f"  [{timestamp()}] [{node_id}] ✗ Error: {e}")
    finally:
        try: client.close()
        except: pass
        print(f"  [{timestamp()}] [{node_id}] SSH uplink closed. Retrying in 15s...")
        time.sleep(15)

def run_node_loop(node):
    """Retry loop for a single node — keeps reconnecting on disconnect."""
    while True:
        mine_node(node)

def list_nodes():
    print("\n  Configured NB-SSH Nodes:")
    print("  " + "─" * 50)
    for n in NODES:
        print(f"  {n['id']:20} {n['user']}@{n['host']}:{n['port']}  ({n['label']})")
    print()

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--list" in args:
        list_nodes()
        sys.exit(0)

    print("=" * 55)
    print("  NETWORKBUSTER SSH TELEMETRY MINER ONLINE")
    print("  Moon 2 Mars Deep Space AI Network")
    print("=" * 55)

    target_nodes = NODES

    if "--node" in args:
        idx = args.index("--node")
        node_id = args[idx + 1] if idx + 1 < len(args) else None
        target_nodes = [n for n in NODES if n["id"] == node_id]
        if not target_nodes:
            print(f"  Node '{node_id}' not found. Use --list to see available nodes.")
            sys.exit(1)

    once = "--once" in args

    if once:
        for node in target_nodes:
            mine_node(node)
    else:
        threads = []
        for node in target_nodes:
            t = threading.Thread(target=run_node_loop, args=(node,), daemon=True)
            t.start()
            threads.append(t)
            print(f"  [{timestamp()}] Spawned miner thread for {node['id']}")

        print(f"\n  Mining {len(target_nodes)} node(s). Press Ctrl+C to stop.\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n  Uplinks terminated.")
