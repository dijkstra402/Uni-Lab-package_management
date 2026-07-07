"""
移液器 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「移液器」标准动作/属性映射为 PLC 节点读写：
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
    id="pipette_plc",
    category=["移液器"],
    description="移液器 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="移液器(PLC)",
)
class PipettePLC(OpcUaClientWithSubscription):

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

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """设置运行模式：写入设定值节点 Mode_Setpoint。"""
        self.set_node_value("Mode_Setpoint", mode)
        return {"success": True, "message": "设置运行模式已下发", "mode": mode}

    @action(description="设置吸液体积")
    def set_aspirate_volume(self, aspirate_volume: float = 0.0) -> Dict[str, Any]:
        """设置吸液体积：写入设定值节点 Aspirate_Volume_Setpoint。"""
        self.set_node_value("Aspirate_Volume_Setpoint", aspirate_volume)
        return {"success": True, "message": "设置吸液体积已下发", "aspirate_volume": aspirate_volume}

    @action(description="设置排液体积")
    def set_dispense_volume(self, dispense_volume: float = 0.0) -> Dict[str, Any]:
        """设置排液体积：写入设定值节点 Dispense_Volume_Setpoint。"""
        self.set_node_value("Dispense_Volume_Setpoint", dispense_volume)
        return {"success": True, "message": "设置排液体积已下发", "dispense_volume": dispense_volume}

    @action(description="设置吸液速度")
    def set_aspirate_speed(self, aspirate_speed: float = 0.0) -> Dict[str, Any]:
        """设置吸液速度：写入设定值节点 Aspirate_Speed_Setpoint。"""
        self.set_node_value("Aspirate_Speed_Setpoint", aspirate_speed)
        return {"success": True, "message": "设置吸液速度已下发", "aspirate_speed": aspirate_speed}

    @action(description="设置排液速度")
    def set_dispense_speed(self, dispense_speed: float = 0.0) -> Dict[str, Any]:
        """设置排液速度：写入设定值节点 Dispense_Speed_Setpoint。"""
        self.set_node_value("Dispense_Speed_Setpoint", dispense_speed)
        return {"success": True, "message": "设置排液速度已下发", "dispense_speed": dispense_speed}

    @action(description="设置枪头位置")
    def set_tip_position(self, tip_position: float = 0.0) -> Dict[str, Any]:
        """设置枪头位置：写入设定值节点 Tip_Position_Setpoint。"""
        self.set_node_value("Tip_Position_Setpoint", tip_position)
        return {"success": True, "message": "设置枪头位置已下发", "tip_position": tip_position}

    @action(description="吸液")
    def draw_liquid(self) -> Dict[str, Any]:
        """吸液：写 Draw_Liquid_Trigger 触发，等待 Draw_Liquid_Complete 完成后复位。"""
        logger.info("吸液...")
        self.set_node_value("Draw_Liquid_Trigger", True)
        if not self._wait_until_true("Draw_Liquid_Complete", description="吸液完成"):
            raise ValueError("吸液失败：动作未完成")
        self.set_node_value("Draw_Liquid_Trigger", False)
        if not self._wait_until_false("Draw_Liquid_Complete", description="吸液完成复位"):
            raise ValueError("吸液失败：完成状态复位超时")
        return {"success": True, "message": "吸液完成"}

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

    @action(description="枪头安装")
    def attach_tip(self) -> Dict[str, Any]:
        """枪头安装：写 Attach_Tip_Trigger 触发，等待 Attach_Tip_Complete 完成后复位。"""
        logger.info("枪头安装...")
        self.set_node_value("Attach_Tip_Trigger", True)
        if not self._wait_until_true("Attach_Tip_Complete", description="枪头安装完成"):
            raise ValueError("枪头安装失败：动作未完成")
        self.set_node_value("Attach_Tip_Trigger", False)
        if not self._wait_until_false("Attach_Tip_Complete", description="枪头安装完成复位"):
            raise ValueError("枪头安装失败：完成状态复位超时")
        return {"success": True, "message": "枪头安装完成"}

    @action(description="枪头丢弃")
    def discard_tip(self) -> Dict[str, Any]:
        """枪头丢弃：写 Discard_Tip_Trigger 触发，等待 Discard_Tip_Complete 完成后复位。"""
        logger.info("枪头丢弃...")
        self.set_node_value("Discard_Tip_Trigger", True)
        if not self._wait_until_true("Discard_Tip_Complete", description="枪头丢弃完成"):
            raise ValueError("枪头丢弃失败：动作未完成")
        self.set_node_value("Discard_Tip_Trigger", False)
        if not self._wait_until_false("Discard_Tip_Complete", description="枪头丢弃完成复位"):
            raise ValueError("枪头丢弃失败：完成状态复位超时")
        return {"success": True, "message": "枪头丢弃完成"}

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
    def device_ready(self) -> bool:
        """设备就绪（读节点 Device_Ready）。"""
        v = self.get_node_value("Device_Ready")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_aspirate_volume(self) -> float:
        """实际吸液体积（读节点 Current_Aspirate_Volume）。"""
        v = self.get_node_value("Current_Aspirate_Volume")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_dispense_volume(self) -> float:
        """实际排液体积（读节点 Current_Dispense_Volume）。"""
        v = self.get_node_value("Current_Dispense_Volume")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_tip_position(self) -> float:
        """实际枪头位置（读节点 Current_Tip_Position）。"""
        v = self.get_node_value("Current_Tip_Position")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def tip_state(self) -> int:
        """枪头状态（读节点 Tip_State）。"""
        v = self.get_node_value("Tip_State")
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
