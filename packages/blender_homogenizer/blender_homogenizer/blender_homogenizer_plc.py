"""
匀浆机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「匀浆机」标准动作/属性映射为 PLC 节点读写：
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
    id="blender_homogenizer_plc",
    category=["样品处理仪器与设备", "混合与分散设备", "匀浆机"],
    description="匀浆机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="匀浆机(PLC)",
)
class BlenderHomogenizerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置匀浆转速")
    def set_blend_speed(self, blend_speed: float = 0.0) -> Dict[str, Any]:
        """设置匀浆转速：写入设定值节点 Blend_Speed_Setpoint。"""
        self.set_node_value("Blend_Speed_Setpoint", blend_speed)
        return {"success": True, "message": "设置匀浆转速已下发", "blend_speed": blend_speed}

    @action(description="设置匀浆时间")
    def set_blend_time(self, blend_time: float = 0.0) -> Dict[str, Any]:
        """设置匀浆时间：写入设定值节点 Blend_Time_Setpoint。"""
        self.set_node_value("Blend_Time_Setpoint", blend_time)
        return {"success": True, "message": "设置匀浆时间已下发", "blend_time": blend_time}

    @action(description="设置匀浆模式")
    def set_blend_mode(self, blend_mode: str = "") -> Dict[str, Any]:
        """设置匀浆模式：写入设定值节点 Blend_Mode_Setpoint。"""
        self.set_node_value("Blend_Mode_Setpoint", blend_mode)
        return {"success": True, "message": "设置匀浆模式已下发", "blend_mode": blend_mode}

    @action(description="设置脉冲间隔")
    def set_pulse_interval(self, pulse_interval: float = 0.0) -> Dict[str, Any]:
        """设置脉冲间隔：写入设定值节点 Pulse_Interval_Setpoint。"""
        self.set_node_value("Pulse_Interval_Setpoint", pulse_interval)
        return {"success": True, "message": "设置脉冲间隔已下发", "pulse_interval": pulse_interval}

    @action(description="设置脉冲宽度")
    def set_pulse_width(self, pulse_width: int = 0) -> Dict[str, Any]:
        """设置脉冲宽度：写入设定值节点 Pulse_Width_Setpoint。"""
        self.set_node_value("Pulse_Width_Setpoint", pulse_width)
        return {"success": True, "message": "设置脉冲宽度已下发", "pulse_width": pulse_width}

    @action(description="设置扭矩限制")
    def set_torque_limit(self, torque_limit: float = 0.0) -> Dict[str, Any]:
        """设置扭矩限制：写入设定值节点 Torque_Limit_Setpoint。"""
        self.set_node_value("Torque_Limit_Setpoint", torque_limit)
        return {"success": True, "message": "设置扭矩限制已下发", "torque_limit": torque_limit}

    @action(description="设置时间")
    def set_time(self, time: float = 0.0) -> Dict[str, Any]:
        """设置时间：写入设定值节点 Time_Setpoint。"""
        self.set_node_value("Time_Setpoint", time)
        return {"success": True, "message": "设置时间已下发", "time": time}

    @action(description="匀浆")
    def blend(self) -> Dict[str, Any]:
        """匀浆：写 Blend_Trigger 触发，等待 Blend_Complete 完成后复位。"""
        logger.info("匀浆...")
        self.set_node_value("Blend_Trigger", True)
        if not self._wait_until_true("Blend_Complete", description="匀浆完成"):
            raise ValueError("匀浆失败：动作未完成")
        self.set_node_value("Blend_Trigger", False)
        if not self._wait_until_false("Blend_Complete", description="匀浆完成复位"):
            raise ValueError("匀浆失败：完成状态复位超时")
        return {"success": True, "message": "匀浆完成"}

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
    def safety_lock_state(self) -> bool:
        """安全锁状态（读节点 Safety_Lock_State）。"""
        v = self.get_node_value("Safety_Lock_State")
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
        """当前转速显示（读节点 Current_Speed）。"""
        v = self.get_node_value("Current_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示（读节点 Current_Time）。"""
        v = self.get_node_value("Current_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_torque(self) -> float:
        """当前扭矩显示（读节点 Current_Torque）。"""
        v = self.get_node_value("Current_Torque")
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
