"""
涡旋混匀仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「涡旋混匀仪」标准动作/属性映射为 PLC 节点读写：
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
    id="vortex_mixer_plc",
    category=["涡旋混匀仪"],
    description="涡旋混匀仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="涡旋混匀仪(PLC)",
)
class VortexMixerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置混匀速度")
    def set_mix_speed(self, mix_speed: float = 0.0) -> Dict[str, Any]:
        """设置混匀速度：写入设定值节点 Mix_Speed_Setpoint。"""
        self.set_node_value("Mix_Speed_Setpoint", mix_speed)
        return {"success": True, "message": "设置混匀速度已下发", "mix_speed": mix_speed}

    @action(description="设置混匀时间")
    def set_mix_time(self, mix_time: float = 0.0) -> Dict[str, Any]:
        """设置混匀时间：写入设定值节点 Mix_Time_Setpoint。"""
        self.set_node_value("Mix_Time_Setpoint", mix_time)
        return {"success": True, "message": "设置混匀时间已下发", "mix_time": mix_time}

    @action(description="设置工作模式")
    def set_work_mode(self, work_mode: str = "") -> Dict[str, Any]:
        """设置工作模式：写入设定值节点 Work_Mode_Setpoint。"""
        self.set_node_value("Work_Mode_Setpoint", work_mode)
        return {"success": True, "message": "设置工作模式已下发", "work_mode": work_mode}

    @action(description="设置速度档位")
    def set_speed_gear(self, speed_gear: int = 0) -> Dict[str, Any]:
        """设置速度档位：写入设定值节点 Speed_Gear_Setpoint。"""
        self.set_node_value("Speed_Gear_Setpoint", speed_gear)
        return {"success": True, "message": "设置速度档位已下发", "speed_gear": speed_gear}

    @action(description="设置启动延迟")
    def set_start_delay(self, start_delay: int = 0) -> Dict[str, Any]:
        """设置启动延迟：写入设定值节点 Start_Delay_Setpoint。"""
        self.set_node_value("Start_Delay_Setpoint", start_delay)
        return {"success": True, "message": "设置启动延迟已下发", "start_delay": start_delay}

    @action(description="设置循环次数")
    def set_cycle_count(self, cycle_count: int = 0) -> Dict[str, Any]:
        """设置循环次数：写入设定值节点 Cycle_Count_Setpoint。"""
        self.set_node_value("Cycle_Count_Setpoint", cycle_count)
        return {"success": True, "message": "设置循环次数已下发", "cycle_count": cycle_count}

    @action(description="设置时间")
    def set_time(self, time: float = 0.0) -> Dict[str, Any]:
        """设置时间：写入设定值节点 Time_Setpoint。"""
        self.set_node_value("Time_Setpoint", time)
        return {"success": True, "message": "设置时间已下发", "time": time}

    @action(description="混匀")
    def mix(self) -> Dict[str, Any]:
        """混匀：写 Mix_Trigger 触发，等待 Mix_Complete 完成后复位。"""
        logger.info("混匀...")
        self.set_node_value("Mix_Trigger", True)
        if not self._wait_until_true("Mix_Complete", description="混匀完成"):
            raise ValueError("混匀失败：动作未完成")
        self.set_node_value("Mix_Trigger", False)
        if not self._wait_until_false("Mix_Complete", description="混匀完成复位"):
            raise ValueError("混匀失败：完成状态复位超时")
        return {"success": True, "message": "混匀完成"}

    @action(description="脚踏开关")
    def foot_switch(self) -> Dict[str, Any]:
        """脚踏开关：写 Foot_Switch_Trigger 触发，等待 Foot_Switch_Complete 完成后复位。"""
        logger.info("脚踏开关...")
        self.set_node_value("Foot_Switch_Trigger", True)
        if not self._wait_until_true("Foot_Switch_Complete", description="脚踏开关完成"):
            raise ValueError("脚踏开关失败：动作未完成")
        self.set_node_value("Foot_Switch_Trigger", False)
        if not self._wait_until_false("Foot_Switch_Complete", description="脚踏开关完成复位"):
            raise ValueError("脚踏开关失败：完成状态复位超时")
        return {"success": True, "message": "脚踏开关完成"}

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
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_speed(self) -> float:
        """当前速度显示（读节点 Current_Speed）。"""
        v = self.get_node_value("Current_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示（读节点 Current_Time）。"""
        v = self.get_node_value("Current_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_cycle_count(self) -> int:
        """当前循环次数（读节点 Current_Cycle_Count）。"""
        v = self.get_node_value("Current_Cycle_Count")
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
