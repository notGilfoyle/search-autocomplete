from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

from trie import Trie
from search_data import SEARCH_TERMS


autocomplete_trie = Trie()
autocomplete_cache = {}

for term, frequency in SEARCH_TERMS:
    autocomplete_trie.insert(term, frequency)


class AutocompleteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/autocomplete":
            query_params = parse_qs(parsed_url.query)
            prefix = query_params.get("prefix", [""])[0]

            debug = query_params.get("debug", ["false"])[0] == "true"
            cache_key = f"{prefix}:debug={debug}"

            if cache_key in autocomplete_cache:
                suggestions = autocomplete_cache[cache_key]
                cache_hit = True
            else:
                suggestions = autocomplete_trie.autocomplete(
                    prefix,
                    include_frequencies=debug
                )
                autocomplete_cache[cache_key] = suggestions
                cache_hit = False

            response = {
                "prefix": prefix,
                "suggestions": suggestions,
                "cache_hit": cache_hit
            }

            self.send_json_response(response)
            return

        self.send_error(404, "Not Found")

    def send_json_response(self, data):
        response_body = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_cors_headers()
        self.send_header("Content-Length", len(response_body))
        self.end_headers()
        self.wfile.write(response_body)

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_POST(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/record-search":
            content_length = int(self.headers.get("Content-Length", 0))
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body)

            term = data.get("term", "").strip()
            was_updated = autocomplete_trie.increment_frequency(term)
            if was_updated:
                autocomplete_cache.clear()

            response = {
                "term": term,
                "updated": was_updated
            }

            self.send_json_response(response)
            return

        self.send_error(404, "Not Found")


    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()


def run_server():
    server_address = ("localhost", 8000)
    server = HTTPServer(server_address, AutocompleteHandler)

    print("Backend running at http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    run_server()