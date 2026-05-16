from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import sys
from pathlib import Path

# Add project root and liens dir to path
ROOT_DIR = Path(__file__).parent.parent
LIENS_DIR = Path(r"C:\liens")
sys.path.append(str(ROOT_DIR))
sys.path.append(str(LIENS_DIR))

try:
    import liens_data
    import gemini_cli
    from network_tools_engine import nt_engine
except ImportError as e:
    print(f"Import Error: {e}")

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/market')
def market_data():
    if 'liens_data' in globals():
        return jsonify(liens_data.get_overview_bundle())
    return jsonify({"error": "liens_data not available"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    api_key = data.get('api_key', os.environ.get("GEMINI_API_KEY", ""))
    
    if not api_key:
        return jsonify({"error": "No API key provided"}), 400
        
    if 'gemini_cli' in globals():
        response = gemini_cli.ask_gemini(api_key, message)
        return jsonify({"response": response})
    
    return jsonify({"error": "gemini_cli not available"}), 500

@app.route('/api/ports/fragment')
def ports_fragment():
    critical_ports = [3000, 3001, 3002, 5000, 6000, 7000, 8000, 9000]
    results = nt_engine.scanner.scan_ports('127.0.0.1', critical_ports)
    
    html = '<div class="port-grid">'
    for res in results:
        status_class = "tag-low" if res['status'] == 'open' else "tag-high"
        html += f"""
            <div class="port-item">
                <span class="port-number">PORT {res['port']}</span>
                <span class="tag {status_class}">{res['status'].upper()}</span>
                <span class="port-service">{res['service']}</span>
            </div>
        """
    html += '</div>'
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting NetworkBuster Backend on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
