"""
超声波萃取设备 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「超声波萃取设备」标准动作/属性映射为 PLC 节点读写：
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
    id="ultrasonic_extractor_plc",
    category=["超声波萃取设备"],
    description="超声波萃取设备 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="超声波萃取设备(PLC)",
)
class UltrasonicExtractorPLC(OpcUaClientWithSubscription):

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

    @action(description="设置运行时间")
    def set_run_time(self, run_time: float = 0.0) -> Dict[str, Any]:
        """设置运行时间：写入设定值节点 Run_Time_Setpoint。"""
        self.set_node_value("Run_Time_Setpoint", run_time)
        return {"success": True, "message": "设置运行时间已下发", "run_time": run_time}

    @action(description="设置超声功率")
    def set_ultrasonic_power(self, ultrasonic_power: float = 0.0) -> Dict[str, Any]:
        """设置超声功率：写入设定值节点 Ultrasonic_Power_Setpoint。"""
        self.set_node_value("Ultrasonic_Power_Setpoint", ultrasonic_power)
        return {"success": True, "message": "设置超声功率已下发", "ultrasonic_power": ultrasonic_power}

    @action(description="设置超声频率")
    def set_ultrasonic_frequency(self, ultrasonic_frequency: float = 0.0) -> Dict[str, Any]:
        """设置超声频率：写入设定值节点 Ultrasonic_Frequency_Setpoint。"""
        self.set_node_value("Ultrasonic_Frequency_Setpoint", ultrasonic_frequency)
        return {"success": True, "message": "设置超声频率已下发", "ultrasonic_frequency": ultrasonic_frequency}

    @action(description="设置萃取温度")
    def set_extraction_temperature(self, extraction_temperature: float = 0.0) -> Dict[str, Any]:
        """设置萃取温度：写入设定值节点 Extraction_Temperature_Setpoint。"""
        self.set_node_value("Extraction_Temperature_Setpoint", extraction_temperature)
        return {"success": True, "message": "设置萃取温度已下发", "extraction_temperature": extraction_temperature}

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行：写 Run_Trigger 触发，等待 Run_Complete 完成后复位。"""
        logger.info("运行...")
        self.set_node_value("Run_Trigger", True)
        if not self._wait_until_true("Run_Complete", description="运行完成"):
            raise ValueError("运行失败：动作未完成")
        self.set_node_value("Run_Trigger", False)
        if not self._wait_until_false("Run_Complete", description="运行完成复位"):
            raise ValueError("运行失败：完成状态复位超时")
        return {"success": True, "message": "运行完成"}

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止：写 Stop_Trigger 触发，等待 Stop_Complete 完成后复位。"""
        logger.info("停止...")
        self.set_node_value("Stop_Trigger", True)
        if not self._wait_until_true("Stop_Complete", description="停止完成"):
            raise ValueError("停止失败：动作未完成")
        self.set_node_value("Stop_Trigger", False)
        if not self._wait_until_false("Stop_Complete", description="停止完成复位"):
            raise ValueError("停止失败：完成状态复位超时")
        return {"success": True, "message": "停止完成"}

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位：写 Reset_Trigger 触发，等待 Reset_Complete 完成后复位。"""
        logger.info("复位...")
        self.set_node_value("Reset_Trigger", True)
        if not self._wait_until_true("Reset_Complete", description="复位完成"):
            raise ValueError("复位失败：动作未完成")
        self.set_node_value("Reset_Trigger", False)
        if not self._wait_until_false("Reset_Complete", description="复位完成复位"):
            raise ValueError("复位失败：完成状态复位超时")
        return {"success": True, "message": "复位完成"}

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
    def ultrasonic_on_state(self) -> bool:
        """超声开启状态（读节点 Ultrasonic_On_State）。"""
        v = self.get_node_value("Ultrasonic_On_State")
        return v if v is not None else False

    @property
    @topic_config()
    def temperature_protection_state(self) -> bool:
        """温度保护状态（读节点 Temperature_Protection_State）。"""
        v = self.get_node_value("Temperature_Protection_State")
        return v if v is not None else False

    @property
    @topic_config()
    def liquid_level_state(self) -> bool:
        """液位检测状态（读节点 Liquid_Level_State）。"""
        v = self.get_node_value("Liquid_Level_State")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_run_time(self) -> float:
        """实际运行时间（读节点 Current_Run_Time）。"""
        v = self.get_node_value("Current_Run_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_ultrasonic_power(self) -> float:
        """实际超声功率（读节点 Current_Ultrasonic_Power）。"""
        v = self.get_node_value("Current_Ultrasonic_Power")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_ultrasonic_frequency(self) -> float:
        """实际超声频率（读节点 Current_Ultrasonic_Frequency）。"""
        v = self.get_node_value("Current_Ultrasonic_Frequency")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_extraction_temperature(self) -> float:
        """实际萃取温度（读节点 Current_Extraction_Temperature）。"""
        v = self.get_node_value("Current_Extraction_Temperature")
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
