"""
注射泵 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「注射泵」标准动作/属性映射为 PLC 节点读写：
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
    id="syringe_pump_plc",
    category=["合成制备仪器与设备", "实验泵", "注射泵"],
    description="注射泵 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="注射泵(PLC)",
)
class SyringePumpPLC(OpcUaClientWithSubscription):

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

    @action(description="设置绝对位置")
    def set_position(self, position: float = 0.0) -> Dict[str, Any]:
        """设置绝对位置：写入设定值节点 Position_Setpoint。"""
        self.set_node_value("Position_Setpoint", position)
        return {"success": True, "message": "设置绝对位置已下发", "position": position}

    @action(description="设置抽液位置")
    def set_aspirate_position(self, aspirate_position: float = 0.0) -> Dict[str, Any]:
        """设置抽液位置：写入设定值节点 Aspirate_Position_Setpoint。"""
        self.set_node_value("Aspirate_Position_Setpoint", aspirate_position)
        return {"success": True, "message": "设置抽液位置已下发", "aspirate_position": aspirate_position}

    @action(description="设置排液位置")
    def set_dispense_position(self, dispense_position: float = 0.0) -> Dict[str, Any]:
        """设置排液位置：写入设定值节点 Dispense_Position_Setpoint。"""
        self.set_node_value("Dispense_Position_Setpoint", dispense_position)
        return {"success": True, "message": "设置排液位置已下发", "dispense_position": dispense_position}

    @action(description="绝对控制")
    def move_absolute(self) -> Dict[str, Any]:
        """绝对控制：写 Move_Absolute_Trigger 触发，等待 Move_Absolute_Complete 完成后复位。"""
        logger.info("绝对控制...")
        self.set_node_value("Move_Absolute_Trigger", True)
        if not self._wait_until_true("Move_Absolute_Complete", description="绝对控制完成"):
            raise ValueError("绝对控制失败：动作未完成")
        self.set_node_value("Move_Absolute_Trigger", False)
        if not self._wait_until_false("Move_Absolute_Complete", description="绝对控制完成复位"):
            raise ValueError("绝对控制失败：完成状态复位超时")
        return {"success": True, "message": "绝对控制完成"}

    @action(description="抽液")
    def aspirate(self) -> Dict[str, Any]:
        """抽液：写 Aspirate_Trigger 触发，等待 Aspirate_Complete 完成后复位。"""
        logger.info("抽液...")
        self.set_node_value("Aspirate_Trigger", True)
        if not self._wait_until_true("Aspirate_Complete", description="抽液完成"):
            raise ValueError("抽液失败：动作未完成")
        self.set_node_value("Aspirate_Trigger", False)
        if not self._wait_until_false("Aspirate_Complete", description="抽液完成复位"):
            raise ValueError("抽液失败：完成状态复位超时")
        return {"success": True, "message": "抽液完成"}

    @action(description="排液")
    def dispense(self) -> Dict[str, Any]:
        """排液：写 Dispense_Trigger 触发，等待 Dispense_Complete 完成后复位。"""
        logger.info("排液...")
        self.set_node_value("Dispense_Trigger", True)
        if not self._wait_until_true("Dispense_Complete", description="排液完成"):
            raise ValueError("排液失败：动作未完成")
        self.set_node_value("Dispense_Trigger", False)
        if not self._wait_until_false("Dispense_Complete", description="排液完成复位"):
            raise ValueError("排液失败：完成状态复位超时")
        return {"success": True, "message": "排液完成"}

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
    def current_position(self) -> float:
        """当前位置显示（读节点 Current_Position）。"""
        v = self.get_node_value("Current_Position")
        return v if v is not None else 0.0

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
