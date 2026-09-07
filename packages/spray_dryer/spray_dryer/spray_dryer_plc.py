"""
喷雾干燥机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「喷雾干燥机」标准动作/属性映射为 PLC 节点读写：
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
    id="spray_dryer_plc",
    category=["样品处理仪器与设备", "分离设备", "喷雾干燥机"],
    description="喷雾干燥机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="喷雾干燥机(PLC)",
)
class SprayDryerPLC(OpcUaClientWithSubscription):

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

    @action(description="干燥")
    def dry(self) -> Dict[str, Any]:
        """干燥：写 Dry_Trigger 触发，等待 Dry_Complete 完成后复位。"""
        logger.info("干燥...")
        self.set_node_value("Dry_Trigger", True)
        if not self._wait_until_true("Dry_Complete", description="干燥完成"):
            raise ValueError("干燥失败：动作未完成")
        self.set_node_value("Dry_Trigger", False)
        if not self._wait_until_false("Dry_Complete", description="干燥完成复位"):
            raise ValueError("干燥失败：完成状态复位超时")
        return {"success": True, "message": "干燥完成"}

    @action(description="进料")
    def feed_in(self) -> Dict[str, Any]:
        """进料：写 Feed_In_Trigger 触发，等待 Feed_In_Complete 完成后复位。"""
        logger.info("进料...")
        self.set_node_value("Feed_In_Trigger", True)
        if not self._wait_until_true("Feed_In_Complete", description="进料完成"):
            raise ValueError("进料失败：动作未完成")
        self.set_node_value("Feed_In_Trigger", False)
        if not self._wait_until_false("Feed_In_Complete", description="进料完成复位"):
            raise ValueError("进料失败：完成状态复位超时")
        return {"success": True, "message": "进料完成"}

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
    def feed_flow(self) -> float:
        """进料流量（读节点 Feed_Flow）。"""
        v = self.get_node_value("Feed_Flow")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def drying_time(self) -> float:
        """干燥时间（读节点 Drying_Time）。"""
        v = self.get_node_value("Drying_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def collection_state(self) -> int:
        """收料状态（读节点 Collection_State）。"""
        v = self.get_node_value("Collection_State")
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
