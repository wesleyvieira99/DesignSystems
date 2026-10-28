"""Adaptador HTTP de laboratório. http.server não é servidor de produção."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from controller import Response, TaskController
from model import TaskStore
from views import json_response

class Server(ThreadingHTTPServer):
    def __init__(self, address, controller):
        self.controller = controller
        super().__init__(address, Handler)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond(self.server.controller.handle("GET", urlsplit(self.path).path))

    def do_POST(self):
        try:
            if self.headers.get("Transfer-Encoding"):
                self.respond(Response(400, json_response({"error": "Use Content-Length."})))
                return
            size = int(self.headers.get("Content-Length", "0"))
            if size < 0 or size > 4096:
                self.respond(Response(413, json_response({"error": "Payload acima do limite."})))
                return
            raw = self.rfile.read(size).decode("utf-8")
            media_type = self.headers.get("Content-Type", "").split(";", 1)[0]
            if media_type == "application/json":
                data = json.loads(raw)
                if not isinstance(data, dict):
                    raise ValueError("JSON deve ser um objeto.")
            elif media_type == "application/x-www-form-urlencoded":
                values = parse_qs(raw, keep_blank_values=True)
                data = {key: value[0] for key, value in values.items()}
            else:
                self.respond(Response(415, json_response({"error": "Content-Type não aceito."})))
                return
        except (ValueError, UnicodeError):
            self.respond(Response(400, json_response({"error": "Corpo inválido."})))
            return
        self.respond(self.server.controller.handle("POST", urlsplit(self.path).path, data))

    def respond(self, response):
        self.send_response(response.status)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(response.body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.body)

def make_server(database: str, port: int = 8080) -> Server:
    return Server(("127.0.0.1", port), TaskController(TaskStore(database)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MVC local · System Atlas")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--database", default=str(Path(__file__).with_name("tasks.sqlite3")))
    args = parser.parse_args()
    with make_server(args.database, args.port) as server:
        print(f"MVC disponível em http://127.0.0.1:{server.server_port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
