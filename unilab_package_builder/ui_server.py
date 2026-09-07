"""为设备包选配 UI 提供目录和工程生成下载 API。"""

from __future__ import annotations

import json
import tarfile
import tempfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .acceptance import AcceptanceScaffoldError, generate_acceptance_bundle
from .catalog import CatalogError, ModuleCatalog
from .config import ConfigError, ProjectConfig, project_config_from_dict
from .scaffold import ScaffoldError, generate_project

MAX_CONFIG_BYTES = 1024 * 1024


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

        def do_POST(self):
            route = urlsplit(self.path).path
            generators = {
                "/api/generate/device-package": (
                    generate_project,
                    "device-package",
                ),
                "/api/generate/acceptance-bundle": (
                    generate_acceptance_bundle,
                    "acceptance-bundle",
                ),
            }
            generator_spec = generators.get(route)
            if generator_spec is None:
                self.send_error(404)
                return
            try:
                config = self._read_config()
                payload, filename = _build_archive(
                    config,
                    catalog,
                    generator_spec[0],
                    generator_spec[1],
                )
            except (
                AcceptanceScaffoldError,
                CatalogError,
                ConfigError,
                ScaffoldError,
                OSError,
                ValueError,
            ) as error:
                self._send_error(str(error))
                return
            self._send_archive(payload, filename)

        def _read_config(self) -> ProjectConfig:
            content_length = self.headers.get("Content-Length")
            if content_length is None:
                raise ConfigError("请求缺少 Content-Length")
            try:
                length = int(content_length)
            except ValueError as error:
                raise ConfigError("Content-Length 无效") from error
            if length < 1 or length > MAX_CONFIG_BYTES:
                raise ConfigError("配置请求大小必须在 1B 至 1MiB 之间")
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ConfigError(f"请求不是合法 JSON: {error}") from error
            return project_config_from_dict(payload)

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

        def _send_error(self, message: str) -> None:
            payload = json.dumps(
                {"error": message}, ensure_ascii=False
            ).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def _send_archive(self, payload: bytes, filename: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "application/gzip")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format_string, *args):
            return

    return partial(UIRequestHandler)


def _build_archive(
    config: ProjectConfig,
    catalog: ModuleCatalog,
    generator,
    artifact_kind: str,
) -> tuple[bytes, str]:
    """在临时目录生成工程并返回不落盘的 tar.gz 内容。"""

    with tempfile.TemporaryDirectory(prefix="unilab-package-builder-") as directory:
        project_root = Path(directory) / "project"
        generator(config, catalog, project_root)
        filename = f"{config.distribution_name}-{artifact_kind}.tar.gz"
        archive_path = Path(directory) / filename
        with tarfile.open(archive_path, mode="w:gz") as archive:
            archive.add(
                project_root,
                arcname=config.distribution_name,
                recursive=True,
            )
        return archive_path.read_bytes(), filename
