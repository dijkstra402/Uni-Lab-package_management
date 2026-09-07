"""生成遵循 Uni-Lab-OS 外部设备包契约的项目脚手架。"""

from __future__ import annotations

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
        package_root / "__init__.py": '"""生成的 Uni-Lab-OS 设备包。"""\n',
        devices_root / "__init__.py": '"""设备模块目录。"""\n',
        output_root / "device_selection.json": _render_selection(config, selected),
    }
    for module in selected:
        source = catalog.repository_root / module.source_path
        files[devices_root / f"{module.device_id}.py"] = _render_device_source(source)
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tuple(files)


def _render_pyproject(config: ProjectConfig) -> str:
    distribution_name = json.dumps(config.distribution_name, ensure_ascii=False)
    description = json.dumps(config.description, ensure_ascii=False)
    package_include = json.dumps(f"{config.package_name}*", ensure_ascii=False)
    return f'''[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = {distribution_name}
version = "{config.version}"
description = {description}
readme = "README.md"
requires-python = ">=3.11"
dependencies = ["unilabos>=0.11.3"]

[project.optional-dependencies]
dev = ["pytest>=8,<9", "ruff>=0.6"]

[tool.setuptools.packages.find]
include = [{package_include}]

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
    return f'''# {config.description}

这是由 `unilab-package-builder` 根据设备模块选择配置生成的 Uni-Lab-OS 外部设备包。
设备动作和状态接口来自选中的标准模块；未实现的动作会明确抛出
`NotImplementedError`，不会伪造成功结果。

## 已选择模块

{module_lines}

## 开发与校验

```bash
python -m pip install -e '.[dev]'
unilab --check_mode --devices ./{config.package_name} --external_devices_only
unilab package inspect --path . --out ./artifacts
unilab package build --path . --out ./artifacts
```

设备真实通信适配器、配置、资源和工作流应继续放在本设备包内；PLC 点表、NodeId 和验收用例
由对应的仿真/验收工程通过公开协议接缝提供，不写入本脚手架的选择配置。
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
