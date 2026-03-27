import http.server
import socketserver
import json
import os
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가 (한국어 경로 등 인코딩 이슈 해결)
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

PORT = 8080
LOG_FILE = "governance_audit.log"
TEMPLATE_DIR = Path("templates")

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'templates/index.html'
            return super().do_GET()
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            stats = self._get_stats()
            self.wfile.write(json.dumps(stats).encode())
        else:
            return super().do_GET()

    def _get_stats(self):
        if not os.path.exists(LOG_FILE):
            return {"total": 0, "work": 0, "personal": 0, "security": 0, "recent": []}
        
        work_count = 0
        personal_count = 0
        security_count = 0
        recent_logs = []
        
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    # 로그 형식: 2026-03-27 07:31:21,123 - {"type": "asset_metadata", ...}
                    parts = line.split(" - ", 1)
                    if len(parts) < 2: continue
                    
                    data = json.loads(parts[1])
                    if data.get("category") == "Work":
                        work_count += 1
                    elif data.get("category") == "Personal":
                        personal_count += 1
                    elif data.get("category") == "Security_Alert_Samples":
                        security_count += 1
                    
                    recent_logs.append(data)
                except:
                    continue
        
        return {
            "total": work_count + personal_count + security_count,
            "work": work_count,
            "personal": personal_count,
            "security": security_count,
            "recent": recent_logs[-10:] # 최근 10개만
        }

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Dashboard serving at http://localhost:{PORT}")
        httpd.serve_forever()
