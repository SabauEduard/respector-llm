#!/usr/bin/env python3
"""
Simple HTTP server to view Swagger UI documentation
Alternative to Docker for quick viewing
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT_BEFORE = 8081
PORT_AFTER = 8082

def create_html(json_path: str) -> str:
    """Create HTML page that loads Swagger UI with the given spec."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui.css">
    <style>
        body {{ margin: 0; padding: 0; }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            fetch('{json_path}')
                .then(response => response.json())
                .then(spec => {{
                    SwaggerUIBundle({{
                        spec: spec,
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        plugins: [
                            SwaggerUIBundle.plugins.DownloadUrl
                        ],
                        layout: "StandaloneLayout"
                    }});
                }});
        }};
    </script>
</body>
</html>
"""

def main():
    print("🚀 Starting Swagger UI viewers...")
    print("")
    
    # Create temporary HTML files
    base_dir = Path(__file__).parent
    
    # BEFORE viewer
    before_html = base_dir / "temp_before.html"
    before_html.write_text(create_html("/order-api.json"))
    
    # AFTER viewer  
    after_html = base_dir / "temp_after.html"
    after_html.write_text(create_html("/order-api.json"))
    
    print("📄 BEFORE (Raw Respector):  http://localhost:8081/temp_before.html")
    print("✨ AFTER (Enhanced):        http://localhost:8082/temp_after.html")
    print("")
    print("Press Ctrl+C to stop")
    print("")
    
    # Open browsers
    webbrowser.open(f"http://localhost:{PORT_BEFORE}/temp_before.html")
    webbrowser.open(f"http://localhost:{PORT_AFTER}/temp_after.html")
    
    # Start simple HTTP server
    os.chdir(base_dir)
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT_BEFORE), handler) as httpd:
        print(f"Serving on port {PORT_BEFORE}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Stopping server...")
            before_html.unlink(missing_ok=True)
            after_html.unlink(missing_ok=True)

if __name__ == "__main__":
    main()

