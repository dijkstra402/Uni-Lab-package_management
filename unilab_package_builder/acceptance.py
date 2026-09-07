"""生成遵循 PLC-Sim 自动验收包规范的 L0 合同模板。"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .catalog import ModuleCatalog, ModuleSpec
from .config import ProjectConfig


class AcceptanceScaffoldError(ValueError):
    """自动验收包脚手架无法生成。"""


def generate_acceptance_bundle(
    config: ProjectConfig,
    catalog: ModuleCatalog,
    output_root: Path,
    *,
    force: bool = False,
) -> tuple[Path, ...]:
    """根据设备选择生成不猜测物理地址的 L0 自动验收包。"""

    config.validate()
    selected = catalog.select(config.modules)
    output_root = Path(output_root).resolve()
    if output_root.exists() and (
        not output_root.is_dir() or any(output_root.iterdir())
    ) and not force:
        raise AcceptanceScaffoldError(
            f"输出目录非空，使用 --force 覆盖生成文件: {output_root}"
        )

    project_id = f"{config.distribution_name}-acceptance"
    bundle_name = _bundle_name(config)
    bundle_root = output_root / "plc_acceptance" / "bundles" / bundle_name
    files: dict[Path, str] = {
        output_root / "pyproject.toml": _render_pyproject(config),
        output_root / "README.md": _render_readme(config, selected, bundle_name),
        output_root / "FRAMEWORK.md": _render_framework(),
        output_root / "DEVELOPMENT_STANDARD.md": _render_development_standard(),
        output_root / "device_selection.json": _render_selection(config, selected),
        output_root / "acceptance_selection.json": _render_acceptance_selection(
            config, selected, project_id
        ),
        output_root / "plc_acceptance" / "__init__.py": _render_init(config),
        output_root / "plc_acceptance" / "cli.py": _render_cli(bundle_name),
        output_root / "plc_acceptance" / "validator.py": _render_validator(
            bundle_name
        ),
        output_root / "plc_acceptance" / "runner.py": _render_runner(),
        output_root / "plc_acceptance" / "reporting.py": _render_reporting(),
        output_root / "plc_acceptance" / "simulator.py": _render_simulator(),
        output_root / "tests_py" / "test_bundle.py": _render_bundle_test(bundle_name),
        output_root / "reports" / ".gitkeep": "",
        bundle_root / "protocol" / "plc-interface.yaml": _render_protocol(
            config, selected, project_id
        ),
        bundle_root / "protocol" / "test-manifest.yaml": _render_manifest(
            selected, project_id
        ),
        bundle_root / "protocol" / "requirements-coverage.yaml": _render_coverage(
            selected
        ),
        bundle_root / "mappings" / f"{bundle_name}.yaml": _render_mapping(config),
        bundle_root / "environments" / "simulator.yaml": _render_environment(config),
        bundle_root / "simulator" / "simulation-profile.yaml": _render_simulation_profile(
            config
        ),
        bundle_root / "tests" / "common" / "handshake.yaml": _render_empty_cases(
            "通用握手用例由项目点表补齐"
        ),
        bundle_root / "tests" / "project" / "selection.yaml": _render_project_cases(
            config, selected
        ),
    }
    for module in selected:
        _validate_device_id(module.device_id)
        files[
            bundle_root / "tests" / "devices" / f"{module.device_id}.yaml"
        ] = _render_device_cases(module)

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tuple(files)


def _validate_device_id(device_id: str) -> None:
    if not re.fullmatch(r"[a-zA-Z0-9_]+", device_id):
        raise AcceptanceScaffoldError(f"设备 ID 不能安全生成验收文件名: {device_id}")


def _bundle_name(config: ProjectConfig) -> str:
    return config.package_name


def _yaml_string(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _yaml_list(values: tuple[str, ...] | list[str]) -> str:
    return "[" + ", ".join(_yaml_string(value) for value in values) + "]"


def _case_prefix(device_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", device_id.upper()).strip("-")


def _render_pyproject(config: ProjectConfig) -> str:
    distribution_name = json.dumps(
        f"{config.distribution_name}-acceptance", ensure_ascii=False
    )
    description = json.dumps(
        f"{config.description} 的 PLC 自动验收合同模板", ensure_ascii=False
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
dependencies = ["PyYAML>=6.0,<7"]

[project.optional-dependencies]
test = ["pytest>=8,<9"]

[project.scripts]
plc-acceptance = "plc_acceptance.cli:main"

[tool.setuptools.packages.find]
include = ["plc_acceptance*"]

[tool.setuptools.package-data]
plc_acceptance = ["bundles/**/*.yaml"]

[tool.pytest.ini_options]
testpaths = ["tests_py"]
'''


def _render_readme(
    config: ProjectConfig,
    selected: tuple[ModuleSpec, ...],
    bundle_name: str,
) -> str:
    module_lines = "\n".join(
        f"- `{module.device_id}`：{module.displayname}；动作 {len(module.actions)} 个，属性 {len(module.properties)} 个"
        for module in selected
    )
    return f'''# {config.description} · PLC 自动验收包

这是由 `unilab-package-builder` 根据设备包选择生成的 PLC 自动验收工程模板，目录结构对齐
PLC-Sim `automation-acceptance` 分支的验收包规范。

## 当前证据边界

本下载包是 **L0 合同模板**，不是已经连接 PLC 的通过报告。生成器只知道 Uni-Lab-OS
设备动作和状态合同，不知道供应商点表、OPC UA Namespace、NodeId、完成条件或安全回路，
所以这些内容全部保留为明确的 `BLOCKED` / `REPLACE_WITH_...` 门禁，不会伪造成功。

## 已选择设备

{module_lines}

## 目录与工作流

- `plc_acceptance/bundles/{bundle_name}/protocol/`：逻辑变量协议、测试清单和规范覆盖表；
- `plc_acceptance/bundles/{bundle_name}/mappings/`：供应商点表和 NodeId 映射占位；
- `plc_acceptance/bundles/{bundle_name}/environments/`：仿真环境占位，默认禁止物理动作；
- `plc_acceptance/bundles/{bundle_name}/tests/`：每个所选设备的就绪、动作、失败、超时、重启和非法参数用例模板；
- `device_selection.json`：与设备包生成使用的同一份选择快照；
- `acceptance_selection.json`：验收包的项目身份和合同摘要。

## 使用步骤

```bash
python -m pip install -e '.[test]'
plc-acceptance validate
```

首次校验预期为 `BLOCKED`，因为还没有真实点表和项目映射。接入具体 PLC-Sim 或供应商
软 PLC 时，应由验收工程维护者补齐 `mappings/{bundle_name}.yaml`、协议逻辑 ID、环境 Endpoint
和真实用例，再按 L0 → L1 → L2 → L3/L4 逐级执行。测试用例只引用逻辑 ID；物理 NodeId
只能存在于项目映射或点表中。
'''


def _render_framework() -> str:
    return '''# 自动验收工程框架

本工程采用 PLC-Sim `automation-acceptance` 的配置驱动边界：

1. `protocol/` 声明稳定逻辑变量和数据类型；
2. `mappings/` 将项目点表映射到逻辑变量；
3. `environments/` 声明 Endpoint、证据等级和安全门禁；
4. `tests/` 只通过逻辑 ID 编写前置、刺激、断言和清理；
5. `requirements-coverage.yaml` 记录自动、人工、部分和阻塞证据。

生成器只填充设备包的公开动作/属性合同，不跨仓库复制 PLC-Sim 实现，也不推断供应商
点位。L0 模板校验与真实 OPC UA/HTTP 运行严格分开。
'''


def _render_development_standard() -> str:
    return '''# 自动验收包开发规范

- 不在测试 YAML 中写物理 NodeId；
- 不把设备动作名直接当作 PLC 完成位；
- 没有点表、故障位、心跳、初始化或安全回路证据时必须标记 `blocked`；
- 每个设备补齐 ready/state 观察、代表性动作闭环、清理、失败/超时/重启/非法参数覆盖；
- 真实设备测试前必须确认受控测试模式、权限、监护人和现场证据；
- 结果状态使用 `PASSED`、`FAILED`、`BLOCKED` 或 `ABORTED`，不得以固定 sleep 伪造完成。
'''


def _render_selection(config: ProjectConfig, selected: tuple[ModuleSpec, ...]) -> str:
    payload = {
        "schema_version": "1.0",
        "project": config.to_dict(),
        "modules": [module.to_dict() for module in selected],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _render_acceptance_selection(
    config: ProjectConfig,
    selected: tuple[ModuleSpec, ...],
    project_id: str,
) -> str:
    payload = {
        "schema": "unilab.package_builder.acceptance_selection/v1",
        "project_id": project_id,
        "device_package": config.to_dict(),
        "evidence_level": "L0 contract template",
        "mapping_status": "blocked_pending_supplier_point_table",
        "modules": [
            {
                "device_id": module.device_id,
                "displayname": module.displayname,
                "actions": [item.to_dict() for item in module.actions],
                "properties": [item.to_dict() for item in module.properties],
            }
            for module in selected
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _render_init(config: ProjectConfig) -> str:
    return f'''"""{config.description} 的自动验收包。"""

__version__ = "{config.version}"
'''


def _render_cli(bundle_name: str) -> str:
    return '''"""L0 自动验收合同模板的命令行入口。"""

from __future__ import annotations

import argparse
from pathlib import Path

from .reporting import write_report
from .runner import run_acceptance
from .validator import validate_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="plc-acceptance")
    parser.add_argument("--root", type=Path, default=Path(__file__).parent / "bundles" / "__BUNDLE_NAME__")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="执行 L0 合同模板检查")
    run = commands.add_parser("run", help="生成明确阻塞的 L0 运行记录")
    run.add_argument("--output", type=Path, default=Path("reports"))
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "validate":
        findings = validate_bundle(root)
        for finding in findings:
            print(f"[BLOCKED] {finding}")
        print(f"L0 BLOCKED: {len(findings)} 项待补齐")
        return 1 if findings else 0
    result = run_acceptance(root)
    report_path = write_report(result, args.output)
    print(f"BLOCKED: {result['reason']}")
    print(f"报告: {report_path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
'''.replace("__BUNDLE_NAME__", bundle_name)


def _render_validator(bundle_name: str) -> str:
    return '''"""验证自动验收包的 L0 文件边界和未映射门禁。"""

from __future__ import annotations

import re
from pathlib import Path

import yaml


REQUIRED_FILES = (
    "protocol/plc-interface.yaml",
    "protocol/test-manifest.yaml",
    "protocol/requirements-coverage.yaml",
    "mappings/__BUNDLE_NAME__.yaml",
    "environments/simulator.yaml",
    "simulator/simulation-profile.yaml",
)


def validate_bundle(root: str | Path) -> list[str]:
    """返回 L0 模板中仍需项目验收工程补齐的门禁。"""

    bundle_root = Path(root).resolve()
    findings = [
        f"缺少验收包文件: {relative}"
        for relative in REQUIRED_FILES
        if not (bundle_root / relative).is_file()
    ]
    mapping_path = bundle_root / "mappings" / "__BUNDLE_NAME__.yaml"
    if mapping_path.is_file():
        mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8")) or {}
        if str(mapping.get("csv_path", "")).startswith("REPLACE_WITH_"):
            findings.append("供应商点表尚未绑定: mappings/__BUNDLE_NAME__.yaml")
        if str(mapping.get("namespace_uri", "")).startswith("REPLACE_WITH_"):
            findings.append("OPC UA Namespace 尚未绑定: mappings/__BUNDLE_NAME__.yaml")
    for path in bundle_root.rglob("*"):
        if not path.is_file() or path.suffix not in {".yaml", ".yml", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"ns=\\d+;s=", text):
            findings.append(f"发现不应出现在合同包中的物理 NodeId: {path.name}")
    return findings
'''.replace("__BUNDLE_NAME__", bundle_name)


def _render_runner() -> str:
    return '''"""提供诚实的 L0 运行结果，不连接未知 PLC Endpoint。"""

from __future__ import annotations

from pathlib import Path

from .validator import validate_bundle


def run_acceptance(root: str | Path) -> dict[str, object]:
    """返回待补齐真实点表和环境前的 BLOCKED 结果。"""

    findings = validate_bundle(root)
    return {
        "status": "BLOCKED",
        "evidence_level": "L0 contract template",
        "reason": "生成包没有供应商点表、物理映射和可验证 PLC Endpoint",
        "findings": findings,
    }
'''


def _render_reporting() -> str:
    return '''"""写出可追踪的 L0 阻塞记录。"""

from __future__ import annotations

import json
from pathlib import Path


def write_report(result: dict[str, object], output_root: str | Path) -> Path:
    """将运行结果写入 reports/run.json。"""

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / "run.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    return path
'''


def _render_simulator() -> str:
    return '''"""保留 PLC-Sim 接缝，待项目验收工程提供真实仿真配置。"""

from __future__ import annotations

from pathlib import Path

from .runner import run_acceptance


def run_simulator_acceptance(root: str | Path) -> dict[str, object]:
    """当前只返回 L0 阻塞结果，不启动未知的外部仿真器。"""

    return run_acceptance(root)
'''


def _render_bundle_test(bundle_name: str) -> str:
    return '''from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = ROOT / "plc_acceptance" / "bundles" / "__BUNDLE_NAME__"


def test_selected_devices_have_acceptance_case_files() -> None:
    selection = json.loads((ROOT / "acceptance_selection.json").read_text(encoding="utf-8"))
    device_ids = {item["device_id"] for item in selection["modules"]}
    case_ids = {path.stem for path in (BUNDLE_ROOT / "tests" / "devices").glob("*.yaml")}
    assert device_ids == case_ids


def test_contract_templates_do_not_guess_physical_node_ids() -> None:
    physical_node_id = re.compile(r"ns=\\d+;s=")
    for path in BUNDLE_ROOT.rglob("*.yaml"):
        assert physical_node_id.search(path.read_text(encoding="utf-8")) is None
'''.replace("__BUNDLE_NAME__", bundle_name)


def _render_protocol(
    config: ProjectConfig,
    selected: tuple[ModuleSpec, ...],
    project_id: str,
) -> str:
    lines = [
        "schema: unilab.plc_acceptance.protocol/v1",
        f"project_id: {_yaml_string(project_id)}",
        "protocol_version: 0.1.0",
        "status: draft",
        "source:",
        '  specification: "PLC-Sim automation-acceptance contract template"',
        f"  device_package_selection: {_yaml_string('device_selection.json')}",
        '  mapping_status: "blocked_pending_supplier_point_table"',
        "",
        "nodes:",
    ]
    for module in selected:
        prefix = f"device.{module.device_id}"
        nodes = (
            (f"{prefix}.ready", "ready", "plc", "设备可接收动作的状态观察点"),
            (f"{prefix}.fault", "fault", "plc", "设备故障状态观察点"),
            (
                f"{prefix}.action_request",
                "action_request",
                "host",
                "代表性动作请求触发点",
            ),
            (f"{prefix}.action_done", "action_done", "plc", "代表性动作完成观察点"),
        )
        for logical_id, name, owner, description in nodes:
            lines.extend(
                [
                    f"  - id: {_yaml_string(logical_id)}",
                    f"    name: {_yaml_string(f'REPLACE_WITH_{module.device_id}_{name}')}",
                    "    data_type: BOOLEAN",
                    f"    owner: {owner}",
                    "    required: true",
                    f"    description: {_yaml_string(description)}",
                ]
            )
    lines.extend(["", "device_contracts:"])
    for module in selected:
        lines.extend(
            [
                f"  - device_id: {_yaml_string(module.device_id)}",
                f"    displayname: {_yaml_string(module.displayname)}",
                f"    category_path: {_yaml_list(list(module.category_path))}",
                "    actions:",
            ]
        )
        for contract in module.actions:
            lines.extend(
                [
                    f"      - name: {_yaml_string(contract.name)}",
                    f"        description: {_yaml_string(contract.description)}",
                    f"        parameter_spec: {_yaml_string(contract.parameter_spec)}",
                ]
            )
        if not module.actions:
            lines.append("      []")
        lines.append("    properties:")
        for contract in module.properties:
            lines.extend(
                [
                    f"      - name: {_yaml_string(contract.name)}",
                    f"        description: {_yaml_string(contract.description)}",
                    f"        parameter_spec: {_yaml_string(contract.parameter_spec)}",
                ]
            )
        if not module.properties:
            lines.append("      []")
    return "\n".join(lines) + "\n"


def _render_manifest(
    selected: tuple[ModuleSpec, ...], project_id: str
) -> str:
    lines = [
        "schema: unilab.plc_acceptance.manifest/v1",
        f"project_id: {_yaml_string(project_id)}",
        "manifest_version: 0.1.0",
        "case_files:",
        "  - tests/common/*.yaml",
        "  - tests/devices/*.yaml",
        "  - tests/project/*.yaml",
        "",
        "cases:",
        "  - id: CT-001",
        "    required: true",
        "    safety_level: P0",
        "  - id: CT-002",
        "    required: true",
        "    safety_level: P0",
    ]
    for module in selected:
        prefix = _case_prefix(module.device_id)
        for suffix, safety in (
            ("READY-001", "P0"),
            ("ACTION-001", "P1"),
            ("FAILURE-001", "P1"),
            ("TIMEOUT-001", "P1"),
            ("RESTART-001", "P1"),
            ("INVALID-PARAM-001", "P1"),
        ):
            lines.extend(
                [
                    f"  - id: DEV-{prefix}-{suffix}",
                    "    required: true",
                    "    required_environments: [template]",
                    f"    safety_level: {safety}",
                ]
            )
    return "\n".join(lines) + "\n"


def _render_coverage(selected: tuple[ModuleSpec, ...]) -> str:
    lines = [
        "schema: unilab.plc_acceptance.coverage/v1",
        'baseline: "PLC-Sim automation-acceptance development standard"',
        "scope: generated_device_package",
        "",
        "requirements:",
        "  - requirement: PACKAGE-CONTRACT",
        "    status: automated",
        '    evidence: "device_selection.json and protocol/plc-interface.yaml"',
        "  - requirement: PLC-MAPPING",
        "    status: blocked",
        '    evidence: "供应商点表、Namespace 和 NodeId 尚未提供"',
        "  - requirement: DEVICE-READY-STATE",
        "    status: blocked",
        '    evidence: "每个设备有 ready/fault 逻辑变量模板，待项目映射"',
        "  - requirement: DEVICE-ACTION-LOOP",
        "    status: blocked",
        '    evidence: "动作请求/完成模板待供应商完成条件和仿真行为"',
        "  - requirement: FAILURE-TIMEOUT-RESTART-INVALID",
        "    status: blocked",
        '    evidence: "每设备用例已列入清单，执行前需补齐可观察故障与重启接口"',
        "  - requirement: SAFETY-EVIDENCE",
        "    status: blocked",
        '    evidence: "L3/L4 监护人、现场位置和物料证据尚未提供"',
    ]
    for module in selected:
        lines.extend(
            [
                f"  - requirement: DEVICE-{module.device_id}",
                "    status: blocked",
                f"    evidence: {_yaml_string(f'{module.displayname} 的 PLC 映射和动作闭环待补齐')}",
            ]
        )
    return "\n".join(lines) + "\n"


def _render_mapping(config: ProjectConfig) -> str:
    return f'''schema: unilab.plc_acceptance.mapping/v1
mapping_version: 0.1.0
csv_path: "REPLACE_WITH_SUPPLIER_POINT_TABLE.csv"
expected_scalar_nodes: 0
namespace_uri: "REPLACE_WITH_OPC_UA_NAMESPACE_URI"
node_id_prefix: "REPLACE_WITH_NODE_ID_PREFIX"
project_id: {_yaml_string(config.distribution_name)}
mapping_status: blocked_pending_supplier_point_table

# 测试用例只引用逻辑 ID；补齐点表后仍通过本文件统一解析物理 NodeId。
'''


def _render_environment(config: ProjectConfig) -> str:
    return f'''schema: unilab.plc_acceptance.environment/v1
id: {_yaml_string(f'{config.package_name}-acceptance-template')}
kind: template
endpoint: "REPLACE_WITH_PLC_SIM_OR_SUPPLIER_ENDPOINT"
connect_timeout_ms: 5000
poll_interval_ms: 20
enforce_access_level: true
allow_physical_actions: false
evidence_level: "L0 合同模板"
scope_statement: "仅证明所选设备合同和验收目录已生成，不代表 PLC-Sim、软 PLC、台架或真机验收。"
required_evidence_fields: []
case_repeat_overrides: {{}}
service_endpoints: {{}}
'''


def _render_simulation_profile(config: ProjectConfig) -> str:
    return f'''schema: unilab.plc_acceptance.simulator/v1
implementation: project_owned
server_profile: {_yaml_string(f'{config.package_name}-simulator-profile-to-be-defined')}
handshake_config: "REPLACE_WITH_PROJECT_HANDSHAKE_CONFIG"
evidence_label: "L0 合同模板，不等同于 PLC-Sim、软 PLC、台架或硬件验收"
'''


def _render_empty_cases(description: str) -> str:
    return f'''schema: unilab.plc_acceptance.cases/v1
description: {_yaml_string(description)}
cases: []
'''


def _render_project_cases(
    config: ProjectConfig, selected: tuple[ModuleSpec, ...]
) -> str:
    module_ids = _yaml_list([module.device_id for module in selected])
    return f'''schema: unilab.plc_acceptance.cases/v1
project_id: {_yaml_string(config.distribution_name)}
selected_devices: {module_ids}
cases: []
'''


def _render_device_cases(module: ModuleSpec) -> str:
    prefix = _case_prefix(module.device_id)
    logical_prefix = f"device.{module.device_id}"
    contract_names = _yaml_list([item.name for item in module.actions])
    lines = [
        "schema: unilab.plc_acceptance.cases/v1",
        f"device_id: {_yaml_string(module.device_id)}",
        f"displayname: {_yaml_string(module.displayname)}",
        f"contract_actions: {contract_names}",
        f"contract_properties: {_yaml_list([item.name for item in module.properties])}",
        "",
        "cases:",
        f"  - id: DEV-{prefix}-READY-001",
        f"    name: {_yaml_string(f'{module.displayname} 就绪与故障状态可观测')}",
        "    level: L0",
        "    safety_level: P0",
        "    environments: [template]",
        "    physical_effect: false",
        "    given:",
        f"      - {{action: assert, node: {_yaml_string(f'{logical_prefix}.ready')}, equals: true}}",
        f"      - {{action: assert, node: {_yaml_string(f'{logical_prefix}.fault')}, equals: false}}",
        "    when: []",
        "    cleanup: []",
        "    status: blocked",
        '    block_reason: "待供应商点表映射 ready/fault 变量"',
        f"  - id: DEV-{prefix}-ACTION-001",
        f"    name: {_yaml_string(f'{module.displayname} 代表性动作请求完成闭环')}",
        "    level: L0",
        "    safety_level: P1",
        "    environments: [template]",
        "    physical_effect: false",
        "    given:",
        f"      - {{action: assert, node: {_yaml_string(f'{logical_prefix}.ready')}, equals: true}}",
        "    when:",
        f"      - {{action: write, node: {_yaml_string(f'{logical_prefix}.action_request')}, value: true}}",
        f"      - {{action: wait, node: {_yaml_string(f'{logical_prefix}.action_done')}, equals: true, timeout_ms: 3000}}",
        f"      - {{action: assert, node: {_yaml_string(f'{logical_prefix}.fault')}, equals: false}}",
        "    cleanup:",
        f"      - {{action: write, node: {_yaml_string(f'{logical_prefix}.action_request')}, value: false}}",
        f"      - {{action: wait, node: {_yaml_string(f'{logical_prefix}.action_done')}, equals: false, timeout_ms: 1000}}",
        "    status: blocked",
        '    block_reason: "待供应商定义动作请求、完成条件和清理语义"',
    ]
    for suffix, name in (
        ("FAILURE-001", "故障回执与安全失败路径"),
        ("TIMEOUT-001", "超时不误报完成"),
        ("RESTART-001", "重启后状态恢复与证据绑定"),
        ("INVALID-PARAM-001", "非法参数被拒绝且不产生伪成功"),
    ):
        lines.extend(
            [
                f"  - id: DEV-{prefix}-{suffix}",
                f"    name: {_yaml_string(f'{module.displayname} {name}')}",
                "    level: L0",
                "    safety_level: P1",
                "    environments: [template]",
                "    physical_effect: false",
                "    given: []",
                "    when: []",
                "    cleanup: []",
                "    status: blocked",
                f'    block_reason: "{name}需要项目点表、仿真行为或供应商证据"',
            ]
        )
    return "\n".join(lines) + "\n"
