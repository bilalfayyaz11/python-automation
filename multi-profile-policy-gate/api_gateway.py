#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
from policy_gate import PolicyGate
from config_manager import ConfigManager


class PolicyGateHandler(BaseHTTPRequestHandler):
    gate = None
    config_mgr = None

    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}

        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8"))

    def do_POST(self):
        if self.path == "/enforce":
            try:
                request_data = self.read_json_body()
                result = self.gate.enforce_policy(request_data)
                self._send_json_response(result, 200)
            except Exception as exc:
                self._send_json_response({"error": str(exc)}, 400)

        elif self.path == "/switch-profile":
            try:
                request_data = self.read_json_body()
                profile_name = request_data.get("profile")

                if not profile_name:
                    self._send_json_response({"success": False, "error": "profile field is required"}, 400)
                    return

                switched = self.gate.switch_profile(profile_name)

                if switched:
                    self.config_mgr.set_active_profile(profile_name)
                    self._send_json_response({
                        "success": True,
                        "message": f"Active profile switched to {profile_name}",
                        "active_profile": profile_name
                    })
                else:
                    self._send_json_response({
                        "success": False,
                        "error": f"Profile '{profile_name}' not found",
                        "available_profiles": self.config_mgr.list_available_profiles()
                    }, 404)

            except Exception as exc:
                self._send_json_response({"success": False, "error": str(exc)}, 400)

        else:
            self._send_json_response({"error": "Not found"}, 404)

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/status":
            self._send_json_response(self.gate.get_active_profile_info())

        elif parsed_path.path == "/profiles":
            self._send_json_response({
                "profiles": self.config_mgr.list_available_profiles(),
                "active_profile": self.config_mgr.get_active_profile()
            })

        elif parsed_path.path == "/health":
            self._send_json_response({"status": "healthy", "service": "multi-profile-policy-gate"})

        else:
            self._send_json_response({"error": "Not found"}, 404)

    def _send_json_response(self, data: dict, status: int = 200):
        payload = json.dumps(data, indent=2).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def run_server(port: int = 8080):
    gate = PolicyGate()
    gate.load_profiles_from_directory("config/profiles")

    config_mgr = ConfigManager("config")

    active_profile = config_mgr.get_active_profile()
    if active_profile and active_profile in gate.profiles:
        gate.switch_profile(active_profile)
    else:
        gate.switch_profile("healthcare")
        config_mgr.set_active_profile("healthcare")

    PolicyGateHandler.gate = gate
    PolicyGateHandler.config_mgr = config_mgr

    server = HTTPServer(("0.0.0.0", port), PolicyGateHandler)

    print(f"Policy Gate API listening on port {port}")
    print(f"Available profiles: {', '.join(config_mgr.list_available_profiles())}")
    print(f"Active profile: {gate.active_profile.name}")

    server.serve_forever()


if __name__ == "__main__":
    run_server()
