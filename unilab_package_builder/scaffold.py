"""生成遵循 Uni-Lab-OS 外部设备包契约的项目脚手架。"""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

from .catalog import ModuleCatalog, ModuleSpec
from .config import ProjectConfig


class ScaffoldError(ValueError):
    """设备包脚手架无法生成。"""


def generate_project(
    config: ProjectConfig,
    catalog: ModuleCatalog,
    output_root: Path,
    *,
    force: bool = False,
) -> tuple[Path, ...]:
    """根据选择配置生成一个可安装设备包，并返回写入文件。"""

    config.validate()
    selected = catalog.select(config.modules)
    output_root = Path(output_root).resolve()
    if output_root.exists() and any(output_root.iterdir()) and not force:
        raise ScaffoldError(f"输出目录非空，使用 --force 覆盖生成文件: {output_root}")

    package_root = output_root / config.package_name
    devices_root = package_root / "devices"
    files: dict[Path, str] = {
        output_root / "pyproject.toml": _render_pyproject(config),
        output_root / "package.yaml": _render_package_manifest(config),
        output_root / "README.md": _render_readme(config, selected),
        package_root / "__init__.py": _render_package_init(selected),
        devices_root / "__init__.py": _render_devices_init(selected),
        output_root / "device_selection.json": _render_selection(config, selected),
    }
    if config.driver_mode == "opcua":
        files[package_root / "opcua.py"] = _render_opcua_runtime()
    for module in selected:
        source = catalog.repository_root / module.source_path
        if config.driver_mode == "opcua":
            files[devices_root / f"{module.device_id}.py"] = _render_opcua_device_source(
                config, module
            )
            files[package_root / "protocols" / f"{module.device_id}.csv"] = (
                _render_protocol_csv(module)
            )
        else:
            files[devices_root / f"{module.device_id}.py"] = _render_device_source(source)
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tuple(files)


def _render_pyproject(config: ProjectConfig) -> str:
    distribution_name = json.dumps(config.distribution_name, ensure_ascii=False)
    description = json.dumps(config.description, ensure_ascii=False)
    package_include = json.dumps(f"{config.package_name}*", ensure_ascii=False)
    dependencies = '["unilabos>=0.11.3"'
    if config.driver_mode == "opcua":
        dependencies += ', "opcua>=0.98.13"'
    dependencies += "]"
    package_data = ""
    if config.driver_mode == "opcua":
        package_data = (
            "\n[tool.setuptools.package-data]\n"
            f"{json.dumps(config.package_name)} = [\"protocols/*.csv\"]\n"
        )
    return f'''[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = {distribution_name}
version = "{config.version}"
description = {description}
readme = "README.md"
requires-python = ">=3.11"
dependencies = {dependencies}

[project.optional-dependencies]
dev = ["pytest>=8,<9", "ruff>=0.6"]

[tool.setuptools.packages.find]
include = [{package_include}]
{package_data}

[tool.pytest.ini_options]
testpaths = ["tests"]
'''


def _render_package_manifest(config: ProjectConfig) -> str:
    return f'''package:
  name: {config.package_name}
workflows: []
'''


def _render_readme(config: ProjectConfig, selected: tuple[ModuleSpec, ...]) -> str:
    module_lines = "\n".join(
        f"- `{module.device_id}`：{' > '.join(module.category_path)}" for module in selected
    )
    if config.driver_mode == "opcua":
        implementation = f'''设备模块已按 `device_templates_actions.csv` 生成 OPC UA 实际驱动。
每个设备包含标准 BrowseName 协议表 `{config.package_name}/protocols/<device_id>.csv`，运行时位于
`{config.package_name}/opcua.py`。驱动连接时依次支持协议表中的 NodeId、构造参数中的
`node_id_map`、`node_id_prefix`，以及从 `Objects` 节点按 BrowseName 查找。

连接示例：

```python
from {config.package_name}.devices.{selected[0].device_id} import { _class_name(selected[0].device_id) }

device = {_class_name(selected[0].device_id)}(
    url="opc.tcp://127.0.0.1:4840",
    node_id_map={{"设备运行状态": "ns=2;s=Device.Status"}},
)
```

具体 PLC 的 Namespace、NodeId 或 BrowseName 根路径需要根据设备点表传入；协议表提供标准逻辑节点名和数据类型。
'''
    else:
        implementation = '''设备动作和状态接口来自选中的标准模块；未实现的动作会明确抛出
`NotImplementedError`，不会伪造成功结果。
'''
    return f'''# {config.description}

这是由 `unilab-package-builder` 根据设备模块选择配置生成的 Uni-Lab-OS 外部设备包。
{implementation}

## 已选择模块

{module_lines}

## 开发与校验

```bash
python -m pip install -e '.[dev]'
unilab --check_mode --devices ./{config.package_name} --external_devices_only
unilab package inspect --path . --out ./artifacts
unilab package build --path . --out ./artifacts
```

设备配置、资源和工作流继续放在本设备包内；真实驱动模式下，具体设备的物理 NodeId、Namespace
和安全配置通过构造参数或部署配置注入，不写死到标准模板。
'''


