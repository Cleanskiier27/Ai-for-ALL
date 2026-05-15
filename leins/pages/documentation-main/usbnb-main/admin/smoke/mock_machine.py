import urllib.request
import urllib.error
import json
import time
import random

MIDDLEWARE_URL = "http://localhost:8080/api/m2m/telemetry"
HEADERS = {
    "X-API-KEY": "NEXUS-77X-AUTH",
    "Content-Type": "application/json"
}

print("Initializing Moon 2 Mars Deep Space AI Node...")
print(f"Connecting to M2M Broker at {MIDDLEWARE_URL}")

while True:
    # Simulate a high-load deep space AI node
    simulated_cpu = round(random.uniform(70.0, 99.9), 1)
    simulated_mem = round(random.uniform(60.0, 85.0), 1)
    
    payload = json.dumps({
        "cpu": simulated_cpu,
        "memory": simulated_mem
    }).encode('utf-8')
    
    req = urllib.request.Request(MIDDLEWARE_URL, data=payload, headers=HEADERS, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f"[{time.strftime('%H:%M:%S')}] Transmission Successful: CPU {simulated_cpu}% | MEM {simulated_mem}%")
    except urllib.error.HTTPError as e:
        print(f"Broker rejected transmission: {e.code} - {e.reason}")
    except Exception as e:
        print(f"Deep space connection failed: {e}")
        
    time.sleep(2) # Push data every 2 seconds
