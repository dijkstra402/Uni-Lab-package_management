"""
分散机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「分散机」标准动作/属性映射为 PLC 节点读写：
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
    id="disperser_plc",
    category=["样品处理仪器与设备", "混合与分散设备", "分散机"],
    description="分散机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="分散机(PLC)",
)
class DisperserPLC(OpcUaClientWithSubscription):

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

    @action(description="设置分散转速")
    def set_dispersion_speed(self, dispersion_speed: float = 0.0) -> Dict[str, Any]:
        """设置分散转速：写入设定值节点 Dispersion_Speed_Setpoint。"""
        self.set_node_value("Dispersion_Speed_Setpoint", dispersion_speed)
        return {"success": True, "message": "设置分散转速已下发", "dispersion_speed": dispersion_speed}

    @action(description="设置分散时间")
    def set_dispersion_time(self, dispersion_time: float = 0.0) -> Dict[str, Any]:
        """设置分散时间：写入设定值节点 Dispersion_Time_Setpoint。"""
        self.set_node_value("Dispersion_Time_Setpoint", dispersion_time)
        return {"success": True, "message": "设置分散时间已下发", "dispersion_time": dispersion_time}

    @action(description="设置分散头高度")
    def set_disperser_head_height(self, disperser_head_height: float = 0.0) -> Dict[str, Any]:
        """设置分散头高度：写入设定值节点 Disperser_Head_Height_Setpoint。"""
        self.set_node_value("Disperser_Head_Height_Setpoint", disperser_head_height)
        return {"success": True, "message": "设置分散头高度已下发", "disperser_head_height": disperser_head_height}

    @action(description="设置分散模式")
    def set_dispersion_mode(self, dispersion_mode: str = "") -> Dict[str, Any]:
        """设置分散模式：写入设定值节点 Dispersion_Mode_Setpoint。"""
        self.set_node_value("Dispersion_Mode_Setpoint", dispersion_mode)
        return {"success": True, "message": "设置分散模式已下发", "dispersion_mode": dispersion_mode}

    @action(description="设置转速增量")
    def set_speed_increment(self, speed_increment: float = 0.0) -> Dict[str, Any]:
        """设置转速增量：写入设定值节点 Speed_Increment_Setpoint。"""
        self.set_node_value("Speed_Increment_Setpoint", speed_increment)
        return {"success": True, "message": "设置转速增量已下发", "speed_increment": speed_increment}

    @action(description="设置增量时间")
    def set_increment_time(self, increment_time: float = 0.0) -> Dict[str, Any]:
        """设置增量时间：写入设定值节点 Increment_Time_Setpoint。"""
        self.set_node_value("Increment_Time_Setpoint", increment_time)
        return {"success": True, "message": "设置增量时间已下发", "increment_time": increment_time}

    @action(description="设置扭矩限制")
    def set_torque_limit(self, torque_limit: float = 0.0) -> Dict[str, Any]:
        """设置扭矩限制：写入设定值节点 Torque_Limit_Setpoint。"""
        self.set_node_value("Torque_Limit_Setpoint", torque_limit)
        return {"success": True, "message": "设置扭矩限制已下发", "torque_limit": torque_limit}

    @action(description="分散")
    def disperse(self) -> Dict[str, Any]:
        """分散：写 Disperse_Trigger 触发，等待 Disperse_Complete 完成后复位。"""
        logger.info("分散...")
        self.set_node_value("Disperse_Trigger", True)
        if not self._wait_until_true("Disperse_Complete", description="分散完成"):
            raise ValueError("分散失败：动作未完成")
        self.set_node_value("Disperse_Trigger", False)
        if not self._wait_until_false("Disperse_Complete", description="分散完成复位"):
            raise ValueError("分散失败：完成状态复位超时")
        return {"success": True, "message": "分散完成"}

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
    def current_height(self) -> float:
        """当前高度显示（读节点 Current_Height）。"""
        v = self.get_node_value("Current_Height")
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
