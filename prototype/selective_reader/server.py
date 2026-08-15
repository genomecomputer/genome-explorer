from __future__ import annotations

import json
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict
from urllib.parse import urlsplit

from .core import WorkspaceReport, json_ready, search_workspace
from .web import PAGE


MAX_REQUEST_BYTES = 4096
MAX_QUERY_CHARACTERS = 200


class LocalExplorerServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, report: WorkspaceReport, port: int):
        super().__init__(("127.0.0.1", port), LocalExplorerHandler)
        self.report = report
        self.token = secrets.token_urlsafe(24)
        self.nonce = secrets.token_urlsafe(18)
        self.expected_host = "127.0.0.1:%d" % self.server_port
        self.origin = "http://%s" % self.expected_host
        self.base_path = "/%s" % self.token

    @property
    def url(self) -> str:
        return self.origin + self.base_path + "/"


class LocalExplorerHandler(BaseHTTPRequestHandler):
    server: LocalExplorerServer

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _request_is_local(self) -> bool:
        return self.headers.get("Host") == self.server.expected_host

    def _send_headers(self, status: int, content_type: str, length: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; "
            "script-src 'nonce-%s'; style-src 'nonce-%s'; "
            "connect-src 'self'; img-src data:; "
            "base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
            % (self.server.nonce, self.server.nonce),
        )
        self.end_headers()

    def _send_bytes(self, status: int, content_type: str, body: bytes) -> None:
        self._send_headers(status, content_type, len(body))
        self.wfile.write(body)

    def _send_json(self, status: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(json_ready(payload), separators=(",", ":")).encode("utf-8")
        self._send_bytes(status, "application/json; charset=utf-8", body)

    def _reject(self, status: int = 404) -> None:
        self._send_json(status, {"error": "not found"})

    def do_GET(self) -> None:
        if not self._request_is_local():
            self._reject(403)
            return
        path = urlsplit(self.path).path.rstrip("/")
        if path == self.server.base_path:
            page = (
                PAGE.replace("__BASE_PATH__", self.server.base_path)
                .replace("__NONCE__", self.server.nonce)
                .encode("utf-8")
            )
            self._send_bytes(200, "text/html; charset=utf-8", page)
            return
        if path == self.server.base_path + "/api/status":
            report = self.server.report
            self._send_json(
                200,
                {
                    "schema_version": report.schema_version,
                    "genome_build": report.genome_build,
                    "generated_at": report.generated_at,
                    "validated_entries": report.validated_entries,
                    "stored_files": report.extracted_files,
                    "stored_bytes": report.extracted_bytes,
                    "validation_seconds": report.elapsed_seconds,
                    "validation_mode": report.validation_mode,
                    "validated_at": report.validated_at,
                },
            )
            return
        self._reject()

    def do_POST(self) -> None:
        if not self._request_is_local():
            self._reject(403)
            return
        if self.headers.get("Origin") != self.server.origin:
            self._reject(403)
            return
        path = urlsplit(self.path).path.rstrip("/")
        if path != self.server.base_path + "/api/search":
            self._reject()
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "invalid request length"})
            return
        if content_length < 1 or content_length > MAX_REQUEST_BYTES:
            self._send_json(400, {"error": "invalid request length"})
            return
        try:
            payload = json.loads(self.rfile.read(content_length))
            query = payload.get("query", "")
            if not isinstance(query, str) or len(query) > MAX_QUERY_CHARACTERS:
                raise ValueError("search query is invalid")
            result = search_workspace(self.server.report.workspace, query)
            self._send_json(200, result.to_dict())
        except ValueError as error:
            self._send_json(400, {"error": str(error)})
        except Exception:
            self._send_json(500, {"error": "search could not be completed"})


def serve(report: WorkspaceReport, port: int, open_browser: bool) -> None:
    server = LocalExplorerServer(report, port)
    print("Genome Explorer ready: %s" % server.url, flush=True)
    print("Press Ctrl-C to stop.", flush=True)
    if open_browser:
        threading.Timer(0.2, webbrowser.open, args=(server.url,)).start()
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            server.server_close()
        except KeyboardInterrupt:
            pass
