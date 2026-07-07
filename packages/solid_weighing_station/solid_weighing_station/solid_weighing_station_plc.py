"""
固体称量工作站 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「固体称量工作站」标准动作/属性映射为 PLC 节点读写：
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
    id="solid_weighing_station_plc",
    category=["固体称量工作站"],
    description="固体称量工作站 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="固体称量工作站(PLC)",
)
class SolidWeighingStationPLC(OpcUaClientWithSubscription):

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

    @action(description="设置称量精度")
    def set_weighing_precision(self, weighing_precision: int = 0) -> Dict[str, Any]:
        """设置称量精度：写入设定值节点 Weighing_Precision_Setpoint。"""
        self.set_node_value("Weighing_Precision_Setpoint", weighing_precision)
        return {"success": True, "message": "设置称量精度已下发", "weighing_precision": weighing_precision}

    @action(description="设置卸料速度")
    def set_discharge_speed(self, discharge_speed: float = 0.0) -> Dict[str, Any]:
        """设置卸料速度：写入设定值节点 Discharge_Speed_Setpoint。"""
        self.set_node_value("Discharge_Speed_Setpoint", discharge_speed)
        return {"success": True, "message": "设置卸料速度已下发", "discharge_speed": discharge_speed}

    @action(description="设置称量重量")
    def set_weighed_weight(self, weighed_weight: float = 0.0) -> Dict[str, Any]:
        """设置称量重量：写入设定值节点 Weighed_Weight_Setpoint。"""
        self.set_node_value("Weighed_Weight_Setpoint", weighed_weight)
        return {"success": True, "message": "设置称量重量已下发", "weighed_weight": weighed_weight}

    @action(description="称量")
    def weigh(self) -> Dict[str, Any]:
        """称量：写 Weigh_Trigger 触发，等待 Weigh_Complete 完成后复位。"""
        logger.info("称量...")
        self.set_node_value("Weigh_Trigger", True)
        if not self._wait_until_true("Weigh_Complete", description="称量完成"):
            raise ValueError("称量失败：动作未完成")
        self.set_node_value("Weigh_Trigger", False)
        if not self._wait_until_false("Weigh_Complete", description="称量完成复位"):
            raise ValueError("称量失败：完成状态复位超时")
        return {"success": True, "message": "称量完成"}

    @action(description="卸料")
    def discharge(self) -> Dict[str, Any]:
        """卸料：写 Discharge_Trigger 触发，等待 Discharge_Complete 完成后复位。"""
        logger.info("卸料...")
        self.set_node_value("Discharge_Trigger", True)
        if not self._wait_until_true("Discharge_Complete", description="卸料完成"):
            raise ValueError("卸料失败：动作未完成")
        self.set_node_value("Discharge_Trigger", False)
        if not self._wait_until_false("Discharge_Complete", description="卸料完成复位"):
            raise ValueError("卸料失败：完成状态复位超时")
        return {"success": True, "message": "卸料完成"}

    @action(description="校准")
    def calibrate(self) -> Dict[str, Any]:
        """校准：写 Calibrate_Trigger 触发，等待 Calibrate_Complete 完成后复位。"""
        logger.info("校准...")
        self.set_node_value("Calibrate_Trigger", True)
        if not self._wait_until_true("Calibrate_Complete", description="校准完成"):
            raise ValueError("校准失败：动作未完成")
        self.set_node_value("Calibrate_Trigger", False)
        if not self._wait_until_false("Calibrate_Complete", description="校准完成复位"):
            raise ValueError("校准失败：完成状态复位超时")
        return {"success": True, "message": "校准完成"}

    @action(description="去皮")
    def tare(self) -> Dict[str, Any]:
        """去皮：写 Tare_Trigger 触发，等待 Tare_Complete 完成后复位。"""
        logger.info("去皮...")
        self.set_node_value("Tare_Trigger", True)
        if not self._wait_until_true("Tare_Complete", description="去皮完成"):
            raise ValueError("去皮失败：动作未完成")
        self.set_node_value("Tare_Trigger", False)
        if not self._wait_until_false("Tare_Complete", description="去皮完成复位"):
            raise ValueError("去皮失败：完成状态复位超时")
        return {"success": True, "message": "去皮完成"}

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
    def current_weighed_weight(self) -> float:
        """实际称量重量（读节点 Current_Weighed_Weight）。"""
        v = self.get_node_value("Current_Weighed_Weight")
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
