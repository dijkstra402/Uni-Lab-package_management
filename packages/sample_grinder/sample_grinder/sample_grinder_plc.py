"""
磨样机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「磨样机」标准动作/属性映射为 PLC 节点读写：
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
    id="sample_grinder_plc",
    category=["磨样机"],
    description="磨样机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="磨样机(PLC)",
)
class SampleGrinderPLC(OpcUaClientWithSubscription):

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

    @action(description="设置研磨转速")
    def set_grinding_speed(self, grinding_speed: float = 0.0) -> Dict[str, Any]:
        """设置研磨转速：写入设定值节点 Grinding_Speed_Setpoint。"""
        self.set_node_value("Grinding_Speed_Setpoint", grinding_speed)
        return {"success": True, "message": "设置研磨转速已下发", "grinding_speed": grinding_speed}

    @action(description="设置研磨时间")
    def set_grinding_time(self, grinding_time: float = 0.0) -> Dict[str, Any]:
        """设置研磨时间：写入设定值节点 Grinding_Time_Setpoint。"""
        self.set_node_value("Grinding_Time_Setpoint", grinding_time)
        return {"success": True, "message": "设置研磨时间已下发", "grinding_time": grinding_time}

    @action(description="设置研磨压力")
    def set_grinding_pressure(self, grinding_pressure: float = 0.0) -> Dict[str, Any]:
        """设置研磨压力：写入设定值节点 Grinding_Pressure_Setpoint。"""
        self.set_node_value("Grinding_Pressure_Setpoint", grinding_pressure)
        return {"success": True, "message": "设置研磨压力已下发", "grinding_pressure": grinding_pressure}

    @action(description="设置磨头选择")
    def set_grinding_head_select(self, grinding_head_select: int = 0) -> Dict[str, Any]:
        """设置磨头选择：写入设定值节点 Grinding_Head_Select_Setpoint。"""
        self.set_node_value("Grinding_Head_Select_Setpoint", grinding_head_select)
        return {"success": True, "message": "设置磨头选择已下发", "grinding_head_select": grinding_head_select}

    @action(description="设置粒度控制")
    def set_particle_size_control(self, particle_size_control: int = 0) -> Dict[str, Any]:
        """设置粒度控制：写入设定值节点 Particle_Size_Control_Setpoint。"""
        self.set_node_value("Particle_Size_Control_Setpoint", particle_size_control)
        return {"success": True, "message": "设置粒度控制已下发", "particle_size_control": particle_size_control}

    @action(description="设置冷却水量")
    def set_cooling_water_volume(self, cooling_water_volume: int = 0) -> Dict[str, Any]:
        """设置冷却水量：写入设定值节点 Cooling_Water_Volume_Setpoint。"""
        self.set_node_value("Cooling_Water_Volume_Setpoint", cooling_water_volume)
        return {"success": True, "message": "设置冷却水量已下发", "cooling_water_volume": cooling_water_volume}

    @action(description="设置振动频率")
    def set_vibration_frequency(self, vibration_frequency: float = 0.0) -> Dict[str, Any]:
        """设置振动频率：写入设定值节点 Vibration_Frequency_Setpoint。"""
        self.set_node_value("Vibration_Frequency_Setpoint", vibration_frequency)
        return {"success": True, "message": "设置振动频率已下发", "vibration_frequency": vibration_frequency}

    @action(description="设置研磨精度")
    def set_grinding_precision(self, grinding_precision: int = 0) -> Dict[str, Any]:
        """设置研磨精度：写入设定值节点 Grinding_Precision_Setpoint。"""
        self.set_node_value("Grinding_Precision_Setpoint", grinding_precision)
        return {"success": True, "message": "设置研磨精度已下发", "grinding_precision": grinding_precision}

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

    @property
    @topic_config()
    def current_speed(self) -> float:
        """实际转速监测（读节点 Current_Speed）。"""
        v = self.get_node_value("Current_Speed")
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
