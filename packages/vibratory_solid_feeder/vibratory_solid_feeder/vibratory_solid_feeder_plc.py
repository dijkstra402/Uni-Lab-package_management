"""
振动固体加料模块 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「振动固体加料模块」标准动作/属性映射为 PLC 节点读写：
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
    id="vibratory_solid_feeder_plc",
    category=["合成制备仪器与设备", "固体分配设备", "振动固体加料模块"],
    description="振动固体加料模块 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="振动固体加料模块(PLC)",
)
class VibratorySolidFeederPLC(OpcUaClientWithSubscription):

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

    @action(description="设置振动频率")
    def set_vibration_frequency(self, vibration_frequency: float = 0.0) -> Dict[str, Any]:
        """设置振动频率：写入设定值节点 Vibration_Frequency_Setpoint。"""
        self.set_node_value("Vibration_Frequency_Setpoint", vibration_frequency)
        return {"success": True, "message": "设置振动频率已下发", "vibration_frequency": vibration_frequency}

    @action(description="设置振动振幅")
    def set_vibration_amplitude(self, vibration_amplitude: int = 0) -> Dict[str, Any]:
        """设置振动振幅：写入设定值节点 Vibration_Amplitude_Setpoint。"""
        self.set_node_value("Vibration_Amplitude_Setpoint", vibration_amplitude)
        return {"success": True, "message": "设置振动振幅已下发", "vibration_amplitude": vibration_amplitude}

    @action(description="设置加料时间")
    def set_feed_time(self, feed_time: float = 0.0) -> Dict[str, Any]:
        """设置加料时间：写入设定值节点 Feed_Time_Setpoint。"""
        self.set_node_value("Feed_Time_Setpoint", feed_time)
        return {"success": True, "message": "设置加料时间已下发", "feed_time": feed_time}

    @action(description="设置加料量")
    def set_feed_amount(self, feed_amount: float = 0.0) -> Dict[str, Any]:
        """设置加料量：写入设定值节点 Feed_Amount_Setpoint。"""
        self.set_node_value("Feed_Amount_Setpoint", feed_amount)
        return {"success": True, "message": "设置加料量已下发", "feed_amount": feed_amount}

    @action(description="加料")
    def feed(self) -> Dict[str, Any]:
        """加料：写 Feed_Trigger 触发，等待 Feed_Complete 完成后复位。"""
        logger.info("加料...")
        self.set_node_value("Feed_Trigger", True)
        if not self._wait_until_true("Feed_Complete", description="加料完成"):
            raise ValueError("加料失败：动作未完成")
        self.set_node_value("Feed_Trigger", False)
        if not self._wait_until_false("Feed_Complete", description="加料完成复位"):
            raise ValueError("加料失败：完成状态复位超时")
        return {"success": True, "message": "加料完成"}

    @action(description="清堵")
    def clear_clog(self) -> Dict[str, Any]:
        """清堵：写 Clear_Clog_Trigger 触发，等待 Clear_Clog_Complete 完成后复位。"""
        logger.info("清堵...")
        self.set_node_value("Clear_Clog_Trigger", True)
        if not self._wait_until_true("Clear_Clog_Complete", description="清堵完成"):
            raise ValueError("清堵失败：动作未完成")
        self.set_node_value("Clear_Clog_Trigger", False)
        if not self._wait_until_false("Clear_Clog_Complete", description="清堵完成复位"):
            raise ValueError("清堵失败：完成状态复位超时")
        return {"success": True, "message": "清堵完成"}

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
    def current_feed_amount(self) -> int:
        """实际加料量（读节点 Current_Feed_Amount）。"""
        v = self.get_node_value("Current_Feed_Amount")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_vibration_frequency(self) -> float:
        """实际振动频率（读节点 Current_Vibration_Frequency）。"""
        v = self.get_node_value("Current_Vibration_Frequency")
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
