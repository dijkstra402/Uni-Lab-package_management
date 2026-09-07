"""为设备包选配 UI 提供只读模块目录 API。"""

from __future__ import annotations

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .catalog import ModuleCatalog


def serve_ui(repository_root: Path, host: str, port: int) -> None:
    """启动本地 UI 服务，目录数据始终来自当前仓库。"""

    catalog = ModuleCatalog(repository_root)
    ui_root = Path(__file__).with_name("ui")
    handler = _make_handler(catalog, ui_root)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"设备包选配 UI：http://{host}:{port}")
    print("按 Ctrl+C 停止服务。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止设备包选配 UI。")
    finally:
        server.server_close()


def _make_handler(catalog: ModuleCatalog, ui_root: Path):
    class UIRequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            super().__init__(request, client_address, server, directory=str(ui_root))

        def do_GET(self):
            if urlsplit(self.path).path == "/api/catalog":
                self._send_catalog()
                return
            super().do_GET()

        def _send_catalog(self):
            payload = json.dumps(
                [module.to_dict() for module in catalog.modules],
                ensure_ascii=False,
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format_string, *args):
            return

    return partial(UIRequestHandler)
