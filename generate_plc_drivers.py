"""
PLC(OPC UA) 交互驱动生成器

读取 device_templates_actions.csv，为每个设备大类在其包目录下生成
    packages/<id>/<id>/<id>_plc.py
生成的类继承 OpcUaClientWithSubscription，把标准动作/属性映射为 PLC 节点读写，
交互范式与 OPCUA 通信协议一致，节点使用中文命名：
    - 触发类动作(无参数)：写 <X>触发=True → 等 <X>完成=True → 复位 → 等 <X>完成=False
    - 设定类动作(set_*，单参数)：写 <X>设置 = 值
    - 状态属性：读对应中文命名的状态节点（如 故障 / 设备就绪 / 温度超限报警）

同时把 PLC 方案(节点、交互模式)回写到 device_templates_actions.csv。
"""

import csv
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT, "device_templates_actions.csv")
PKG_DIR = os.path.join(ROOT, "packages")

PY_DEFAULT = {"float": "0.0", "int": "0", "str": '""', "bool": "False"}


def pascal(name: str) -> str:
    """snake_case → Pascal_Case（仅用于 Python 类名等英文场景）。"""
    return "_".join(seg.capitalize() for seg in name.split("_"))


def class_name(device_id: str) -> str:
    return "".join(seg.capitalize() for seg in device_id.split("_"))


def _strip_paren(s: str) -> str:
    """剥除中文/英文括号及其内容（用于 PLC 节点派生时清理描述）。"""
    if not s:
        return s
    cuts = [i for i in (s.find("("), s.find("（")) if i >= 0]
    if cuts:
        return s[: min(cuts)].rstrip()
    return s


def plc_node(row_type: str, en: str, param: str, zh: str = "", mode: str = ""):
    """
    返回 (PLC 节点, 交互模式)。

    PLC 节点使用与 OPCUA 通信协议一致的中文命名：
    - 属性(property): 直接用中文描述作为节点名
    - 触发类动作(action, 无 param): 节点表示为 "<X>触发 / <X>完成"
    - 设定类动作(action, 有 param): 节点为 "<X>设置"

    参数中 zh、mode 优先于 en/param 用于派生；若 zh 为空则回退到英文名。
    """
    core = _strip_paren(zh) if zh else en
    if row_type == "property":
        return (zh or en), "读状态"
    if param:  # set_* 设定类动作
        if core.endswith("设置"):
            node = core
        elif core.startswith("设置") and len(core) > 2:
            node = core[2:] + "设置"
        else:
            node = (core or en) + "设置"
        return node, "写设定值"
    # 触发类动作
    if not core:
        core = en
    return f"{core}触发 / {core}完成", "写触发→等完成→复位"


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def group_by_device(rows):
    devices = OrderedDict()
    for r in rows:
        did = r["device_id"]
        devices.setdefault(did, {"category": r["设备大类"], "actions": [], "properties": []})
        item = {
            "en": r["英文名"],
            "desc": r["中文描述"],
            "param": r["参数(名:类型)"].strip(),
            "node": (r.get("PLC节点") or "").strip(),
            "mode": (r.get("交互模式") or "").strip(),
        }
        if r["类型"] == "action":
            devices[did]["actions"].append(item)
        else:
            item["ptype"] = r["参数(名:类型)"].strip() or "str"
            devices[did]["properties"].append(item)
    return devices


def _split_trigger_complete(node: str):
    """把 "X触发 / X完成" 拆成 (trigger_node, complete_node)。回退兼容英文旧格式。"""
    if node and "/" in node:
        parts = [p.strip() for p in node.split("/", 1)]
        if len(parts) == 2 and parts[0] and parts[1]:
            return parts[0], parts[1]
    # 回退：按中文 "X触发"/"X完成" 或英文 "X_Trigger"/"X_Complete" 派生
    core = node
    for suf in ("触发", "完成", "_Trigger", "_Complete"):
        if core.endswith(suf):
            core = core[: -len(suf)]
            break
    if core:
        return f"{core}触发", f"{core}完成"
    return "触发", "完成"


def render_action(a):
    en, desc, param = a["en"], a["desc"], a["param"]
    csv_node = a.get("node", "")
    csv_mode = a.get("mode", "")
    if param:  # 设定类：写设定值
        pname, ptype = param.split(":")
        default = PY_DEFAULT.get(ptype, "None")
        node, _ = plc_node("action", en, param, zh=desc, mode=csv_mode)
        # 若 CSV 明确给出中文节点，则优先采用
        if csv_node and "/" not in csv_node:
            node = csv_node
        return f'''    @action(description="{desc}")
    def {en}(self, {pname}: {ptype} = {default}) -> Dict[str, Any]:
        """{desc}：写入设定值节点 {node}。"""
        self.set_node_value("{node}", {pname})
        return {{"success": True, "message": "{desc}已下发", "{pname}": {pname}}}
'''
    # 触发类：写触发→等完成→复位
    if csv_node and "/" in csv_node:
        trig_node, done_node = _split_trigger_complete(csv_node)
    else:
        derived, _ = plc_node("action", en, "", zh=desc, mode=csv_mode)
        trig_node, done_node = _split_trigger_complete(derived)
    return f'''    @action(description="{desc}")
    def {en}(self) -> Dict[str, Any]:
        """{desc}：写 {trig_node} 触发，等待 {done_node} 完成后复位。"""
        logger.info("{desc}...")
        self.set_node_value("{trig_node}", True)
        if not self._wait_until_true("{done_node}", description="{desc}完成"):
            raise ValueError("{desc}失败：动作未完成")
        self.set_node_value("{trig_node}", False)
        if not self._wait_until_false("{done_node}", description="{desc}完成复位"):
            raise ValueError("{desc}失败：完成状态复位超时")
        return {{"success": True, "message": "{desc}完成"}}
'''


