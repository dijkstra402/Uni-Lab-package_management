"""
PLC(OPC UA) 交互驱动生成器

读取 device_templates_actions.csv，为每个设备大类在其包目录下生成
    packages/<id>/<id>/<id>_plc.py
生成的类继承 OpcUaClientWithSubscription，把标准动作/属性映射为 PLC 节点读写，
交互范式对齐 AI4C.py：
    - 触发类动作(无参数)：写 <X>_Trigger=True → 等 <X>_Complete=True → 复位 → 等 <X>_Complete=False
    - 设定类动作(set_*，单参数)：写 <Param>_Setpoint = 值
    - 状态属性：读对应状态节点

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
    """snake_case → Pascal_Case 的 PLC 节点命名（保留下划线分段）。"""
    return "_".join(seg.capitalize() for seg in name.split("_"))


def class_name(device_id: str) -> str:
    return "".join(seg.capitalize() for seg in device_id.split("_"))


def plc_node(row_type: str, en: str, param: str):
    """返回 (节点描述, 交互模式)。param 形如 'temperature:float' 或空。"""
    if row_type == "property":
        return pascal(en), "读状态"
    if param:  # set_* 设定类动作
        pname = param.split(":")[0]
        return f"{pascal(pname)}_Setpoint", "写设定值"
    # 触发类动作
    p = pascal(en)
    return f"{p}_Trigger / {p}_Complete", "写触发→等完成→复位"


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def group_by_device(rows):
    devices = OrderedDict()
    for r in rows:
        did = r["device_id"]
        devices.setdefault(did, {"category": r["设备大类"], "actions": [], "properties": []})
        item = {"en": r["英文名"], "desc": r["中文描述"], "param": r["参数(名:类型)"].strip()}
        if r["类型"] == "action":
            devices[did]["actions"].append(item)
        else:
            item["ptype"] = r["参数(名:类型)"].strip() or "str"
            devices[did]["properties"].append(item)
    return devices


def render_action(a):
    en, desc, param = a["en"], a["desc"], a["param"]
    if param:  # 设定类：写设定值
        pname, ptype = param.split(":")
        default = PY_DEFAULT.get(ptype, "None")
        node = f"{pascal(pname)}_Setpoint"
        return f'''    @action(description="{desc}")
    def {en}(self, {pname}: {ptype} = {default}) -> Dict[str, Any]:
        """{desc}：写入设定值节点 {node}。"""
        self.set_node_value("{node}", {pname})
        return {{"success": True, "message": "{desc}已下发", "{pname}": {pname}}}
'''
    # 触发类：写触发→等完成→复位
    p = pascal(en)
    return f'''    @action(description="{desc}")
    def {en}(self) -> Dict[str, Any]:
        """{desc}：写 {p}_Trigger 触发，等待 {p}_Complete 完成后复位。"""
        logger.info("{desc}...")
        self.set_node_value("{p}_Trigger", True)
        if not self._wait_until_true("{p}_Complete", description="{desc}完成"):
            raise ValueError("{desc}失败：动作未完成")
        self.set_node_value("{p}_Trigger", False)
        if not self._wait_until_false("{p}_Complete", description="{desc}完成复位"):
            raise ValueError("{desc}失败：完成状态复位超时")
        return {{"success": True, "message": "{desc}完成"}}
'''


def render_property(p):
    en, desc, ptype = p["en"], p["desc"], p["ptype"]
    default = PY_DEFAULT.get(ptype, '""')
    node = pascal(en)
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
- 触发类动作：写 <X>_Trigger=True → 等 <X>_Complete=True → 复位 → 等 <X>_Complete=False
- 设定类动作：写 <Param>_Setpoint = 值
- 状态属性：  读对应状态节点
节点均可在设备接入时通过 CSV(NodeId 映射) 注册。
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
    """在原 CSV 基础上追加 PLC节点 / 交互模式 两列。"""
    fields = ["设备大类", "device_id", "类型", "英文名", "中文描述", "参数(名:类型)", "PLC节点", "交互模式"]
    for r in rows:
        node, mode = plc_node(r["类型"], r["英文名"], r["参数(名:类型)"].strip())
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
