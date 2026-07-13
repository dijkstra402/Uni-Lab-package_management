#!/usr/bin/env python3
"""查询并校验当前 Uni-Lab 设备接口标准。"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


字段 = [
    "设备大类", "device_id", "类型", "英文名", "中文描述",
    "参数(名:类型)", "PLC节点", "交互模式",
]
基础类型 = {"bool", "int", "float", "str"}
标识符格式 = re.compile(r"^[a-z_][a-z0-9_]*$")
参数格式 = re.compile(r"^([a-z_][a-z0-9_]*):(bool|int|float|str)$")


def 定位仓库(指定路径: str | None) -> Path:
    起点 = []
    if 指定路径:
        起点.append(Path(指定路径).expanduser().resolve())
    起点.extend([Path.cwd().resolve(), Path(__file__).resolve()])
    已检查: set[Path] = set()
    for 当前 in 起点:
        目录 = 当前 if 当前.is_dir() else 当前.parent
        for 候选 in (目录, *目录.parents):
            if 候选 in 已检查:
                continue
            已检查.add(候选)
            if (候选 / "device_templates_actions.csv").is_file() and (候选 / "packages").is_dir():
                return 候选
    raise FileNotFoundError("找不到同时包含 device_templates_actions.csv 和 packages/ 的仓库，请传入 --repo。")


def 读取标准(仓库: Path) -> tuple[list[dict[str, str]], list[str]]:
    with (仓库 / "device_templates_actions.csv").open(newline="", encoding="utf-8-sig") as 文件:
        读取器 = csv.DictReader(文件)
        表头 = 读取器.fieldnames or []
        数据 = [{键: (值 or "").strip() for 键, 值 in 行.items()} for 行 in 读取器]
    return 数据, 表头


def 按设备分组(数据: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    分组: dict[str, list[dict[str, str]]] = defaultdict(list)
    for 行 in 数据:
        分组[行.get("device_id", "")].append(行)
    return dict(分组)


def 搜索设备(数据: list[dict[str, str]], 关键词: str) -> list[dict[str, object]]:
    关键词 = 关键词.casefold()
    结果 = []
    for 设备编号, 行列表 in 按设备分组(数据).items():
        类别 = 行列表[0].get("设备大类", "")
        匹配接口 = sorted({
            行["英文名"] for 行 in 行列表
            if 关键词 in " ".join(行.get(列, "") for 列 in 字段).casefold()
        })
        if 关键词 in 设备编号.casefold() or 关键词 in 类别.casefold() or 匹配接口:
            结果.append({"device_id": 设备编号, "设备大类": 类别, "接口数": len(行列表), "匹配接口": 匹配接口[:8]})
    return sorted(结果, key=lambda 项: (str(项["设备大类"]), str(项["device_id"])))


def 显示设备(设备编号: str, 行列表: list[dict[str, str]], 输出JSON: bool) -> None:
    if 输出JSON:
        print(json.dumps(行列表, ensure_ascii=False, indent=2))
        return
    print(f"{行列表[0]['设备大类']} ({设备编号}) — {len(行列表)} 个接口")
    for 类型, 标题 in (("action", "动作"), ("property", "状态属性")):
        接口 = [行 for 行 in 行列表 if 行["类型"] == 类型]
        if not 接口:
            continue
        print(f"\n{标题}:")
        for 行 in 接口:
            参数 = 行["参数(名:类型)"] or "-"
            节点 = 行["PLC节点"] or "-"
            print(f"  {行['英文名']:<38} {参数:<24} {行['中文描述']}  [PLC: {节点}]")


def 校验CSV(数据: list[dict[str, str]], 表头: list[str]) -> tuple[list[str], list[str]]:
    错误: list[str] = []
    警告: list[str] = []
    缺少字段 = [列 for 列 in 字段 if 列 not in 表头]
    if 缺少字段:
        return [f"CSV 缺少字段: {', '.join(缺少字段)}"], 警告

    已有接口: set[tuple[str, str, str]] = set()
    类别映射: dict[str, set[str]] = defaultdict(set)
    for 行号, 行 in enumerate(数据, start=2):
        设备编号, 类型, 名称 = 行["device_id"], 行["类型"], 行["英文名"]
        参数, 节点, 模式 = 行["参数(名:类型)"], 行["PLC节点"], 行["交互模式"]
        前缀 = f"第 {行号} 行 ({设备编号 or '?'}:{名称 or '?'})"
        if not 标识符格式.fullmatch(设备编号):
            错误.append(f"{前缀}: device_id 不是 snake_case 标识符")
        if 类型 not in {"action", "property"}:
            错误.append(f"{前缀}: 类型必须是 action 或 property")
        if not 标识符格式.fullmatch(名称):
            错误.append(f"{前缀}: 英文名不是 snake_case 标识符")
        if not 行["设备大类"] or not 行["中文描述"]:
            错误.append(f"{前缀}: 设备大类和中文描述不能为空")
        类别映射[设备编号].add(行["设备大类"])
        接口键 = (设备编号, 类型, 名称)
        if 接口键 in 已有接口:
            错误.append(f"{前缀}: 接口重复 {类型}:{名称}")
        已有接口.add(接口键)

        if 类型 == "property":
            if 参数 not in 基础类型:
                错误.append(f"{前缀}: 状态属性类型必须属于 {sorted(基础类型)}")
            预期模式 = "读状态"
        else:
            if 参数 and not 参数格式.fullmatch(参数):
                错误.append(f"{前缀}: 动作参数必须为空或采用 name:type")
            预期模式 = "写设定值" if 参数 else "写触发→等完成→复位"
        if 模式 != 预期模式:
            错误.append(f"{前缀}: 交互模式应为 {预期模式}")
        if not 节点:
            警告.append(f"{前缀}: PLC节点为空")
        if 类型 == "action" and not 参数 and "/" not in 节点:
            警告.append(f"{前缀}: 触发动作的 PLC节点缺少触发/完成分隔符")

    for 设备编号, 类别 in 类别映射.items():
        if len(类别) > 1:
            错误.append(f"{设备编号}: 同一 device_id 使用了多个设备大类: {sorted(类别)}")
    if not 数据:
        错误.append("CSV 没有数据行")
    return 错误, 警告


def 注解文本(注解: ast.expr | None) -> str:
    return ast.unparse(注解) if 注解 is not None else ""


def 装饰器名称(装饰器: ast.expr) -> str:
    目标 = 装饰器.func if isinstance(装饰器, ast.Call) else 装饰器
    if isinstance(目标, ast.Name):
        return 目标.id
    if isinstance(目标, ast.Attribute):
        return 目标.attr
    return ""


def 解析代码接口(路径: Path) -> tuple[dict[str, tuple[str, str]], dict[str, str], str | None]:
    try:
        语法树 = ast.parse(路径.read_text(encoding="utf-8"), filename=str(路径))
    except (OSError, SyntaxError) as 异常:
        return {}, {}, str(异常)
    类定义 = next((节点 for 节点 in 语法树.body if isinstance(节点, ast.ClassDef)), None)
    if 类定义 is None:
        return {}, {}, "未找到类定义"
    动作: dict[str, tuple[str, str]] = {}
    属性: dict[str, str] = {}
    for 节点 in 类定义.body:
        if not isinstance(节点, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        装饰器 = {装饰器名称(项) for 项 in 节点.decorator_list}
        if "action" in 装饰器:
            参数 = [项 for 项 in 节点.args.args if 项.arg != "self"]
            if len(参数) > 1:
                动作[节点.name] = ("<多个参数>", "<多个参数>")
            elif 参数:
                动作[节点.name] = (参数[0].arg, 注解文本(参数[0].annotation))
            else:
                动作[节点.name] = ("", "")
        if "property" in 装饰器:
            属性[节点.name] = 注解文本(节点.returns)
    return 动作, 属性, None


def 预期接口(行列表: list[dict[str, str]]) -> tuple[dict[str, tuple[str, str]], dict[str, str]]:
    动作: dict[str, tuple[str, str]] = {}
    属性: dict[str, str] = {}
    for 行 in 行列表:
        if 行["类型"] == "action":
            参数 = 行["参数(名:类型)"]
            动作[行["英文名"]] = tuple(参数.split(":", 1)) if 参数 else ("", "")
        elif 行["类型"] == "property":
            属性[行["英文名"]] = 行["参数(名:类型)"]
    return 动作, 属性


def 比较接口(标签: str, 路径: Path, 预期动作: dict, 预期属性: dict) -> list[str]:
    if not 路径.is_file():
        return [f"{标签}: 文件不存在 {路径}"]
    动作, 属性, 解析错误 = 解析代码接口(路径)
    if 解析错误:
        return [f"{标签}: 无法解析 {路径}: {解析错误}"]
    错误 = []
    for 名称, 实际, 预期 in (("动作", 动作, 预期动作), ("状态属性", 属性, 预期属性)):
        缺少 = sorted(set(预期) - set(实际))
        多余 = sorted(set(实际) - set(预期))
        变化 = sorted(键 for 键 in set(实际) & set(预期) if 实际[键] != 预期[键])
        if 缺少:
            错误.append(f"{标签}: 缺少{名称}: {缺少}")
        if 多余:
            错误.append(f"{标签}: 多余{名称}: {多余}")
        for 键 in 变化:
            错误.append(f"{标签}: {名称} {键} 应为 {预期[键]}，实际为 {实际[键]}")
    return 错误


def 校验代码(仓库: Path, 数据: list[dict[str, str]], 目标设备: str) -> list[str]:
    设备 = 按设备分组(数据)
    if 目标设备 != "all":
        if 目标设备 not in 设备:
            return [f"未找到要检查的 device_id: {目标设备}"]
        设备 = {目标设备: 设备[目标设备]}
    错误: list[str] = []
    for 设备编号, 行列表 in 设备.items():
        预期动作, 预期属性 = 预期接口(行列表)
        包目录 = 仓库 / "packages" / 设备编号 / 设备编号
        错误.extend(比较接口(f"{设备编号} 标准模板", 包目录 / f"{设备编号}.py", 预期动作, 预期属性))
        错误.extend(比较接口(f"{设备编号} PLC驱动", 包目录 / f"{设备编号}_plc.py", 预期动作, 预期属性))
    return 错误


def 参数解析器() -> argparse.ArgumentParser:
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument("--repo", help="Uni-Lab 设备包管理仓库路径")
    操作 = 解析器.add_mutually_exclusive_group(required=True)
    操作.add_argument("--search", metavar="关键词", help="按类别、ID、接口或描述搜索")
    操作.add_argument("--device-id", help="显示一个设备大类的完整接口")
    操作.add_argument("--list", action="store_true", help="列出全部设备大类")
    操作.add_argument("--validate", action="store_true", help="校验标准 CSV")
    解析器.add_argument("--check-code", metavar="DEVICE_ID", help="同时检查指定设备代码；全量检查传 all")
    解析器.add_argument("--json", action="store_true", help="以 JSON 输出查询结果")
    return 解析器


def 主函数() -> int:
    参数 = 参数解析器().parse_args()
    try:
        仓库 = 定位仓库(参数.repo)
        数据, 表头 = 读取标准(仓库)
    except (FileNotFoundError, OSError, csv.Error) as 异常:
        print(f"错误: {异常}", file=sys.stderr)
        return 2
    设备 = 按设备分组(数据)

    if 参数.device_id:
        if 参数.device_id not in 设备:
            print(f"未找到 device_id: {参数.device_id}", file=sys.stderr)
            return 1
        显示设备(参数.device_id, 设备[参数.device_id], 参数.json)
        return 0
    if 参数.search is not None:
        结果 = 搜索设备(数据, 参数.search)
        if 参数.json:
            print(json.dumps(结果, ensure_ascii=False, indent=2))
        else:
            for 项 in 结果:
                匹配 = f"；匹配接口: {', '.join(项['匹配接口'])}" if 项["匹配接口"] else ""
                print(f"{项['设备大类']:<24} {项['device_id']:<42} {项['接口数']:>3} 个接口{匹配}")
        return 0 if 结果 else 1
    if 参数.list:
        结果 = [{"device_id": 编号, "设备大类": 行[0]["设备大类"], "接口数": len(行)} for 编号, 行 in sorted(设备.items())]
        if 参数.json:
            print(json.dumps(结果, ensure_ascii=False, indent=2))
        else:
            for 项 in 结果:
                print(f"{项['设备大类']:<24} {项['device_id']:<42} {项['接口数']:>3} 个接口")
            print(f"\n共 {len(结果)} 个设备大类，{len(数据)} 条接口定义。")
        return 0

    错误, 警告 = 校验CSV(数据, 表头)
    if 参数.check_code and not 错误:
        错误.extend(校验代码(仓库, 数据, 参数.check_code))
    for 内容 in 警告:
        print(f"警告: {内容}")
    for 内容 in 错误:
        print(f"错误: {内容}")
    print(f"校验完成：{len(设备)} 个设备大类，{len(数据)} 条接口定义，{len(错误)} 个错误，{len(警告)} 个警告。")
    return 1 if 错误 else 0


if __name__ == "__main__":
    raise SystemExit(主函数())
