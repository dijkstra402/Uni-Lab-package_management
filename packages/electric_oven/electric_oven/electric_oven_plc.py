"""
电烤箱 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「电烤箱」标准动作/属性映射为 PLC 节点读写：
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
    id="electric_oven_plc",
    category=["加热、制冷及空气净化与调节设备", "恒温箱及类似设备", "高温箱", "电烤箱"],
    description="电烤箱 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="电烤箱(PLC)",
)
class ElectricOvenPLC(OpcUaClientWithSubscription):

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

    @action(description="设置烘烤时间")
    def set_baking_time(self, baking_time: float = 0.0) -> Dict[str, Any]:
        """设置烘烤时间：写入设定值节点 Baking_Time_Setpoint。"""
        self.set_node_value("Baking_Time_Setpoint", baking_time)
        return {"success": True, "message": "设置烘烤时间已下发", "baking_time": baking_time}

    @action(description="设置加热模式")
    def set_heating_mode(self, heating_mode: str = "") -> Dict[str, Any]:
        """设置加热模式：写入设定值节点 Heating_Mode_Setpoint。"""
        self.set_node_value("Heating_Mode_Setpoint", heating_mode)
        return {"success": True, "message": "设置加热模式已下发", "heating_mode": heating_mode}

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: float = 0.0) -> Dict[str, Any]:
        """设置加热功率：写入设定值节点 Heating_Power_Setpoint。"""
        self.set_node_value("Heating_Power_Setpoint", heating_power)
        return {"success": True, "message": "设置加热功率已下发", "heating_power": heating_power}

    @action(description="设置旋转速度")
    def set_rotation_speed(self, rotation_speed: float = 0.0) -> Dict[str, Any]:
        """设置旋转速度：写入设定值节点 Rotation_Speed_Setpoint。"""
        self.set_node_value("Rotation_Speed_Setpoint", rotation_speed)
        return {"success": True, "message": "设置旋转速度已下发", "rotation_speed": rotation_speed}

    @action(description="设置热风转速")
    def set_hot_air_speed(self, hot_air_speed: float = 0.0) -> Dict[str, Any]:
        """设置热风转速：写入设定值节点 Hot_Air_Speed_Setpoint。"""
        self.set_node_value("Hot_Air_Speed_Setpoint", hot_air_speed)
        return {"success": True, "message": "设置热风转速已下发", "hot_air_speed": hot_air_speed}

    @action(description="设置温度")
    def set_temperature(self, temperature: float = 0.0) -> Dict[str, Any]:
        """设置温度：写入设定值节点 Temperature_Setpoint。"""
        self.set_node_value("Temperature_Setpoint", temperature)
        return {"success": True, "message": "设置温度已下发", "temperature": temperature}

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
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_run_step(self) -> int:
        """当前运行步骤（读节点 Current_Run_Step）。"""
        v = self.get_node_value("Current_Run_Step")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """当前温度（读节点 Current_Temperature）。"""
        v = self.get_node_value("Current_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def remaining_baking_time(self) -> float:
        """剩余烘烤时间（读节点 Remaining_Baking_Time）。"""
        v = self.get_node_value("Remaining_Baking_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_heating_power(self) -> float:
        """实际加热功率（读节点 Current_Heating_Power）。"""
        v = self.get_node_value("Current_Heating_Power")
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