def render_property(p):
    en, desc, ptype = p["en"], p["desc"], p["ptype"]
    default = PY_DEFAULT.get(ptype, '""')
    node = p.get("node") or desc or en
    return f'''    @property
    @topic_config()
    def {en}(self) -> {ptype}:
        """{desc}（读节点 {node}）。"""
        v = self.get_node_value("{node}")
        return v if v is not None else {default}
'''


def render_file(device_id, info):
    cat = info["category"]
    cls = class_name(device_id) + "PLC"
    actions = "\n".join(render_action(a) for a in info["actions"])
    props = "\n".join(render_property(p) for p in info["properties"])
    return f'''"""
{cat} — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「{cat}」标准动作/属性映射为 PLC 节点读写：
- 触发类动作：写 <X>触发=True → 等 <X>完成=True → 复位 → 等 <X>完成=False
- 设定类动作：写 <X>设置 = 值
- 状态属性：  读对应中文命名的状态节点
节点使用与 OPCUA 通信协议一致的中文命名，通过 CSV(NodeId 映射) 在设备接入时注册。
"""

import time
from typing import Any, Dict

from unilabos.registry.decorators import device, action, topic_config
from unilabos.utils.log import logger

from base_opcua_client import OpcUaClientWithSubscription


@device(
    id="{device_id}_plc",
    category=["{cat}"],
    description="{cat} PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="{cat}(PLC)",
)
class {cls}(OpcUaClientWithSubscription):

    def __init__(
        self,
        url: str,
        csv_path: str = None,
        username: str = None,
        password: str = None,
        use_subscription: bool = True,
        cache_timeout: float = 5.0,
        subscription_interval: int = 500,
        *args,
        **kwargs,
    ):
        super().__init__(
            url=url,
            username=username,
            password=password,
            use_subscription=use_subscription,
            cache_timeout=cache_timeout,
            subscription_interval=subscription_interval,
            *args,
            **kwargs,
        )
        if csv_path:
            self.load_nodes_from_csv(csv_path)

{actions}
{props}
    def _wait_until_true(self, node_name: str, timeout: float = 300.0,
                         interval: float = 0.2, description: str = None) -> bool:
        """等待布尔节点变为 True（强制从服务器读取，避免订阅缓存过期）。"""
        desc = description or node_name
        start = time.time()
        while True:
            if self.get_node_value(node_name, force_read=True):
                return True
            if time.time() - start >= timeout:
                logger.error(f"等待 {{desc}} 超时（{{timeout}}秒，节点 {{node_name}}）")
                return False
            time.sleep(interval)

    def _wait_until_false(self, node_name: str, timeout: float = 300.0,
                          interval: float = 0.2, description: str = None) -> bool:
        """等待布尔节点变为 False（强制从服务器读取）。"""
        desc = description or node_name
        start = time.time()
        while True:
            if not self.get_node_value(node_name, force_read=True):
                return True
            if time.time() - start >= timeout:
                logger.error(f"等待 {{desc}} 超时（{{timeout}}秒，节点 {{node_name}}）")
                return False
            time.sleep(interval)
'''


def write_drivers(devices):
    written = []
    for did, info in devices.items():
        pkg = os.path.join(PKG_DIR, did, did)
        if not os.path.isdir(pkg):
            print(f"跳过（无包目录）: {did}")
            continue
        out = os.path.join(pkg, f"{did}_plc.py")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render_file(did, info))
        written.append(out)
    return written


def rewrite_csv(rows):
    """
    在原 CSV 基础上刷新 PLC节点 / 交互模式 两列。

    PLC 节点采用与 OPCUA 通信协议一致的中文命名（参见 plc_node()）。
    若 CSV 中已存在合规的中文节点，则保持不变；否则按中文描述派生。
    """
    fields = ["设备大类", "device_id", "类型", "英文名", "中文描述", "参数(名:类型)", "PLC节点", "交互模式"]
    for r in rows:
        node, mode = plc_node(
            r["类型"],
            r["英文名"],
            r["参数(名:类型)"].strip(),
            zh=r.get("中文描述", ""),
            mode=r.get("交互模式", ""),
        )
        r["PLC节点"] = node
        r["交互模式"] = mode
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    rows = load_rows()
    devices = group_by_device(rows)
    written = write_drivers(devices)
    rewrite_csv(rows)
    print(f"生成 {len(written)} 个 _plc.py，覆盖 {len(devices)} 个设备大类；CSV 已补充 PLC 方案列。")


if __name__ == "__main__":
    main()
