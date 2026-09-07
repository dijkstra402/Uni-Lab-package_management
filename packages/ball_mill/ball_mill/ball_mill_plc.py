"""
球磨机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「球磨机」标准动作/属性映射为 PLC 节点读写：
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
    id="ball_mill_plc",
    category=["样品处理仪器与设备", "粉碎设备", "球磨机"],
    description="球磨机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="球磨机(PLC)",
)
class BallMillPLC(OpcUaClientWithSubscription):

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

    @action(description="设置研磨时间")
    def set_grinding_time(self, grinding_time: float = 0.0) -> Dict[str, Any]:
        """设置研磨时间：写入设定值节点 Grinding_Time_Setpoint。"""
        self.set_node_value("Grinding_Time_Setpoint", grinding_time)
        return {"success": True, "message": "设置研磨时间已下发", "grinding_time": grinding_time}

    @action(description="设置球料比")
    def set_ball_to_powder_ratio(self, ball_to_powder_ratio: float = 0.0) -> Dict[str, Any]:
        """设置球料比：写入设定值节点 Ball_To_Powder_Ratio_Setpoint。"""
        self.set_node_value("Ball_To_Powder_Ratio_Setpoint", ball_to_powder_ratio)
        return {"success": True, "message": "设置球料比已下发", "ball_to_powder_ratio": ball_to_powder_ratio}

    @action(description="设置研磨温度")
    def set_grinding_temperature(self, grinding_temperature: float = 0.0) -> Dict[str, Any]:
        """设置研磨温度：写入设定值节点 Grinding_Temperature_Setpoint。"""
        self.set_node_value("Grinding_Temperature_Setpoint", grinding_temperature)
        return {"success": True, "message": "设置研磨温度已下发", "grinding_temperature": grinding_temperature}

    @action(description="设置正反转间隔")
    def set_fwd_rev_interval(self, fwd_rev_interval: float = 0.0) -> Dict[str, Any]:
        """设置正反转间隔：写入设定值节点 Fwd_Rev_Interval_Setpoint。"""
        self.set_node_value("Fwd_Rev_Interval_Setpoint", fwd_rev_interval)
        return {"success": True, "message": "设置正反转间隔已下发", "fwd_rev_interval": fwd_rev_interval}

    @action(description="设置转速")
    def set_speed(self, speed: float = 0.0) -> Dict[str, Any]:
        """设置转速：写入设定值节点 Speed_Setpoint。"""
        self.set_node_value("Speed_Setpoint", speed)
        return {"success": True, "message": "设置转速已下发", "speed": speed}

    @action(description="研磨")
    def grind(self) -> Dict[str, Any]:
        """研磨：写 Grind_Trigger 触发，等待 Grind_Complete 完成后复位。"""
        logger.info("研磨...")
        self.set_node_value("Grind_Trigger", True)
        if not self._wait_until_true("Grind_Complete", description="研磨完成"):
            raise ValueError("研磨失败：动作未完成")
        self.set_node_value("Grind_Trigger", False)
        if not self._wait_until_false("Grind_Complete", description="研磨完成复位"):
            raise ValueError("研磨失败：完成状态复位超时")
        return {"success": True, "message": "研磨完成"}

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
    def current_speed(self) -> float:
        """实际转速（读节点 Current_Speed）。"""
        v = self.get_node_value("Current_Speed")
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
