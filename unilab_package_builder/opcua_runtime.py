"""生成设备包使用的轻量 OPC UA 运行时。"""

from __future__ import annotations

import csv
import time
from collections import deque
from pathlib import Path
from typing import Any, Mapping

from opcua import Client
from unilabos.device_comms.universal_driver import UniversalDriver
from unilabos.utils.log import logger


class OpcUaDeviceClient(UniversalDriver):
    """按标准协议点表连接、查找、读取和写入 OPC UA 变量。"""

    def __init__(
        self,
        *,
        url: str,
        protocol_path: str,
        username: str | None = None,
        password: str | None = None,
        node_id_map: Mapping[str, str] | None = None,
        node_id_prefix: str | None = None,
        browse_root: str | None = None,
        request_timeout: float = 10.0,
        wait_timeout: float = 30.0,
        poll_interval: float = 0.2,
        auto_connect: bool = True,
        **kwargs: Any,
    ) -> None:
        del kwargs
        if not url.strip():
            raise ValueError("OPC UA url 不能为空")
        super().__init__()
        self.url = url
        self.protocol_path = str(Path(protocol_path).resolve())
        self.node_id_map = {
            str(name).strip(): str(node_id).strip()
            for name, node_id in (node_id_map or {}).items()
            if str(name).strip() and str(node_id).strip()
        }
        self.node_id_prefix = node_id_prefix or ""
        self.browse_root = browse_root
        self.wait_timeout = max(float(wait_timeout), 0.0)
        self.poll_interval = max(float(poll_interval), 0.0)
        self._protocol = self._load_protocol(self.protocol_path)
        self._nodes: dict[str, Any] = {}
        self._connected = False
        self.client = Client(url, timeout=float(request_timeout))
        if username and password:
            self.client.set_user(username)
            self.client.set_password(password)
        if auto_connect:
            self.connect()

    @staticmethod
    def _load_protocol(path: str) -> tuple[dict[str, str], ...]:
        rows: list[dict[str, str]] = []
        seen: dict[str, tuple[str, str]] = {}
        with open(path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required = {"name", "node_type", "data_type"}
            if not required <= set(reader.fieldnames or ()):
                raise ValueError(f"OPC UA 协议表列不完整: {path}")
            for row in reader:
                name = (row.get("name") or "").strip()
                node_type = (row.get("node_type") or "").strip().upper()
                data_type = (row.get("data_type") or "").strip()
                if not name:
                    continue
                signature = (node_type, data_type)
                if name in seen and seen[name] != signature:
                    raise ValueError(f"OPC UA 节点类型冲突: {name}")
                if name in seen:
                    continue
                if node_type != "VARIABLE":
                    raise ValueError(f"暂不支持的 OPC UA 节点类型: {node_type}")
                seen[name] = signature
                rows.append(
                    {
                        "name": name,
                        "node_type": node_type,
                        "data_type": data_type,
                        "node_id": (row.get("node_id") or "").strip(),
                    }
                )
        if not rows:
            raise ValueError(f"OPC UA 协议表为空: {path}")
        return tuple(rows)

    def connect(self) -> None:
        if self._connected:
            return
        try:
            self.client.connect()
            self._nodes = {
                row["name"]: self._resolve_node(row["name"], row["node_id"])
                for row in self._protocol
            }
            self._connected = True
            logger.info(f"OPC UA 已连接并注册 {len(self._nodes)} 个标准节点")
        except Exception:
            self._connected = False
            try:
                self.client.disconnect()
            except Exception:
                pass
            raise

    def disconnect(self) -> None:
        if not self._connected:
            return
        try:
            self.client.disconnect()
        finally:
            self._connected = False
            self._nodes = {}

    close = disconnect

    @property
    def connected(self) -> bool:
        return self._connected

    def reconnect(self) -> None:
        self.disconnect()
        self.connect()

    def _resolve_node(self, name: str, csv_node_id: str) -> Any:
        node_id = self.node_id_map.get(name) or csv_node_id
        if node_id:
            return self.client.get_node(node_id)
        if self.node_id_prefix:
            return self.client.get_node(f"{self.node_id_prefix}{name}")
        return self._find_by_browse_name(name)

    def _find_by_browse_name(self, name: str) -> Any:
        root = self.client.get_node(self.browse_root) if self.browse_root else self.client.get_objects_node()
        queue = deque([root])
        visited: set[str] = set()
        matches: list[Any] = []
        while queue:
            node = queue.popleft()
            node_key = str(node.nodeid)
            if node_key in visited:
                continue
            visited.add(node_key)
            browse_name = node.get_browse_name().Name
            if browse_name == name:
                matches.append(node)
            for child in node.get_children():
                if str(child.nodeid) not in visited:
                    queue.append(child)
            if len(visited) > 10000:
                raise RuntimeError(f"浏览 OPC UA 节点超过上限，无法定位: {name}")
        if not matches:
            raise LookupError(
                f"未找到 OPC UA BrowseName: {name}；请传入 node_id_map 或 node_id_prefix"
            )
        if len(matches) > 1:
            node_ids = ", ".join(str(node.nodeid) for node in matches[:5])
            raise LookupError(f"OPC UA BrowseName 不唯一: {name} ({node_ids})")
        return matches[0]

    def _node(self, name: str) -> Any:
        if not self._connected:
            raise ConnectionError("OPC UA 尚未连接")
        try:
            return self._nodes[name]
        except KeyError as error:
            raise KeyError(f"标准协议未定义 OPC UA 节点: {name}") from error

    def get_node_value(self, name: str) -> Any:
        return self._run_io(lambda: self._node(name).get_value())

    def read_node(self, name: str) -> Any:
        return self.get_node_value(name)

    def set_node_value(self, name: str, value: Any) -> bool:
        self._run_io(
            lambda: self._node(name).set_value(
                value,
                self._node(name).get_data_type_as_variant_type(),
            )
        )
        return True

    def write_node(self, name: str, value: Any) -> bool:
        return self.set_node_value(name, value)

    def wait_until(self, name: str, expected: Any, *, timeout: float | None = None) -> bool:
        limit = self.wait_timeout if timeout is None else max(float(timeout), 0.0)
        started_at = time.monotonic()
        while True:
            if self.get_node_value(name) == expected:
                return True
            if time.monotonic() - started_at >= limit:
                return False
            time.sleep(self.poll_interval)

    def wait_until_true(self, name: str, *, timeout: float | None = None) -> bool:
        return self.wait_until(name, True, timeout=timeout)

    def wait_until_false(self, name: str, *, timeout: float | None = None) -> bool:
        return self.wait_until(name, False, timeout=timeout)

    def _run_io(self, operation):
        try:
            return operation()
        except Exception as error:
            logger.warning(f"OPC UA I/O 失败，尝试重连: {type(error).__name__}: {error}")
            self.reconnect()
            return operation()
