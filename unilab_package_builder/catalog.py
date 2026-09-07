"""静态读取设备模块目录，不导入设备包作者代码。"""

from __future__ import annotations

import ast
import csv
from dataclasses import dataclass
from pathlib import Path


class CatalogError(ValueError):
    """设备模块目录无效。"""


@dataclass(frozen=True, slots=True)
class ContractSpec:
    """设备模块公开的动作或状态属性合同。"""

    kind: str
    name: str
    description: str
    parameter_spec: str

    def to_dict(self) -> dict[str, str]:
        """返回供设备包和验收工程消费的稳定合同投影。"""

        return {
            "kind": self.kind,
            "name": self.name,
            "description": self.description,
            "parameter_spec": self.parameter_spec,
        }


@dataclass(frozen=True, slots=True)
class ModuleSpec:
    """一个可被选择的设备模块及其源码位置。"""

    device_id: str
    displayname: str
    category: str
    category_path: tuple[str, ...]
    source_path: Path
    plc_source_path: Path | None
    actions: tuple[ContractSpec, ...]
    properties: tuple[ContractSpec, ...]

    def to_dict(self) -> dict[str, object]:
        """返回不包含绝对路径的稳定目录投影。"""

        return {
            "device_id": self.device_id,
            "displayname": self.displayname,
            "category": self.category,
            "category_path": list(self.category_path),
            "source_path": self.source_path.as_posix(),
            "plc_source_path": (
                self.plc_source_path.as_posix() if self.plc_source_path else None
            ),
            "actions": [item.to_dict() for item in self.actions],
            "properties": [item.to_dict() for item in self.properties],
        }


