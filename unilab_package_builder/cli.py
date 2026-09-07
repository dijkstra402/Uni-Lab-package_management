"""设备包选择器的命令行 Adapter。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalog import CatalogError, ModuleCatalog
from .config import ConfigError, ProjectConfig, load_project_config
from .scaffold import ScaffoldError, generate_project
from .ui_server import serve_ui


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)
    try:
        catalog = ModuleCatalog(arguments.repository)
        if arguments.command == "list":
            return _list_modules(catalog, arguments)
        if arguments.command == "validate":
            config = load_project_config(arguments.config)
            selected = catalog.select(config.modules)
            print(f"配置有效：{config.package_name}，已选择 {len(selected)} 个模块")
            return 0
        if arguments.command == "init":
            config = _load_init_config(arguments)
            files = generate_project(
                config,
                catalog,
                arguments.out,
                force=arguments.force,
            )
            print(f"已生成设备包：{Path(arguments.out).resolve()}")
            print(f"写入文件：{len(files)} 个；设备模块：{len(config.modules)} 个")
            return 0
        if arguments.command == "ui":
            serve_ui(arguments.repository, arguments.host, arguments.port)
            return 0
    except (CatalogError, ConfigError, ScaffoldError, OSError) as error:
        parser.error(str(error))
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="选择 Uni-Lab 设备模块并生成设备包")
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path.cwd(),
        help="package_management 仓库根目录，默认使用当前目录",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="列出可选设备模块")
    list_parser.add_argument("--query", default="", help="按 ID、名称或分类搜索")
    list_parser.add_argument("--category", default="", help="按分类路径前缀筛选")
    list_parser.add_argument("--format", choices=("table", "json"), default="table")

    validate_parser = subparsers.add_parser("validate", help="校验模块选择配置")
    validate_parser.add_argument("--config", type=Path, required=True)

    init_parser = subparsers.add_parser("init", help="根据配置生成设备包")
    init_source = init_parser.add_mutually_exclusive_group(required=True)
    init_source.add_argument("--config", type=Path)
    init_source.add_argument("--module", dest="modules", action="append")
    init_parser.add_argument("--package-name", help="直接选择模块时的导入包名称")
    init_parser.add_argument("--distribution-name", help="直接选择模块时的发行名称")
    init_parser.add_argument("--description", default="Uni-Lab-OS 设备包")
    init_parser.add_argument("--version", default="0.1.0")
    init_parser.add_argument("--out", type=Path, required=True)
    init_parser.add_argument("--force", action="store_true", help="允许覆盖已有输出文件")

    ui_parser = subparsers.add_parser("ui", help="启动设备包选配 UI")
    ui_parser.add_argument("--host", default="127.0.0.1", help="监听地址，默认仅本机访问")
    ui_parser.add_argument("--port", type=int, default=8765, help="监听端口，默认 8765")
    return parser


def _load_init_config(arguments: argparse.Namespace) -> ProjectConfig:
    if arguments.config is not None:
        return load_project_config(arguments.config)
    if not arguments.package_name:
        raise ConfigError("直接选择模块时必须提供 --package-name")
    distribution_name = arguments.distribution_name or arguments.package_name
    config = ProjectConfig(
        distribution_name=distribution_name,
        package_name=arguments.package_name,
        modules=tuple(arguments.modules or ()),
        version=arguments.version,
        description=arguments.description,
    )
    config.validate()
    return config


def _list_modules(catalog: ModuleCatalog, arguments: argparse.Namespace) -> int:
    modules = catalog.search(arguments.query, arguments.category)
    if arguments.format == "json":
        print(json.dumps([module.to_dict() for module in modules], ensure_ascii=False, indent=2))
        return 0
    print("device_id\t设备大类\t仪器分类路径")
    for module in modules:
        print(f"{module.device_id}\t{module.category}\t{' > '.join(module.category_path)}")
    print(f"共 {len(modules)} 个模块")
    return 0
