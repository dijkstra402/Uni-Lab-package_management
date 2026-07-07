"""
组织研磨仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「组织研磨仪」标准动作/属性映射为 PLC 节点读写：
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
    id="tissue_grinder_plc",
    category=["组织研磨仪"],
    description="组织研磨仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="组织研磨仪(PLC)",
)
class TissueGrinderPLC(OpcUaClientWithSubscription):

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

    @action(description="设置目标转速")
    def set_target_speed(self, target_speed: float = 0.0) -> Dict[str, Any]:
        """设置目标转速：写入设定值节点 Target_Speed_Setpoint。"""
        self.set_node_value("Target_Speed_Setpoint", target_speed)
        return {"success": True, "message": "设置目标转速已下发", "target_speed": target_speed}

    @action(description="设置研磨时间")
    def set_grinding_time(self, grinding_time: float = 0.0) -> Dict[str, Any]:
        """设置研磨时间：写入设定值节点 Grinding_Time_Setpoint。"""
        self.set_node_value("Grinding_Time_Setpoint", grinding_time)
        return {"success": True, "message": "设置研磨时间已下发", "grinding_time": grinding_time}

    @action(description="设置振幅等级")
    def set_amplitude_level(self, amplitude_level: int = 0) -> Dict[str, Any]:
        """设置振幅等级：写入设定值节点 Amplitude_Level_Setpoint。"""
        self.set_node_value("Amplitude_Level_Setpoint", amplitude_level)
        return {"success": True, "message": "设置振幅等级已下发", "amplitude_level": amplitude_level}

    @action(description="设置制冷温度")
    def set_cooling_temperature(self, cooling_temperature: float = 0.0) -> Dict[str, Any]:
        """设置制冷温度：写入设定值节点 Cooling_Temperature_Setpoint。"""
        self.set_node_value("Cooling_Temperature_Setpoint", cooling_temperature)
        return {"success": True, "message": "设置制冷温度已下发", "cooling_temperature": cooling_temperature}

    @action(description="设置循环次数")
    def set_cycle_count(self, cycle_count: int = 0) -> Dict[str, Any]:
        """设置循环次数：写入设定值节点 Cycle_Count_Setpoint。"""
        self.set_node_value("Cycle_Count_Setpoint", cycle_count)
        return {"success": True, "message": "设置循环次数已下发", "cycle_count": cycle_count}

    @action(description="研磨")
    def grind(self) -> Dict[str, Any]:
        """研磨：写 Grind_Trigger 触发，等待 Grind_Complete 完成后复位。"""
        logger.info("研磨...")
        self.set_node_value("Grind_Trigger", True)
        if not self._wait_until_true("Grind_Complete", description="研磨完成"):
            raise ValueError("研磨失败：动作未完成")
        self.set_node_value("Grind_Trigger", False)
        if not self._wait_until_false("Grind_Complete", description="研磨完成复位"):
            raise ValueError("研磨失败：完成状态复位超时")
        return {"success": True, "message": "研磨完成"}

    @action(description="制冷")
    def cool(self) -> Dict[str, Any]:
        """制冷：写 Cool_Trigger 触发，等待 Cool_Complete 完成后复位。"""
        logger.info("制冷...")
        self.set_node_value("Cool_Trigger", True)
        if not self._wait_until_true("Cool_Complete", description="制冷完成"):
            raise ValueError("制冷失败：动作未完成")
        self.set_node_value("Cool_Trigger", False)
        if not self._wait_until_false("Cool_Complete", description="制冷完成复位"):
            raise ValueError("制冷失败：完成状态复位超时")
        return {"success": True, "message": "制冷完成"}

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
    def sample_chamber_door_state(self) -> bool:
        """样品室门状态（读节点 Sample_Chamber_Door_State）。"""
        v = self.get_node_value("Sample_Chamber_Door_State")
        return v if v is not None else False

    @property
    @topic_config()
    def safety_lock_state(self) -> bool:
        """安全锁状态（读节点 Safety_Lock_State）。"""
        v = self.get_node_value("Safety_Lock_State")
        return v if v is not None else False

    @property
    @topic_config()
    def amplitude_stable_state(self) -> bool:
        """振幅稳定状态（读节点 Amplitude_Stable_State）。"""
        v = self.get_node_value("Amplitude_Stable_State")
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
        """实际转速检测（读节点 Current_Speed）。"""
        v = self.get_node_value("Current_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """实际温度检测（读节点 Current_Temperature）。"""
        v = self.get_node_value("Current_Temperature")
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
