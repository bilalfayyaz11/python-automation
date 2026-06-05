#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class AlertHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(content_length)

        try:

            alert_data = json.loads(body.decode())

            print("\n===== ALERT RECEIVED =====")
            print(json.dumps(alert_data, indent=2))

        except Exception as error:

            print(f"Failed to parse alert: {error}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


if __name__ == "__main__":

    server = HTTPServer(
        ("localhost", 8080),
        AlertHandler
    )

    print("Alert webhook listening on port 8080...")
    server.serve_forever()
