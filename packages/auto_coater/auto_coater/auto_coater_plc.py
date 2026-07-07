"""
自动涂布机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「自动涂布机」标准动作/属性映射为 PLC 节点读写：
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
    id="auto_coater_plc",
    category=["自动涂布机"],
    description="自动涂布机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="自动涂布机(PLC)",
)
class AutoCoaterPLC(OpcUaClientWithSubscription):

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

    @action(description="设置涂布速度")
    def set_coating_speed(self, coating_speed: float = 0.0) -> Dict[str, Any]:
        """设置涂布速度：写入设定值节点 Coating_Speed_Setpoint。"""
        self.set_node_value("Coating_Speed_Setpoint", coating_speed)
        return {"success": True, "message": "设置涂布速度已下发", "coating_speed": coating_speed}

    @action(description="设置涂布厚度")
    def set_coating_thickness(self, coating_thickness: float = 0.0) -> Dict[str, Any]:
        """设置涂布厚度：写入设定值节点 Coating_Thickness_Setpoint。"""
        self.set_node_value("Coating_Thickness_Setpoint", coating_thickness)
        return {"success": True, "message": "设置涂布厚度已下发", "coating_thickness": coating_thickness}

    @action(description="设置涂布宽度")
    def set_coating_width(self, coating_width: int = 0) -> Dict[str, Any]:
        """设置涂布宽度：写入设定值节点 Coating_Width_Setpoint。"""
        self.set_node_value("Coating_Width_Setpoint", coating_width)
        return {"success": True, "message": "设置涂布宽度已下发", "coating_width": coating_width}

    @action(description="设置刮刀压力")
    def set_blade_pressure(self, blade_pressure: float = 0.0) -> Dict[str, Any]:
        """设置刮刀压力：写入设定值节点 Blade_Pressure_Setpoint。"""
        self.set_node_value("Blade_Pressure_Setpoint", blade_pressure)
        return {"success": True, "message": "设置刮刀压力已下发", "blade_pressure": blade_pressure}

    @action(description="设置干燥温度")
    def set_drying_temperature(self, drying_temperature: float = 0.0) -> Dict[str, Any]:
        """设置干燥温度：写入设定值节点 Drying_Temperature_Setpoint。"""
        self.set_node_value("Drying_Temperature_Setpoint", drying_temperature)
        return {"success": True, "message": "设置干燥温度已下发", "drying_temperature": drying_temperature}

    @action(description="设置干燥时间")
    def set_drying_time(self, drying_time: float = 0.0) -> Dict[str, Any]:
        """设置干燥时间：写入设定值节点 Drying_Time_Setpoint。"""
        self.set_node_value("Drying_Time_Setpoint", drying_time)
        return {"success": True, "message": "设置干燥时间已下发", "drying_time": drying_time}

    @action(description="设置涂布次数")
    def set_coating_count(self, coating_count: int = 0) -> Dict[str, Any]:
        """设置涂布次数：写入设定值节点 Coating_Count_Setpoint。"""
        self.set_node_value("Coating_Count_Setpoint", coating_count)
        return {"success": True, "message": "设置涂布次数已下发", "coating_count": coating_count}

    @action(description="设置刮刀角度")
    def set_blade_angle(self, blade_angle: float = 0.0) -> Dict[str, Any]:
        """设置刮刀角度：写入设定值节点 Blade_Angle_Setpoint。"""
        self.set_node_value("Blade_Angle_Setpoint", blade_angle)
        return {"success": True, "message": "设置刮刀角度已下发", "blade_angle": blade_angle}

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动：写 Start_Trigger 触发，等待 Start_Complete 完成后复位。"""
        logger.info("启动...")
        self.set_node_value("Start_Trigger", True)
        if not self._wait_until_true("Start_Complete", description="启动完成"):
            raise ValueError("启动失败：动作未完成")
        self.set_node_value("Start_Trigger", False)
        if not self._wait_until_false("Start_Complete", description="启动完成复位"):
            raise ValueError("启动失败：完成状态复位超时")
        return {"success": True, "message": "启动完成"}

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
    def running_completed(self) -> bool:
        """运行完成（读节点 Running_Completed）。"""
        v = self.get_node_value("Running_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
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
