"""
均质器 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「均质器」标准动作/属性映射为 PLC 节点读写：
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
    id="homogenizer_plc",
    category=["样品处理仪器与设备", "混合与分散设备", "均质器"],
    description="均质器 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="均质器(PLC)",
)
class HomogenizerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置均质压力")
    def set_homogenize_pressure(self, homogenize_pressure: float = 0.0) -> Dict[str, Any]:
        """设置均质压力：写入设定值节点 Homogenize_Pressure_Setpoint。"""
        self.set_node_value("Homogenize_Pressure_Setpoint", homogenize_pressure)
        return {"success": True, "message": "设置均质压力已下发", "homogenize_pressure": homogenize_pressure}

    @action(description="设置均质流量")
    def set_homogenize_flow(self, homogenize_flow: float = 0.0) -> Dict[str, Any]:
        """设置均质流量：写入设定值节点 Homogenize_Flow_Setpoint。"""
        self.set_node_value("Homogenize_Flow_Setpoint", homogenize_flow)
        return {"success": True, "message": "设置均质流量已下发", "homogenize_flow": homogenize_flow}

    @action(description="设置运行时间")
    def set_run_time(self, run_time: float = 0.0) -> Dict[str, Any]:
        """设置运行时间：写入设定值节点 Run_Time_Setpoint。"""
        self.set_node_value("Run_Time_Setpoint", run_time)
        return {"success": True, "message": "设置运行时间已下发", "run_time": run_time}

    @action(description="设置均质级别")
    def set_homogenize_level(self, homogenize_level: int = 0) -> Dict[str, Any]:
        """设置均质级别：写入设定值节点 Homogenize_Level_Setpoint。"""
        self.set_node_value("Homogenize_Level_Setpoint", homogenize_level)
        return {"success": True, "message": "设置均质级别已下发", "homogenize_level": homogenize_level}

    @action(description="设置循环次数")
    def set_cycle_count(self, cycle_count: int = 0) -> Dict[str, Any]:
        """设置循环次数：写入设定值节点 Cycle_Count_Setpoint。"""
        self.set_node_value("Cycle_Count_Setpoint", cycle_count)
        return {"success": True, "message": "设置循环次数已下发", "cycle_count": cycle_count}

    @action(description="设置压力上限")
    def set_pressure_upper_limit(self, pressure_upper_limit: float = 0.0) -> Dict[str, Any]:
        """设置压力上限：写入设定值节点 Pressure_Upper_Limit_Setpoint。"""
        self.set_node_value("Pressure_Upper_Limit_Setpoint", pressure_upper_limit)
        return {"success": True, "message": "设置压力上限已下发", "pressure_upper_limit": pressure_upper_limit}

    @action(description="设置流量上限")
    def set_flow_upper_limit(self, flow_upper_limit: float = 0.0) -> Dict[str, Any]:
        """设置流量上限：写入设定值节点 Flow_Upper_Limit_Setpoint。"""
        self.set_node_value("Flow_Upper_Limit_Setpoint", flow_upper_limit)
        return {"success": True, "message": "设置流量上限已下发", "flow_upper_limit": flow_upper_limit}

    @action(description="均质")
    def homogenize(self) -> Dict[str, Any]:
        """均质：写 Homogenize_Trigger 触发，等待 Homogenize_Complete 完成后复位。"""
        logger.info("均质...")
        self.set_node_value("Homogenize_Trigger", True)
        if not self._wait_until_true("Homogenize_Complete", description="均质完成"):
            raise ValueError("均质失败：动作未完成")
        self.set_node_value("Homogenize_Trigger", False)
        if not self._wait_until_false("Homogenize_Complete", description="均质完成复位"):
            raise ValueError("均质失败：完成状态复位超时")
        return {"success": True, "message": "均质完成"}

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
    def pressure_protection(self) -> bool:
        """压力保护（读节点 Pressure_Protection）。"""
        v = self.get_node_value("Pressure_Protection")
        return v if v is not None else False

    @property
    @topic_config()
    def flow_protection(self) -> bool:
        """流量保护（读节点 Flow_Protection）。"""
        v = self.get_node_value("Flow_Protection")
        return v if v is not None else False

    @property
    @topic_config()
    def cleaning_mode(self) -> bool:
        """清洗模式（读节点 Cleaning_Mode）。"""
        v = self.get_node_value("Cleaning_Mode")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_pressure(self) -> float:
        """当前压力显示（读节点 Current_Pressure）。"""
        v = self.get_node_value("Current_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_flow(self) -> float:
        """当前流量显示（读节点 Current_Flow）。"""
        v = self.get_node_value("Current_Flow")
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

    @property
    @topic_config()
    def temperature(self) -> float:
        """温度监测显示（读节点 Temperature）。"""
        v = self.get_node_value("Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def safety_protection_level(self) -> int:
        """安全保护等级（读节点 Safety_Protection_Level）。"""
        v = self.get_node_value("Safety_Protection_Level")
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
