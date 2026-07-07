"""
投料反应站 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「投料反应站」标准动作/属性映射为 PLC 节点读写：
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
    id="charging_reaction_station_plc",
    category=["投料反应站"],
    description="投料反应站 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="投料反应站(PLC)",
)
class ChargingReactionStationPLC(OpcUaClientWithSubscription):

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

    @action(description="设置反应温度")
    def set_reaction_temperature(self, reaction_temperature: float = 0.0) -> Dict[str, Any]:
        """设置反应温度：写入设定值节点 Reaction_Temperature_Setpoint。"""
        self.set_node_value("Reaction_Temperature_Setpoint", reaction_temperature)
        return {"success": True, "message": "设置反应温度已下发", "reaction_temperature": reaction_temperature}

    @action(description="设置搅拌速度")
    def set_stir_speed(self, stir_speed: float = 0.0) -> Dict[str, Any]:
        """设置搅拌速度：写入设定值节点 Stir_Speed_Setpoint。"""
        self.set_node_value("Stir_Speed_Setpoint", stir_speed)
        return {"success": True, "message": "设置搅拌速度已下发", "stir_speed": stir_speed}

    @action(description="设置反应时间")
    def set_reaction_time(self, reaction_time: float = 0.0) -> Dict[str, Any]:
        """设置反应时间：写入设定值节点 Reaction_Time_Setpoint。"""
        self.set_node_value("Reaction_Time_Setpoint", reaction_time)
        return {"success": True, "message": "设置反应时间已下发", "reaction_time": reaction_time}

    @action(description="投料启动")
    def start_charging(self) -> Dict[str, Any]:
        """投料启动：写 Start_Charging_Trigger 触发，等待 Start_Charging_Complete 完成后复位。"""
        logger.info("投料启动...")
        self.set_node_value("Start_Charging_Trigger", True)
        if not self._wait_until_true("Start_Charging_Complete", description="投料启动完成"):
            raise ValueError("投料启动失败：动作未完成")
        self.set_node_value("Start_Charging_Trigger", False)
        if not self._wait_until_false("Start_Charging_Complete", description="投料启动完成复位"):
            raise ValueError("投料启动失败：完成状态复位超时")
        return {"success": True, "message": "投料启动完成"}

    @action(description="反应启动")
    def start_reaction(self) -> Dict[str, Any]:
        """反应启动：写 Start_Reaction_Trigger 触发，等待 Start_Reaction_Complete 完成后复位。"""
        logger.info("反应启动...")
        self.set_node_value("Start_Reaction_Trigger", True)
        if not self._wait_until_true("Start_Reaction_Complete", description="反应启动完成"):
            raise ValueError("反应启动失败：动作未完成")
        self.set_node_value("Start_Reaction_Trigger", False)
        if not self._wait_until_false("Start_Reaction_Complete", description="反应启动完成复位"):
            raise ValueError("反应启动失败：完成状态复位超时")
        return {"success": True, "message": "反应启动完成"}

    @action(description="搅拌启动")
    def start_stirring(self) -> Dict[str, Any]:
        """搅拌启动：写 Start_Stirring_Trigger 触发，等待 Start_Stirring_Complete 完成后复位。"""
        logger.info("搅拌启动...")
        self.set_node_value("Start_Stirring_Trigger", True)
        if not self._wait_until_true("Start_Stirring_Complete", description="搅拌启动完成"):
            raise ValueError("搅拌启动失败：动作未完成")
        self.set_node_value("Start_Stirring_Trigger", False)
        if not self._wait_until_false("Start_Stirring_Complete", description="搅拌启动完成复位"):
            raise ValueError("搅拌启动失败：完成状态复位超时")
        return {"success": True, "message": "搅拌启动完成"}

    @action(description="温控启动")
    def start_temp_control(self) -> Dict[str, Any]:
        """温控启动：写 Start_Temp_Control_Trigger 触发，等待 Start_Temp_Control_Complete 完成后复位。"""
        logger.info("温控启动...")
        self.set_node_value("Start_Temp_Control_Trigger", True)
        if not self._wait_until_true("Start_Temp_Control_Complete", description="温控启动完成"):
            raise ValueError("温控启动失败：动作未完成")
        self.set_node_value("Start_Temp_Control_Trigger", False)
        if not self._wait_until_false("Start_Temp_Control_Complete", description="温控启动完成复位"):
            raise ValueError("温控启动失败：完成状态复位超时")
        return {"success": True, "message": "温控启动完成"}

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
    def reaction_completed(self) -> bool:
        """反应完成（读节点 Reaction_Completed）。"""
        v = self.get_node_value("Reaction_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def stir_completed(self) -> bool:
        """搅拌完成（读节点 Stir_Completed）。"""
        v = self.get_node_value("Stir_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_charge_weight(self) -> float:
        """实际投料重量（读节点 Current_Charge_Weight）。"""
        v = self.get_node_value("Current_Charge_Weight")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_reaction_temperature(self) -> float:
        """实际反应温度（读节点 Current_Reaction_Temperature）。"""
        v = self.get_node_value("Current_Reaction_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_stir_speed(self) -> float:
        """实际搅拌速度（读节点 Current_Stir_Speed）。"""
        v = self.get_node_value("Current_Stir_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_reaction_time(self) -> float:
        """实际反应时间（读节点 Current_Reaction_Time）。"""
        v = self.get_node_value("Current_Reaction_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def liquid_level(self) -> float:
        """液位高度显示（读节点 Liquid_Level）。"""
        v = self.get_node_value("Liquid_Level")
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
