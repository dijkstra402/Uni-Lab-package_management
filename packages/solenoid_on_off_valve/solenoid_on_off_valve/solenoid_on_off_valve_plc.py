"""
电磁开关阀 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「电磁开关阀」标准动作/属性映射为 PLC 节点读写：
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
    id="solenoid_on_off_valve_plc",
    category=["合成制备仪器与设备", "实验阀与气路设备", "电磁开关阀"],
    description="电磁开关阀 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="电磁开关阀(PLC)",
)
class SolenoidOnOffValvePLC(OpcUaClientWithSubscription):

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

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化：写 Initialize_Trigger 触发，等待 Initialize_Complete 完成后复位。"""
        logger.info("初始化...")
        self.set_node_value("Initialize_Trigger", True)
        if not self._wait_until_true("Initialize_Complete", description="初始化完成"):
            raise ValueError("初始化失败：动作未完成")
        self.set_node_value("Initialize_Trigger", False)
        if not self._wait_until_false("Initialize_Complete", description="初始化完成复位"):
            raise ValueError("初始化失败：完成状态复位超时")
        return {"success": True, "message": "初始化完成"}

    @action(description="设置打开时间")
    def set_open_time(self, open_time: float = 0.0) -> Dict[str, Any]:
        """设置打开时间：写入设定值节点 Open_Time_Setpoint。"""
        self.set_node_value("Open_Time_Setpoint", open_time)
        return {"success": True, "message": "设置打开时间已下发", "open_time": open_time}

    @action(description="设置关闭时间")
    def set_close_time(self, close_time: float = 0.0) -> Dict[str, Any]:
        """设置关闭时间：写入设定值节点 Close_Time_Setpoint。"""
        self.set_node_value("Close_Time_Setpoint", close_time)
        return {"success": True, "message": "设置关闭时间已下发", "close_time": close_time}

    @action(description="打开")
    def open(self) -> Dict[str, Any]:
        """打开：写 Open_Trigger 触发，等待 Open_Complete 完成后复位。"""
        logger.info("打开...")
        self.set_node_value("Open_Trigger", True)
        if not self._wait_until_true("Open_Complete", description="打开完成"):
            raise ValueError("打开失败：动作未完成")
        self.set_node_value("Open_Trigger", False)
        if not self._wait_until_false("Open_Complete", description="打开完成复位"):
            raise ValueError("打开失败：完成状态复位超时")
        return {"success": True, "message": "打开完成"}

    @action(description="关闭")
    def close(self) -> Dict[str, Any]:
        """关闭：写 Close_Trigger 触发，等待 Close_Complete 完成后复位。"""
        logger.info("关闭...")
        self.set_node_value("Close_Trigger", True)
        if not self._wait_until_true("Close_Complete", description="关闭完成"):
            raise ValueError("关闭失败：动作未完成")
        self.set_node_value("Close_Trigger", False)
        if not self._wait_until_false("Close_Complete", description="关闭完成复位"):
            raise ValueError("关闭失败：完成状态复位超时")
        return {"success": True, "message": "关闭完成"}

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态（读节点 Status）。"""
        v = self.get_node_value("Status")
        return v if v is not None else ""

    @property
    @topic_config()
    def fault(self) -> bool:
        """故障（读节点 Fault）。"""
        v = self.get_node_value("Fault")
        return v if v is not None else False

    @property
    @topic_config()
    def idle(self) -> bool:
        """空闲（读节点 Idle）。"""
        v = self.get_node_value("Idle")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_switch(self) -> bool:
        """当前开关显示（读节点 Current_Switch）。"""
        v = self.get_node_value("Current_Switch")
        return v if v is not None else False

    def _wait_until_true(self, node_name: str, timeout: float = 300.0,
                         interval: float = 0.2, description: str = None) -> bool:
        """等待布尔节点变为 True（强制从服务器读取，避免订阅缓存过期）。"""
        desc = description or node_name
        start = time.time()
        while True:
            if self.get_node_value(node_name, force_read=True):
                return True
            if time.time() - start >= timeout:
                logger.error(f"等待 {desc} 超时（{timeout}秒，节点 {node_name}）")
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
                logger.error(f"等待 {desc} 超时（{timeout}秒，节点 {node_name}）")
                return False
            time.sleep(interval)
