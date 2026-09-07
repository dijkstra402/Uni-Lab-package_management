"""
撕膜仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「撕膜仪」标准动作/属性映射为 PLC 节点读写：
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
    id="plate_peeler_plc",
    category=["合成制备仪器与设备", "液体分配设备", "撕膜仪"],
    description="撕膜仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="撕膜仪(PLC)",
)
class PlatePeelerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置撕膜速度")
    def set_peeling_speed(self, peeling_speed: float = 0.0) -> Dict[str, Any]:
        """设置撕膜速度：写入设定值节点 Peeling_Speed_Setpoint。"""
        self.set_node_value("Peeling_Speed_Setpoint", peeling_speed)
        return {"success": True, "message": "设置撕膜速度已下发", "peeling_speed": peeling_speed}

    @action(description="设置撕膜高度")
    def set_peeling_height(self, peeling_height: float = 0.0) -> Dict[str, Any]:
        """设置撕膜高度：写入设定值节点 Peeling_Height_Setpoint。"""
        self.set_node_value("Peeling_Height_Setpoint", peeling_height)
        return {"success": True, "message": "设置撕膜高度已下发", "peeling_height": peeling_height}

    @action(description="设置抓取压力")
    def set_grip_pressure(self, grip_pressure: float = 0.0) -> Dict[str, Any]:
        """设置抓取压力：写入设定值节点 Grip_Pressure_Setpoint。"""
        self.set_node_value("Grip_Pressure_Setpoint", grip_pressure)
        return {"success": True, "message": "设置抓取压力已下发", "grip_pressure": grip_pressure}

    @action(description="设置容器位置")
    def set_container_position(self, container_position: float = 0.0) -> Dict[str, Any]:
        """设置容器位置：写入设定值节点 Container_Position_Setpoint。"""
        self.set_node_value("Container_Position_Setpoint", container_position)
        return {"success": True, "message": "设置容器位置已下发", "container_position": container_position}

    @action(description="撕膜启动")
    def start_peeling(self) -> Dict[str, Any]:
        """撕膜启动：写 Start_Peeling_Trigger 触发，等待 Start_Peeling_Complete 完成后复位。"""
        logger.info("撕膜启动...")
        self.set_node_value("Start_Peeling_Trigger", True)
        if not self._wait_until_true("Start_Peeling_Complete", description="撕膜启动完成"):
            raise ValueError("撕膜启动失败：动作未完成")
        self.set_node_value("Start_Peeling_Trigger", False)
        if not self._wait_until_false("Start_Peeling_Complete", description="撕膜启动完成复位"):
            raise ValueError("撕膜启动失败：完成状态复位超时")
        return {"success": True, "message": "撕膜启动完成"}

    @action(description="定位")
    def position(self) -> Dict[str, Any]:
        """定位：写 Position_Trigger 触发，等待 Position_Complete 完成后复位。"""
        logger.info("定位...")
        self.set_node_value("Position_Trigger", True)
        if not self._wait_until_true("Position_Complete", description="定位完成"):
            raise ValueError("定位失败：动作未完成")
        self.set_node_value("Position_Trigger", False)
        if not self._wait_until_false("Position_Complete", description="定位完成复位"):
            raise ValueError("定位失败：完成状态复位超时")
        return {"success": True, "message": "定位完成"}

    @action(description="抓取")
    def grip(self) -> Dict[str, Any]:
        """抓取：写 Grip_Trigger 触发，等待 Grip_Complete 完成后复位。"""
        logger.info("抓取...")
        self.set_node_value("Grip_Trigger", True)
        if not self._wait_until_true("Grip_Complete", description="抓取完成"):
            raise ValueError("抓取失败：动作未完成")
        self.set_node_value("Grip_Trigger", False)
        if not self._wait_until_false("Grip_Complete", description="抓取完成复位"):
            raise ValueError("抓取失败：完成状态复位超时")
        return {"success": True, "message": "抓取完成"}

    @action(description="丢弃")
    def discard(self) -> Dict[str, Any]:
        """丢弃：写 Discard_Trigger 触发，等待 Discard_Complete 完成后复位。"""
        logger.info("丢弃...")
        self.set_node_value("Discard_Trigger", True)
        if not self._wait_until_true("Discard_Complete", description="丢弃完成"):
            raise ValueError("丢弃失败：动作未完成")
        self.set_node_value("Discard_Trigger", False)
        if not self._wait_until_false("Discard_Complete", description="丢弃完成复位"):
            raise ValueError("丢弃失败：完成状态复位超时")
        return {"success": True, "message": "丢弃完成"}

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
    def peeling_completed(self) -> bool:
        """撕膜完成（读节点 Peeling_Completed）。"""
        v = self.get_node_value("Peeling_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_peeling_speed(self) -> float:
        """实际撕膜速度（读节点 Current_Peeling_Speed）。"""
        v = self.get_node_value("Current_Peeling_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_peeling_height(self) -> float:
        """实际撕膜高度（读节点 Current_Peeling_Height）。"""
        v = self.get_node_value("Current_Peeling_Height")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_grip_pressure(self) -> float:
        """实际抓取压力（读节点 Current_Grip_Pressure）。"""
        v = self.get_node_value("Current_Grip_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_container_position(self) -> float:
        """实际容器位置（读节点 Current_Container_Position）。"""
        v = self.get_node_value("Current_Container_Position")
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