class ModuleCatalog:
    """从当前仓库的分类清单和设备源码构建 139 模块目录。"""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = Path(repository_root).resolve()
        self._modules = self._load_modules()

    @property
    def modules(self) -> tuple[ModuleSpec, ...]:
        """返回按设备 ID 排序的完整模块集合。"""

        return self._modules

    def get(self, device_id: str) -> ModuleSpec:
        """按稳定设备 ID 获取模块，不执行模块源码。"""

        for module in self._modules:
            if module.device_id == device_id:
                return module
        raise CatalogError(f"未知设备模块: {device_id}")

    def select(self, device_ids: tuple[str, ...]) -> tuple[ModuleSpec, ...]:
        """按用户配置返回去重且保持配置顺序的模块。"""

        selected: list[ModuleSpec] = []
        seen: set[str] = set()
        for device_id in device_ids:
            if device_id in seen:
                raise CatalogError(f"设备模块重复选择: {device_id}")
            seen.add(device_id)
            selected.append(self.get(device_id))
        if not selected:
            raise CatalogError("至少选择一个设备模块")
        return tuple(selected)

    def search(self, query: str = "", category_prefix: str = "") -> tuple[ModuleSpec, ...]:
        """按设备 ID、名称或分类路径筛选模块。"""

        normalized_query = query.casefold().strip()
        normalized_category = category_prefix.strip()
        return tuple(
            module
            for module in self._modules
            if (not normalized_query or self._matches_query(module, normalized_query))
            and (
                not normalized_category
                or " > ".join(module.category_path).startswith(normalized_category)
            )
        )

    def _matches_query(self, module: ModuleSpec, query: str) -> bool:
        searchable = (
            module.device_id,
            module.displayname,
            module.category,
            " > ".join(module.category_path),
        )
        return any(query in value.casefold() for value in searchable)

    def _load_modules(self) -> tuple[ModuleSpec, ...]:
        category_rows = self._load_category_rows()
        contracts = self._load_contracts()
        packages_root = self.repository_root / "packages"
        package_ids: set[str] = set()
        modules: list[ModuleSpec] = []
        for package_dir in sorted(packages_root.iterdir()):
            source_path = package_dir / package_dir.name / f"{package_dir.name}.py"
            if not source_path.is_file():
                continue
            device_id, displayname, category = _read_device_metadata(source_path)
            if device_id != package_dir.name:
                raise CatalogError(
                    f"设备目录与 @device id 不一致: {package_dir.name} != {device_id}"
                )
            package_ids.add(device_id)
            category_row = category_rows.get(device_id)
            if category_row is None:
                raise CatalogError(f"分类清单缺少设备模块: {device_id}")
            modules.append(
                ModuleSpec(
                    device_id=device_id,
                    displayname=displayname or category,
                    category=category,
                    category_path=category_row["path"],
                    source_path=source_path.relative_to(self.repository_root),
                    plc_source_path=(
                        (source_path.parent / f"{device_id}_plc.py").relative_to(
                            self.repository_root
                        )
                        if (source_path.parent / f"{device_id}_plc.py").is_file()
                        else None
                    ),
                    actions=tuple(
                        item for item in contracts.get(device_id, ()) if item.kind == "action"
                    ),
                    properties=tuple(
                        item
                        for item in contracts.get(device_id, ())
                        if item.kind == "property"
                    ),
                )
            )
        unknown_rows = set(category_rows) - package_ids
        if unknown_rows:
            raise CatalogError(
                "分类清单包含不存在的设备目录: " + ", ".join(sorted(unknown_rows))
            )
        if len(modules) != 139:
            raise CatalogError(f"设备模块数量应为 139，实际为 {len(modules)}")
        return tuple(sorted(modules, key=lambda module: module.device_id))

    def _load_contracts(self) -> dict[str, tuple[ContractSpec, ...]]:
        contract_path = self.repository_root / "device_templates_actions.csv"
        if not contract_path.is_file():
            raise CatalogError(f"动作合同不存在: {contract_path}")
        contracts: dict[str, list[ContractSpec]] = {}
        with contract_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_fields = {"device_id", "类型", "英文名", "中文描述", "参数(名:类型)"}
            if not required_fields <= set(reader.fieldnames or ()):
                raise CatalogError(f"动作合同列不完整: {reader.fieldnames}")
            for row in reader:
                device_id = (row.get("device_id") or "").strip()
                kind = (row.get("类型") or "").strip()
                if kind not in {"action", "property"} or not device_id:
                    raise CatalogError(f"动作合同记录无效: {row}")
                contracts.setdefault(device_id, []).append(
                    ContractSpec(
                        kind=kind,
                        name=(row.get("英文名") or "").strip(),
                        description=(row.get("中文描述") or "").strip(),
                        parameter_spec=(row.get("参数(名:类型)") or "").strip(),
                    )
                )
        return {device_id: tuple(items) for device_id, items in contracts.items()}

    def _load_category_rows(self) -> dict[str, dict[str, object]]:
        category_path = self.repository_root / "instrument_category_paths.csv"
        if not category_path.is_file():
            raise CatalogError(f"分类清单不存在: {category_path}")
        rows: dict[str, dict[str, object]] = {}
        with category_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_fields = {"设备大类", "device_id", "仪器分类路径"}
            if not required_fields <= set(reader.fieldnames or ()):
                raise CatalogError(f"分类清单列不完整: {reader.fieldnames}")
            for row in reader:
                device_id = (row.get("device_id") or "").strip()
                category = (row.get("设备大类") or "").strip()
                path = tuple(
                    part.strip()
                    for part in (row.get("仪器分类路径") or "").split(" > ")
                    if part.strip()
                )
                if not device_id or not category or not path:
                    raise CatalogError(f"分类清单记录不完整: {row}")
                if device_id in rows:
                    raise CatalogError(f"分类清单设备重复: {device_id}")
                rows[device_id] = {"category": category, "path": path}
        if len(rows) != 139:
            raise CatalogError(f"分类清单数量应为 139，实际为 {len(rows)}")
        return rows


def _read_device_metadata(source_path: Path) -> tuple[str, str, str]:
    """通过 AST 读取 @device 元数据，绝不执行源码。"""

    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            if not isinstance(decorator.func, ast.Name) or decorator.func.id != "device":
                continue
            values = {
                keyword.arg: ast.literal_eval(keyword.value)
                for keyword in decorator.keywords
                if keyword.arg in {"id", "category", "displayname", "display_name"}
            }
            device_id = values.get("id")
            category = values.get("category")
            displayname = values.get("displayname") or values.get("display_name") or ""
            if not isinstance(device_id, str) or not isinstance(category, list):
                raise CatalogError(f"设备元数据不完整: {source_path}")
            if not all(isinstance(item, str) for item in category):
                raise CatalogError(f"设备分类必须是字符串列表: {source_path}")
            return device_id, str(displayname), category[-1]
    raise CatalogError(f"找不到 @device: {source_path}")
