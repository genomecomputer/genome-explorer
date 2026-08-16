from __future__ import annotations

import json
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from urllib.parse import urlsplit

from .core import WorkspaceReport, json_ready, open_bundle, search_workspace
from .web import PAGE


MAX_REQUEST_BYTES = 4096
MAX_QUERY_CHARACTERS = 200
ArchiveChooser = Callable[[], Optional[str]]


class LocalExplorerServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        report: Optional[WorkspaceReport],
        port: int,
        chooser: Optional[ArchiveChooser] = None,
        workspace_root: Optional[Path] = None,
        force_validate: bool = False,
    ):
        super().__init__(("127.0.0.1", port), LocalExplorerHandler)
        self.report = report
        self.chooser = chooser
        self.workspace_root = workspace_root
        self.force_validate = force_validate
        self.state_lock = threading.Lock()
        self.state_status = "ready" if report is not None else "waiting"
        self.state_error = ""
        self.archive_name = Path(report.archive).name if report is not None else ""
        self.token = secrets.token_urlsafe(24)
        self.nonce = secrets.token_urlsafe(18)
        self.expected_host = "127.0.0.1:%d" % self.server_port
        self.origin = "http://%s" % self.expected_host
        self.base_path = "/%s" % self.token

    @property
    def url(self) -> str:
        return self.origin + self.base_path + "/"

    def status_payload(self) -> Dict[str, Any]:
        with self.state_lock:
            status = self.state_status
            error = self.state_error
            archive_name = self.archive_name
            report = self.report

        payload: Dict[str, Any] = {
            "status": status,
            "archive_name": archive_name,
        }
        if error:
            payload["error"] = error
        if status == "ready" and report is not None:
            payload.update(
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
                }
            )
        return payload

    def ready_report(self) -> Optional[WorkspaceReport]:
        with self.state_lock:
            if self.state_status != "ready":
                return None
            return self.report

    def begin_selection(self) -> bool:
        with self.state_lock:
            if self.chooser is None or self.state_status in {"choosing", "validating"}:
                return False
            self.state_status = "choosing"
            self.state_error = ""
            self.archive_name = ""
            self.report = None
        threading.Thread(target=self._select_and_open, daemon=True).start()
        return True

    def _select_and_open(self) -> None:
        try:
            archive = self.chooser() if self.chooser is not None else None
            if archive is None:
                with self.state_lock:
                    self.state_status = "waiting"
                return
            with self.state_lock:
                self.state_status = "validating"
                self.archive_name = Path(archive).name
            if self.workspace_root is None:
                raise RuntimeError("local workspace is unavailable")
            report = open_bundle(
                archive,
                self.workspace_root,
                force_validate=self.force_validate,
            )
            with self.state_lock:
                self.report = report
                self.state_status = "ready"
                self.state_error = ""
        except Exception as error:
            with self.state_lock:
                self.report = None
                self.state_status = "failed"
                self.state_error = str(error)


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
            self._send_json(200, self.server.status_payload())
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
        if path == self.server.base_path + "/api/shutdown":
            self._send_json(200, {"status": "stopped"})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        if path == self.server.base_path + "/api/select":
            started = self.server.begin_selection()
            self._send_json(
                202 if started else 409,
                self.server.status_payload(),
            )
            return
        if path != self.server.base_path + "/api/search":
            self._reject()
            return

        report = self.server.ready_report()
        if report is None:
            self._send_json(409, {"error": "choose and verify a bundle first"})
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
            result = search_workspace(report.workspace, query)
            self._send_json(200, result.to_dict())
        except ValueError as error:
            self._send_json(400, {"error": str(error)})
        except Exception:
            self._send_json(500, {"error": "search could not be completed"})


def _run_server(server: LocalExplorerServer, open_browser: bool) -> None:
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


def serve(report: WorkspaceReport, port: int, open_browser: bool) -> None:
    _run_server(LocalExplorerServer(report, port), open_browser)


def serve_launcher(
    chooser: ArchiveChooser,
    workspace_root: Path,
    force_validate: bool,
    port: int,
    open_browser: bool,
) -> None:
    server = LocalExplorerServer(
        None,
        port,
        chooser=chooser,
        workspace_root=workspace_root,
        force_validate=force_validate,
    )
    _run_server(server, open_browser)
