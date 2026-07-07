"""
柱塞泵 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「柱塞泵」标准动作/属性映射为 PLC 节点读写：
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
    id="plunger_pump_plc",
    category=["柱塞泵"],
    description="柱塞泵 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="柱塞泵(PLC)",
)
class PlungerPumpPLC(OpcUaClientWithSubscription):

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

    @action(description="设置往复频率")
    def set_reciprocating_frequency(self, reciprocating_frequency: float = 0.0) -> Dict[str, Any]:
        """设置往复频率：写入设定值节点 Reciprocating_Frequency_Setpoint。"""
        self.set_node_value("Reciprocating_Frequency_Setpoint", reciprocating_frequency)
        return {"success": True, "message": "设置往复频率已下发", "reciprocating_frequency": reciprocating_frequency}

    @action(description="设置行程长度")
    def set_stroke_length(self, stroke_length: int = 0) -> Dict[str, Any]:
        """设置行程长度：写入设定值节点 Stroke_Length_Setpoint。"""
        self.set_node_value("Stroke_Length_Setpoint", stroke_length)
        return {"success": True, "message": "设置行程长度已下发", "stroke_length": stroke_length}

    @action(description="设置冲程数")
    def set_stroke_count(self, stroke_count: int = 0) -> Dict[str, Any]:
        """设置冲程数：写入设定值节点 Stroke_Count_Setpoint。"""
        self.set_node_value("Stroke_Count_Setpoint", stroke_count)
        return {"success": True, "message": "设置冲程数已下发", "stroke_count": stroke_count}

    @action(description="泵送")
    def pump(self) -> Dict[str, Any]:
        """泵送：写 Pump_Trigger 触发，等待 Pump_Complete 完成后复位。"""
        logger.info("泵送...")
        self.set_node_value("Pump_Trigger", True)
        if not self._wait_until_true("Pump_Complete", description="泵送完成"):
            raise ValueError("泵送失败：动作未完成")
        self.set_node_value("Pump_Trigger", False)
        if not self._wait_until_false("Pump_Complete", description="泵送完成复位"):
            raise ValueError("泵送失败：完成状态复位超时")
        return {"success": True, "message": "泵送完成"}

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
