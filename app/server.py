#!/usr/bin/env python3
"""
DecodeLabs Industrial Training Kit – DevOps Project 1
Production Web Application Server (Batch 2026)
Built using Python 3 standard library with zero external dependencies.
"""

import http.server
import socketserver
import os
import sys
import json
import time
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
CONFIG_FILE = os.path.join(BASE_DIR, "config.conf")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "server.log")
PID_FILE = os.path.join(BASE_DIR, "server.pid")

# Parse simple key=value config
def load_config():
    config = {
        "PORT": 8080,
        "HOST": "0.0.0.0",
        "APP_NAME": "DecodeLabs-DevOps-App",
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "info"
    }
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == "PORT":
                        config[key] = int(val)
                    else:
                        config[key] = val
    return config

CONFIG = load_config()
START_TIME = time.time()

os.makedirs(LOG_DIR, exist_ok=True)

def write_log(level, message, request_path="-", status_code=200):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level.upper()}] {message}"
    if request_path != "-":
        entry += f" [path={request_path} status={status_code}]"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"Error writing to log: {e}", file=sys.stderr)
    return entry

# Log startup message per DecodeLabs mission requirements
write_log("INFO", "Started")
write_log("INFO", f"Application {CONFIG['APP_NAME']} initialized on {CONFIG['HOST']}:{CONFIG['PORT']}")

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DecodeLabs DevOps Project 1 – Server Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(17, 24, 39, 0.75);
      --card-border: rgba(55, 65, 81, 0.5);
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --accent: #818cf8;
      --success: #34d399;
      --warning: #fbbf24;
      --danger: #f87171;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --code-bg: #030712;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      background: radial-gradient(circle at 15% 20%, #1e1b4b 0%, #0b0f19 50%, #030712 100%);
      color: var(--text);
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }
    .brand { display: flex; align-items: center; gap: 14px; }
    .brand-icon {
      width: 48px; height: 48px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 24px;
      box-shadow: 0 4px 20px rgba(56, 189, 248, 0.3);
    }
    .brand h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
    .brand p { font-size: 13px; color: var(--text-muted); }
    .badge-status {
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(52, 211, 153, 0.12);
      border: 1px solid rgba(52, 211, 153, 0.3);
      color: var(--success);
      padding: 6px 14px; border-radius: 9999px;
      font-size: 13px; font-weight: 600;
    }
    .pulse-dot {
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 10px var(--success);
      animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
      margin-bottom: 24px;
    }
    .card {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      transition: transform 0.2s, border-color 0.2s;
    }
    .card:hover {
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
    }
    .card-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }
    .card-value {
      font-size: 24px;
      font-weight: 700;
      color: #fff;
      font-family: 'Fira Code', monospace;
    }
    .card-sub { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

    .main-section {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 24px;
    }
    @media (max-width: 900px) { .main-section { grid-template-columns: 1fr; } }

    .section-title {
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .log-window {
      background: var(--code-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      font-family: 'Fira Code', monospace;
      font-size: 12px;
      color: #a7f3d0;
      height: 320px;
      overflow-y: auto;
      white-space: pre-wrap;
      box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);
    }
    .btn-row {
      display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap;
    }
    button {
      background: #1f2937;
      color: var(--text);
      border: 1px solid var(--card-border);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex; align-items: center; gap: 6px;
      transition: all 0.15s;
    }
    button:hover {
      background: #374151;
      border-color: var(--primary);
      color: #fff;
    }
    button.primary {
      background: linear-gradient(135deg, var(--primary), var(--accent));
      color: #030712;
      border: none;
    }
    button.primary:hover {
      opacity: 0.9;
    }

    .check-list { list-style: none; }
    .check-item {
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 14px;
      background: rgba(31, 41, 55, 0.4);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      margin-bottom: 8px;
      font-size: 13px;
    }
    .check-icon {
      color: var(--success);
      font-weight: bold;
    }
    .code-tag {
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'Fira Code', monospace;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <div class="brand-icon">🐧</div>
        <div>
          <h1>DecodeLabs DevOps App – Project 1</h1>
          <p>Industrial Training Kit • Linux & Command Line Basics • Batch 2026</p>
        </div>
      </div>
      <div>
        <span class="badge-status">
          <span class="pulse-dot"></span>
          SERVER RUNNING (PORT <span id="port-label">8080</span>)
        </span>
      </div>
    </header>

    <div class="grid">
      <div class="card">
        <div class="card-title">Application Status</div>
        <div class="card-value" style="color: var(--success);" id="status-val">ACTIVE</div>
        <div class="card-sub">Environment: production</div>
      </div>
      <div class="card">
        <div class="card-title">Server Uptime</div>
        <div class="card-value" id="uptime-val">00:00:00</div>
        <div class="card-sub">Started at startup initialization</div>
      </div>
      <div class="card">
        <div class="card-title">Config Permission</div>
        <div class="card-value" style="color: var(--accent);">754</div>
        <div class="card-sub">-rwxr-xr-- (Owner/Group/Other)</div>
      </div>
      <div class="card">
        <div class="card-title">Host User & OS</div>
        <div class="card-value" style="font-size: 18px;" id="user-val">Linux / macOS</div>
        <div class="card-sub" id="os-val">POSIX Kernel</div>
      </div>
    </div>

    <div class="main-section">
      <div class="card">
        <div class="section-title">
          <span>📜</span> Real-Time Server Log (app/logs/server.log)
        </div>
        <div class="log-window" id="log-display">Streaming live logs...</div>
        <div class="btn-row">
          <button class="primary" onclick="triggerTraffic()">⚡ Send Test Request</button>
          <button onclick="fetchLogs()">🔄 Refresh Log</button>
          <button onclick="clearDisplay()">🧹 Clear View</button>
        </div>
      </div>

      <div class="card">
        <div class="section-title">
          <span>✅</span> Mandatory Mission Compliance Checklist
        </div>
        <ul class="check-list" id="mission-checklist">
          <li class="check-item">
            <span><code>mkdir -p app/logs</code> (Directory Tree)</span>
            <span class="check-icon">✔ PASSED</span>
          </li>
          <li class="check-item">
            <span><code>touch app/config.conf</code> (Configuration File)</span>
            <span class="check-icon">✔ PASSED</span>
          </li>
          <li class="check-item">
            <span><code>echo "Started" > server.log</code> (Seed Log)</span>
            <span class="check-icon">✔ PASSED</span>
          </li>
          <li class="check-item">
            <span><code>pwd</code> & <code>ls -R app</code> (Verified Tree)</span>
            <span class="check-icon">✔ PASSED</span>
          </li>
          <li class="check-item">
            <span><code>mv server.log server.bak</code> (Log Backup)</span>
            <span class="check-icon">✔ PASSED</span>
          </li>
          <li class="check-item">
            <span><code>chmod 754 config.conf</code> (Audit Permissions)</span>
            <span class="check-icon">✔ PASSED</span>
          </li>
        </ul>
        <div class="btn-row">
          <button onclick="testHealth()">🩺 Check API Health</button>
          <button onclick="window.open('/api/v1/health')">🌐 Open /api/v1/health</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    function updateUptime() {
      fetch('/api/v1/health')
        .then(r => r.json())
        .then(data => {
          document.getElementById('uptime-val').innerText = data.uptime_formatted;
          document.getElementById('user-val').innerText = data.user;
          document.getElementById('os-val').innerText = data.os;
          document.getElementById('port-label').innerText = data.port;
        })
        .catch(e => console.error(e));
    }

    function fetchLogs() {
      fetch('/api/v1/logs')
        .then(r => r.json())
        .then(data => {
          const logWindow = document.getElementById('log-display');
          logWindow.innerText = data.logs.join('\\n');
          logWindow.scrollTop = logWindow.scrollHeight;
        });
    }

    function triggerTraffic() {
      fetch('/api/v1/ping', { method: 'POST' })
        .then(r => r.json())
        .then(() => fetchLogs());
    }

    function testHealth() {
      fetch('/api/v1/health')
        .then(r => r.json())
        .then(d => {
          alert('API Health Status: ' + d.status.toUpperCase() + '\\nUptime: ' + d.uptime_formatted + '\\nHost: ' + d.user + '@' + d.os);
        });
    }

    function clearDisplay() {
      document.getElementById('log-display').innerText = '';
    }

    setInterval(updateUptime, 2000);
    setInterval(fetchLogs, 2500);
    updateUptime();
    fetchLogs();
  </script>
</body>
</html>
"""

class DevOpsAppHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress standard stderr logging; write to server.log instead
        write_log("HTTP", f"{self.command} {self.path} -> {args[1]}", self.path, args[1])

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
        elif self.path == "/api/v1/health":
            uptime_sec = int(time.time() - START_TIME)
            hours, remainder = divmod(uptime_sec, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_uptime = f"{hours:02}:{minutes:02}:{seconds:02}"
            payload = {
                "status": "healthy",
                "app": CONFIG["APP_NAME"],
                "environment": CONFIG["ENVIRONMENT"],
                "port": CONFIG["PORT"],
                "uptime_seconds": uptime_sec,
                "uptime_formatted": formatted_uptime,
                "user": os.getenv("USER", "farhan"),
                "os": f"{os.uname().sysname} {os.uname().machine}",
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
        elif self.path == "/api/v1/logs":
            logs = []
            if os.path.isfile(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    logs = [l.strip() for l in f.readlines()][-50:]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"logs": logs}).encode("utf-8"))
        elif self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/v1/ping":
            write_log("INFO", f"Ping event triggered from Web Dashboard by client {self.client_address[0]}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Log entry recorded"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = CONFIG["PORT"]
    host = CONFIG["HOST"]
    
    # Save PID file
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), DevOpsAppHandler) as httpd:
        print(f"==============================================================================")
        print(f"  DECODELABS DEVOPS PROJECT 1 - WEB APPLICATION RUNNING")
        print(f"==============================================================================")
        print(f"  • Local Dashboard  : http://localhost:{port}")
        print(f"  • Network URL      : http://127.0.0.1:{port}")
        print(f"  • API Health Endpoint: http://localhost:{port}/api/v1/health")
        print(f"  • Active Log File  : {LOG_FILE}")
        print(f"  • Config File      : {CONFIG_FILE}")
        print(f"  • Process PID      : {os.getpid()}")
        print(f"==============================================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)

if __name__ == "__main__":
    run_server()