def _render_selection(config: ProjectConfig, selected: tuple[ModuleSpec, ...]) -> str:
    payload = {
        "schema_version": "1.0",
        "project": config.to_dict(),
        "modules": [module.to_dict() for module in selected],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _render_device_source(source_path: Path) -> str:
    source = source_path.read_text(encoding="utf-8")
    source = re.sub(r"(?m)^(\s*)display_name=", r"\1displayname=", source)
    return re.sub(
        r"(?m)^(\s+)pass$",
        r'\1raise NotImplementedError("请在设备包中实现该动作")',
        source,
    )


def _render_package_init(selected: tuple[ModuleSpec, ...]) -> str:
    del selected
    return '"""生成的 Uni-Lab-OS 设备包。"""\nfrom . import devices as _devices\n'


def _render_devices_init(selected: tuple[ModuleSpec, ...]) -> str:
    imports = "\n".join(
        f"from . import {module.device_id} as _{module.device_id}" for module in selected
    )
    return f'"""设备模块目录。"""\n{imports}\n'


def _literal(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _render_opcua_runtime() -> str:
    return Path(__file__).with_name("opcua_runtime.py").read_text(encoding="utf-8")


def _class_name(device_id: str) -> str:
    return "".join(part.capitalize() for part in device_id.split("_"))


def _protocol_type(parameter_spec: str, *, property_type: bool = False) -> str:
    value = parameter_spec.strip()
    if property_type and ":" not in value:
        return value or "str"
    if ":" in value:
        return value.split(":", 1)[1].strip()
    return "str"


def _split_trigger_node(node: str, fallback: str) -> tuple[str, str]:
    parts = [part.strip() for part in node.split("/", 1)] if "/" in node else []
    if len(parts) == 2 and all(parts):
        return parts[0], parts[1]
    core = node.strip() or fallback.strip()
    for suffix in ("触发", "完成", "_Trigger", "_Complete"):
        if core.endswith(suffix):
            core = core[: -len(suffix)]
            break
    return f"{core}触发", f"{core}完成"


def _render_opcua_device_source(config: ProjectConfig, module: ModuleSpec) -> str:
    class_name = _class_name(module.device_id)
    category = json.dumps(list(module.category_path), ensure_ascii=False)
    lines = [
        f'"""{module.displayname} OPC UA 标准协议真实驱动。"""',
        "",
        "from pathlib import Path",
        "from typing import Any, Dict, Optional",
        "",
        "from unilabos.registry.decorators import action, device, topic_config",
        "",
        f"from {config.package_name}.opcua import OpcUaDeviceClient",
        "",
        f'_PROTOCOL_PATH = Path(__file__).resolve().parents[1] / "protocols" / "{module.device_id}.csv"',
        "",
        "",
        "@device(",
        f'    id="{module.device_id}",',
        f"    category={category},",
        f"    displayname={_literal(module.displayname)},",
        f"    description={_literal(f'{module.displayname} OPC UA 标准协议真实驱动。')},",
        ")",
        f"class {class_name}(OpcUaDeviceClient):",
        "    def __init__(",
        "        self,",
        "        url: str,",
        "        username: Optional[str] = None,",
        "        password: Optional[str] = None,",
        "        node_id_map: Optional[Dict[str, str]] = None,",
        "        node_id_prefix: Optional[str] = None,",
        "        browse_root: Optional[str] = None,",
        "        request_timeout: float = 10.0,",
        "        wait_timeout: float = 30.0,",
        "        poll_interval: float = 0.2,",
        "        auto_connect: bool = True,",
        "        **kwargs: Any,",
        "    ) -> None:",
        "        super().__init__(",
        "            url=url,",
        "            protocol_path=str(_PROTOCOL_PATH),",
        "            username=username,",
        "            password=password,",
        "            node_id_map=node_id_map,",
        "            node_id_prefix=node_id_prefix,",
        "            browse_root=browse_root,",
        "            request_timeout=request_timeout,",
        "            wait_timeout=wait_timeout,",
        "            poll_interval=poll_interval,",
        "            auto_connect=auto_connect,",
        "            **kwargs,",
        "        )",
    ]
    for contract in module.actions:
        if contract.parameter_spec:
            parameter, parameter_type = contract.parameter_spec.split(":", 1)
            node = contract.opcua_node or contract.description
            lines.extend(
                [
                    "",
                    f"    @action(description={_literal(contract.description)})",
                    f"    def {contract.name}(self, {parameter}: {parameter_type} = {_default_value(parameter_type)}) -> Dict[str, Any]:",
                    f'        """{contract.description}：写入标准节点 {node}。"""',
                    f"        self.set_node_value({_literal(node)}, {parameter})",
                    f"        return {{\"success\": True, \"message\": {_literal(f'{contract.description}已下发')}, {_literal(parameter)}: {parameter}}}",
                ]
            )
        else:
            trigger, complete = _split_trigger_node(contract.opcua_node, contract.description)
            lines.extend(
                [
                    "",
                    f"    @action(description={_literal(contract.description)})",
                    f"    def {contract.name}(self) -> Dict[str, Any]:",
                    f'        """{contract.description}：触发 {trigger}，等待 {complete} 完成并复位。"""',
                    f"        self.set_node_value({_literal(trigger)}, True)",
                    f"        if not self.wait_until_true({_literal(complete)}):",
                    f"            raise TimeoutError({_literal(f'{contract.description}完成等待超时')})",
                    f"        self.set_node_value({_literal(trigger)}, False)",
                    f"        if not self.wait_until_false({_literal(complete)}):",
                    f"            raise TimeoutError({_literal(f'{contract.description}复位等待超时')})",
                    f"        return {{\"success\": True, \"message\": {_literal(f'{contract.description}完成')}}}",
                ]
            )
    for contract in module.properties:
        property_type = _protocol_type(contract.parameter_spec, property_type=True)
        node = contract.opcua_node or contract.description
        lines.extend(
            [
                "",
                "    @property",
                "    @topic_config()",
                f"    def {contract.name}(self) -> {property_type}:",
                f'        """{contract.description}（读取标准节点 {node}）。"""',
                f"        return self.get_node_value({_literal(node)})",
            ]
        )
    return "\n".join(lines) + "\n"


def _default_value(parameter_type: str) -> str:
    return {"float": "0.0", "int": "0", "str": '""', "bool": "False"}.get(
        parameter_type.strip(), "None"
    )


def _render_protocol_csv(module: ModuleSpec) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["name", "node_type", "data_type", "source_kind", "source_name", "description", "node_id"])
    entries: list[tuple[str, str, str, str, str, str, str]] = []

    def add(name: str, data_type: str, kind: str, source_name: str, description: str) -> None:
        for index, entry in enumerate(entries):
            if entry[0] == name:
                if entry[2] != data_type:
                    entries[index] = (
                        entry[0],
                        entry[1],
                        entry[2],
                        entry[3],
                        f"{entry[4]};{source_name}",
                        f"{entry[5]}；{description}",
                        entry[6],
                    )
                return
        entries.append((name, "VARIABLE", data_type, kind, source_name, description, ""))

    for contract in module.actions:
        if contract.parameter_spec:
            add(
                contract.opcua_node or contract.description,
                _protocol_type(contract.parameter_spec),
                "action",
                contract.name,
                contract.description,
            )
        else:
            trigger, complete = _split_trigger_node(contract.opcua_node, contract.description)
            add(trigger, "bool", "action_trigger", contract.name, contract.description)
            add(complete, "bool", "action_complete", contract.name, contract.description)
    for contract in module.properties:
        add(
            contract.opcua_node or contract.description,
            _protocol_type(contract.parameter_spec, property_type=True),
            "property",
            contract.name,
            contract.description,
        )
    for entry in entries:
        writer.writerow(entry)
    return output.getvalue()
