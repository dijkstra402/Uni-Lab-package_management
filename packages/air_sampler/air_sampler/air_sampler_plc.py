"""
大气采样器 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「大气采样器」标准动作/属性映射为 PLC 节点读写：
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
    id="air_sampler_plc",
    category=["样品处理仪器与设备", "提取设备", "大气采样器"],
    description="大气采样器 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="大气采样器(PLC)",
)
class AirSamplerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置采样流量")
    def set_sampling_flow(self, sampling_flow: float = 0.0) -> Dict[str, Any]:
        """设置采样流量：写入设定值节点 Sampling_Flow_Setpoint。"""
        self.set_node_value("Sampling_Flow_Setpoint", sampling_flow)
        return {"success": True, "message": "设置采样流量已下发", "sampling_flow": sampling_flow}

    @action(description="设置采样时间")
    def set_sampling_time(self, sampling_time: float = 0.0) -> Dict[str, Any]:
        """设置采样时间：写入设定值节点 Sampling_Time_Setpoint。"""
        self.set_node_value("Sampling_Time_Setpoint", sampling_time)
        return {"success": True, "message": "设置采样时间已下发", "sampling_time": sampling_time}

    @action(description="设置采样压力")
    def set_sampling_pressure(self, sampling_pressure: float = 0.0) -> Dict[str, Any]:
        """设置采样压力：写入设定值节点 Sampling_Pressure_Setpoint。"""
        self.set_node_value("Sampling_Pressure_Setpoint", sampling_pressure)
        return {"success": True, "message": "设置采样压力已下发", "sampling_pressure": sampling_pressure}

    @action(description="设置采样温度")
    def set_sampling_temperature(self, sampling_temperature: float = 0.0) -> Dict[str, Any]:
        """设置采样温度：写入设定值节点 Sampling_Temperature_Setpoint。"""
        self.set_node_value("Sampling_Temperature_Setpoint", sampling_temperature)
        return {"success": True, "message": "设置采样温度已下发", "sampling_temperature": sampling_temperature}

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
    def flow_stable_state(self) -> bool:
        """流量稳定状态（读节点 Flow_Stable_State）。"""
        v = self.get_node_value("Flow_Stable_State")
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
    def current_sampling_flow(self) -> float:
        """实际采样流量（读节点 Current_Sampling_Flow）。"""
        v = self.get_node_value("Current_Sampling_Flow")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_sampling_time(self) -> float:
        """实际采样时间（读节点 Current_Sampling_Time）。"""
        v = self.get_node_value("Current_Sampling_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_sampling_pressure(self) -> float:
        """实际采样压力（读节点 Current_Sampling_Pressure）。"""
        v = self.get_node_value("Current_Sampling_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_sampling_temperature(self) -> float:
        """实际采样温度（读节点 Current_Sampling_Temperature）。"""
        v = self.get_node_value("Current_Sampling_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def sampling_state(self) -> bool:
        """采样状态（读节点 Sampling_State）。"""
        v = self.get_node_value("Sampling_State")
        return v if v is not None else False

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
