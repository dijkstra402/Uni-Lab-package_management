"""
微波消解仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「微波消解仪」标准动作/属性映射为 PLC 节点读写：
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
    id="microwave_digester_plc",
    category=["微波消解仪"],
    description="微波消解仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="微波消解仪(PLC)",
)
class MicrowaveDigesterPLC(OpcUaClientWithSubscription):

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

    @action(description="设置目标温度")
    def set_target_temperature(self, target_temperature: float = 0.0) -> Dict[str, Any]:
        """设置目标温度：写入设定值节点 Target_Temperature_Setpoint。"""
        self.set_node_value("Target_Temperature_Setpoint", target_temperature)
        return {"success": True, "message": "设置目标温度已下发", "target_temperature": target_temperature}

    @action(description="设置目标压力")
    def set_target_pressure(self, target_pressure: float = 0.0) -> Dict[str, Any]:
        """设置目标压力：写入设定值节点 Target_Pressure_Setpoint。"""
        self.set_node_value("Target_Pressure_Setpoint", target_pressure)
        return {"success": True, "message": "设置目标压力已下发", "target_pressure": target_pressure}

    @action(description="设置微波功率")
    def set_microwave_power(self, microwave_power: float = 0.0) -> Dict[str, Any]:
        """设置微波功率：写入设定值节点 Microwave_Power_Setpoint。"""
        self.set_node_value("Microwave_Power_Setpoint", microwave_power)
        return {"success": True, "message": "设置微波功率已下发", "microwave_power": microwave_power}

    @action(description="设置消解时间")
    def set_digestion_time(self, digestion_time: float = 0.0) -> Dict[str, Any]:
        """设置消解时间：写入设定值节点 Digestion_Time_Setpoint。"""
        self.set_node_value("Digestion_Time_Setpoint", digestion_time)
        return {"success": True, "message": "设置消解时间已下发", "digestion_time": digestion_time}

    @action(description="设置程序段")
    def set_program_segment(self, program_segment: int = 0) -> Dict[str, Any]:
        """设置程序段：写入设定值节点 Program_Segment_Setpoint。"""
        self.set_node_value("Program_Segment_Setpoint", program_segment)
        return {"success": True, "message": "设置程序段已下发", "program_segment": program_segment}

    @action(description="消解")
    def digest(self) -> Dict[str, Any]:
        """消解：写 Digest_Trigger 触发，等待 Digest_Complete 完成后复位。"""
        logger.info("消解...")
        self.set_node_value("Digest_Trigger", True)
        if not self._wait_until_true("Digest_Complete", description="消解完成"):
            raise ValueError("消解失败：动作未完成")
        self.set_node_value("Digest_Trigger", False)
        if not self._wait_until_false("Digest_Complete", description="消解完成复位"):
            raise ValueError("消解失败：完成状态复位超时")
        return {"success": True, "message": "消解完成"}

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
    def microwave_output_state(self) -> bool:
        """微波输出状态（读节点 Microwave_Output_State）。"""
        v = self.get_node_value("Microwave_Output_State")
        return v if v is not None else False

    @property
    @topic_config()
    def pressure_protection_state(self) -> bool:
        """压力保护状态（读节点 Pressure_Protection_State）。"""
        v = self.get_node_value("Pressure_Protection_State")
        return v if v is not None else False

    @property
    @topic_config()
    def temperature_protection_state(self) -> bool:
        """温度保护状态（读节点 Temperature_Protection_State）。"""
        v = self.get_node_value("Temperature_Protection_State")
        return v if v is not None else False

    @property
    @topic_config()
    def chamber_door_off_state(self) -> bool:
        """腔门关闭状态（读节点 Chamber_Door_Off_State）。"""
        v = self.get_node_value("Chamber_Door_Off_State")
        return v if v is not None else False

    @property
    @topic_config()
    def cooling_system_running(self) -> bool:
        """冷却系统运行（读节点 Cooling_System_Running）。"""
        v = self.get_node_value("Cooling_System_Running")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """实际温度检测（读节点 Current_Temperature）。"""
        v = self.get_node_value("Current_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_pressure(self) -> float:
        """实际压力检测（读节点 Current_Pressure）。"""
        v = self.get_node_value("Current_Pressure")
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
