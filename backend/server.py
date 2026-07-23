from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


class AutocompleteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/autocomplete":
            query_params = parse_qs(parsed_url.query)
            prefix = query_params.get("prefix", [""])[0]

            response = {
                "prefix": prefix,
                "suggestions": []
            }

            self.send_json_response(response)
            return

        self.send_error(404, "Not Found")

    def send_json_response(self, data):
        response_body = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(response_body))
        self.end_headers()
        self.wfile.write(response_body)


def run_server():
    server_address = ("localhost", 8000)
    server = HTTPServer(server_address, AutocompleteHandler)

    print("Backend running at http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    run_server()