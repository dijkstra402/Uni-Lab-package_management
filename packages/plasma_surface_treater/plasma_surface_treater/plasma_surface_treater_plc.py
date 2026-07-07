"""
等离子体表面处理机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「等离子体表面处理机」标准动作/属性映射为 PLC 节点读写：
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
    id="plasma_surface_treater_plc",
    category=["等离子体表面处理机"],
    description="等离子体表面处理机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="等离子体表面处理机(PLC)",
)
class PlasmaSurfaceTreaterPLC(OpcUaClientWithSubscription):

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

    @action(description="设置处理功率")
    def set_treatment_power(self, treatment_power: float = 0.0) -> Dict[str, Any]:
        """设置处理功率：写入设定值节点 Treatment_Power_Setpoint。"""
        self.set_node_value("Treatment_Power_Setpoint", treatment_power)
        return {"success": True, "message": "设置处理功率已下发", "treatment_power": treatment_power}

    @action(description="设置处理时间")
    def set_treatment_time(self, treatment_time: float = 0.0) -> Dict[str, Any]:
        """设置处理时间：写入设定值节点 Treatment_Time_Setpoint。"""
        self.set_node_value("Treatment_Time_Setpoint", treatment_time)
        return {"success": True, "message": "设置处理时间已下发", "treatment_time": treatment_time}

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """设置真空度：写入设定值节点 Vacuum_Setpoint。"""
        self.set_node_value("Vacuum_Setpoint", vacuum)
        return {"success": True, "message": "设置真空度已下发", "vacuum": vacuum}

    @action(description="设置气体流量")
    def set_gas_flow(self, gas_flow: float = 0.0) -> Dict[str, Any]:
        """设置气体流量：写入设定值节点 Gas_Flow_Setpoint。"""
        self.set_node_value("Gas_Flow_Setpoint", gas_flow)
        return {"success": True, "message": "设置气体流量已下发", "gas_flow": gas_flow}

    @action(description="设置电极距离")
    def set_electrode_distance(self, electrode_distance: float = 0.0) -> Dict[str, Any]:
        """设置电极距离：写入设定值节点 Electrode_Distance_Setpoint。"""
        self.set_node_value("Electrode_Distance_Setpoint", electrode_distance)
        return {"success": True, "message": "设置电极距离已下发", "electrode_distance": electrode_distance}

    @action(description="设置等离子体密度")
    def set_plasma_density(self, plasma_density: float = 0.0) -> Dict[str, Any]:
        """设置等离子体密度：写入设定值节点 Plasma_Density_Setpoint。"""
        self.set_node_value("Plasma_Density_Setpoint", plasma_density)
        return {"success": True, "message": "设置等离子体密度已下发", "plasma_density": plasma_density}

    @action(description="设置处理次数")
    def set_treatment_count(self, treatment_count: int = 0) -> Dict[str, Any]:
        """设置处理次数：写入设定值节点 Treatment_Count_Setpoint。"""
        self.set_node_value("Treatment_Count_Setpoint", treatment_count)
        return {"success": True, "message": "设置处理次数已下发", "treatment_count": treatment_count}

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
    def sample_moving_speed(self) -> float:
        """样品移动速度（读节点 Sample_Moving_Speed）。"""
        v = self.get_node_value("Sample_Moving_Speed")
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
