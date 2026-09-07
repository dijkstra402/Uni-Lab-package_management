"""
热混匀仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「热混匀仪」标准动作/属性映射为 PLC 节点读写：
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
    id="thermomixer_plc",
    category=["样品处理仪器与设备", "混合与分散设备", "热混匀仪"],
    description="热混匀仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="热混匀仪(PLC)",
)
class ThermomixerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置加热温度")
    def set_heating_temperature(self, heating_temperature: float = 0.0) -> Dict[str, Any]:
        """设置加热温度：写入设定值节点 Heating_Temperature_Setpoint。"""
        self.set_node_value("Heating_Temperature_Setpoint", heating_temperature)
        return {"success": True, "message": "设置加热温度已下发", "heating_temperature": heating_temperature}

    @action(description="设置混匀速度")
    def set_mix_speed(self, mix_speed: float = 0.0) -> Dict[str, Any]:
        """设置混匀速度：写入设定值节点 Mix_Speed_Setpoint。"""
        self.set_node_value("Mix_Speed_Setpoint", mix_speed)
        return {"success": True, "message": "设置混匀速度已下发", "mix_speed": mix_speed}

    @action(description="设置运行时间")
    def set_run_time(self, run_time: float = 0.0) -> Dict[str, Any]:
        """设置运行时间：写入设定值节点 Run_Time_Setpoint。"""
        self.set_node_value("Run_Time_Setpoint", run_time)
        return {"success": True, "message": "设置运行时间已下发", "run_time": run_time}

    @action(description="设置工作模式")
    def set_work_mode(self, work_mode: str = "") -> Dict[str, Any]:
        """设置工作模式：写入设定值节点 Work_Mode_Setpoint。"""
        self.set_node_value("Work_Mode_Setpoint", work_mode)
        return {"success": True, "message": "设置工作模式已下发", "work_mode": work_mode}

    @action(description="设置温度单位")
    def set_temperature_unit(self, temperature_unit: float = 0.0) -> Dict[str, Any]:
        """设置温度单位：写入设定值节点 Temperature_Unit_Setpoint。"""
        self.set_node_value("Temperature_Unit_Setpoint", temperature_unit)
        return {"success": True, "message": "设置温度单位已下发", "temperature_unit": temperature_unit}

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: float = 0.0) -> Dict[str, Any]:
        """设置加热功率：写入设定值节点 Heating_Power_Setpoint。"""
        self.set_node_value("Heating_Power_Setpoint", heating_power)
        return {"success": True, "message": "设置加热功率已下发", "heating_power": heating_power}

    @action(description="设置安全温度")
    def set_safety_temperature(self, safety_temperature: float = 0.0) -> Dict[str, Any]:
        """设置安全温度：写入设定值节点 Safety_Temperature_Setpoint。"""
        self.set_node_value("Safety_Temperature_Setpoint", safety_temperature)
        return {"success": True, "message": "设置安全温度已下发", "safety_temperature": safety_temperature}

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
    def door_switch_state(self) -> bool:
        """门开关状态（读节点 Door_Switch_State）。"""
        v = self.get_node_value("Door_Switch_State")
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
        """当前温度显示（读节点 Current_Temperature）。"""
        v = self.get_node_value("Current_Temperature")
        return v if v is not None else 0.0

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
