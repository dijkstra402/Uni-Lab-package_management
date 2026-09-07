"""
超声波清洗机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「超声波清洗机」标准动作/属性映射为 PLC 节点读写：
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
    id="ultrasonic_cleaner_plc",
    category=["样品处理仪器与设备", "清洗机", "超声波清洗机"],
    description="超声波清洗机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="超声波清洗机(PLC)",
)
class UltrasonicCleanerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置清洗时间")
    def set_cleaning_time(self, cleaning_time: float = 0.0) -> Dict[str, Any]:
        """设置清洗时间：写入设定值节点 Cleaning_Time_Setpoint。"""
        self.set_node_value("Cleaning_Time_Setpoint", cleaning_time)
        return {"success": True, "message": "设置清洗时间已下发", "cleaning_time": cleaning_time}

    @action(description="设置清洗温度")
    def set_cleaning_temperature(self, cleaning_temperature: float = 0.0) -> Dict[str, Any]:
        """设置清洗温度：写入设定值节点 Cleaning_Temperature_Setpoint。"""
        self.set_node_value("Cleaning_Temperature_Setpoint", cleaning_temperature)
        return {"success": True, "message": "设置清洗温度已下发", "cleaning_temperature": cleaning_temperature}

    @action(description="设置清洗压力")
    def set_cleaning_pressure(self, cleaning_pressure: float = 0.0) -> Dict[str, Any]:
        """设置清洗压力：写入设定值节点 Cleaning_Pressure_Setpoint。"""
        self.set_node_value("Cleaning_Pressure_Setpoint", cleaning_pressure)
        return {"success": True, "message": "设置清洗压力已下发", "cleaning_pressure": cleaning_pressure}

    @action(description="设置超声波功率")
    def set_ultrasonic_power(self, ultrasonic_power: float = 0.0) -> Dict[str, Any]:
        """设置超声波功率：写入设定值节点 Ultrasonic_Power_Setpoint。"""
        self.set_node_value("Ultrasonic_Power_Setpoint", ultrasonic_power)
        return {"success": True, "message": "设置超声波功率已下发", "ultrasonic_power": ultrasonic_power}

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗：写 Clean_Trigger 触发，等待 Clean_Complete 完成后复位。"""
        logger.info("清洗...")
        self.set_node_value("Clean_Trigger", True)
        if not self._wait_until_true("Clean_Complete", description="清洗完成"):
            raise ValueError("清洗失败：动作未完成")
        self.set_node_value("Clean_Trigger", False)
        if not self._wait_until_false("Clean_Complete", description="清洗完成复位"):
            raise ValueError("清洗失败：完成状态复位超时")
        return {"success": True, "message": "清洗完成"}

    @action(description="清洗准备")
    def prepare_cleaning(self) -> Dict[str, Any]:
        """清洗准备：写 Prepare_Cleaning_Trigger 触发，等待 Prepare_Cleaning_Complete 完成后复位。"""
        logger.info("清洗准备...")
        self.set_node_value("Prepare_Cleaning_Trigger", True)
        if not self._wait_until_true("Prepare_Cleaning_Complete", description="清洗准备完成"):
            raise ValueError("清洗准备失败：动作未完成")
        self.set_node_value("Prepare_Cleaning_Trigger", False)
        if not self._wait_until_false("Prepare_Cleaning_Complete", description="清洗准备完成复位"):
            raise ValueError("清洗准备失败：完成状态复位超时")
        return {"success": True, "message": "清洗准备完成"}

    @action(description="清洗结束")
    def finish_cleaning(self) -> Dict[str, Any]:
        """清洗结束：写 Finish_Cleaning_Trigger 触发，等待 Finish_Cleaning_Complete 完成后复位。"""
        logger.info("清洗结束...")
        self.set_node_value("Finish_Cleaning_Trigger", True)
        if not self._wait_until_true("Finish_Cleaning_Complete", description="清洗结束完成"):
            raise ValueError("清洗结束失败：动作未完成")
        self.set_node_value("Finish_Cleaning_Trigger", False)
        if not self._wait_until_false("Finish_Cleaning_Complete", description="清洗结束完成复位"):
            raise ValueError("清洗结束失败：完成状态复位超时")
        return {"success": True, "message": "清洗结束完成"}

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
    def liquid_level(self) -> bool:
        """液位检测（读节点 Liquid_Level）。"""
        v = self.get_node_value("Liquid_Level")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_cleaning_time(self) -> float:
        """实际清洗时间（读节点 Current_Cleaning_Time）。"""
        v = self.get_node_value("Current_Cleaning_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def ultrasonic_power_feedback(self) -> float:
        """超声波功率反馈（读节点 Ultrasonic_Power_Feedback）。"""
        v = self.get_node_value("Ultrasonic_Power_Feedback")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def cleaning_temperature_feedback(self) -> float:
        """清洗温度反馈（读节点 Cleaning_Temperature_Feedback）。"""
        v = self.get_node_value("Cleaning_Temperature_Feedback")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def cleaning_time_feedback(self) -> float:
        """清洗时间反馈（读节点 Cleaning_Time_Feedback）。"""
        v = self.get_node_value("Cleaning_Time_Feedback")
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
