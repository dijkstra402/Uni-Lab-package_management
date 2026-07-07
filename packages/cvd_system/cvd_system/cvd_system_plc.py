"""
化学气相沉积设备 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「化学气相沉积设备」标准动作/属性映射为 PLC 节点读写：
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
    id="cvd_system_plc",
    category=["化学气相沉积设备"],
    description="化学气相沉积设备 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="化学气相沉积设备(PLC)",
)
class CvdSystemPLC(OpcUaClientWithSubscription):

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

    @action(description="设置沉积温度")
    def set_deposition_temperature(self, deposition_temperature: float = 0.0) -> Dict[str, Any]:
        """设置沉积温度：写入设定值节点 Deposition_Temperature_Setpoint。"""
        self.set_node_value("Deposition_Temperature_Setpoint", deposition_temperature)
        return {"success": True, "message": "设置沉积温度已下发", "deposition_temperature": deposition_temperature}

    @action(description="设置工艺压力")
    def set_process_pressure(self, process_pressure: float = 0.0) -> Dict[str, Any]:
        """设置工艺压力：写入设定值节点 Process_Pressure_Setpoint。"""
        self.set_node_value("Process_Pressure_Setpoint", process_pressure)
        return {"success": True, "message": "设置工艺压力已下发", "process_pressure": process_pressure}

    @action(description="设置气体流量 1 ")
    def set_gas_flow_1(self, gas_flow_1: float = 0.0) -> Dict[str, Any]:
        """设置气体流量 1 ：写入设定值节点 Gas_Flow_1_Setpoint。"""
        self.set_node_value("Gas_Flow_1_Setpoint", gas_flow_1)
        return {"success": True, "message": "设置气体流量 1 已下发", "gas_flow_1": gas_flow_1}

    @action(description="设置沉积时间")
    def set_deposition_time(self, deposition_time: float = 0.0) -> Dict[str, Any]:
        """设置沉积时间：写入设定值节点 Deposition_Time_Setpoint。"""
        self.set_node_value("Deposition_Time_Setpoint", deposition_time)
        return {"success": True, "message": "设置沉积时间已下发", "deposition_time": deposition_time}

    @action(description="沉积启动")
    def start_deposition(self) -> Dict[str, Any]:
        """沉积启动：写 Start_Deposition_Trigger 触发，等待 Start_Deposition_Complete 完成后复位。"""
        logger.info("沉积启动...")
        self.set_node_value("Start_Deposition_Trigger", True)
        if not self._wait_until_true("Start_Deposition_Complete", description="沉积启动完成"):
            raise ValueError("沉积启动失败：动作未完成")
        self.set_node_value("Start_Deposition_Trigger", False)
        if not self._wait_until_false("Start_Deposition_Complete", description="沉积启动完成复位"):
            raise ValueError("沉积启动失败：完成状态复位超时")
        return {"success": True, "message": "沉积启动完成"}

    @action(description="抽真空")
    def evacuate(self) -> Dict[str, Any]:
        """抽真空：写 Evacuate_Trigger 触发，等待 Evacuate_Complete 完成后复位。"""
        logger.info("抽真空...")
        self.set_node_value("Evacuate_Trigger", True)
        if not self._wait_until_true("Evacuate_Complete", description="抽真空完成"):
            raise ValueError("抽真空失败：动作未完成")
        self.set_node_value("Evacuate_Trigger", False)
        if not self._wait_until_false("Evacuate_Complete", description="抽真空完成复位"):
            raise ValueError("抽真空失败：完成状态复位超时")
        return {"success": True, "message": "抽真空完成"}

    @action(description="气体切换")
    def switch_gas(self) -> Dict[str, Any]:
        """气体切换：写 Switch_Gas_Trigger 触发，等待 Switch_Gas_Complete 完成后复位。"""
        logger.info("气体切换...")
        self.set_node_value("Switch_Gas_Trigger", True)
        if not self._wait_until_true("Switch_Gas_Complete", description="气体切换完成"):
            raise ValueError("气体切换失败：动作未完成")
        self.set_node_value("Switch_Gas_Trigger", False)
        if not self._wait_until_false("Switch_Gas_Complete", description="气体切换完成复位"):
            raise ValueError("气体切换失败：完成状态复位超时")
        return {"success": True, "message": "气体切换完成"}

    @action(description="降温")
    def cool_down(self) -> Dict[str, Any]:
        """降温：写 Cool_Down_Trigger 触发，等待 Cool_Down_Complete 完成后复位。"""
        logger.info("降温...")
        self.set_node_value("Cool_Down_Trigger", True)
        if not self._wait_until_true("Cool_Down_Complete", description="降温完成"):
            raise ValueError("降温失败：动作未完成")
        self.set_node_value("Cool_Down_Trigger", False)
        if not self._wait_until_false("Cool_Down_Complete", description="降温完成复位"):
            raise ValueError("降温失败：完成状态复位超时")
        return {"success": True, "message": "降温完成"}

    @action(description="腔室开门")
    def open_chamber_door(self) -> Dict[str, Any]:
        """腔室开门：写 Open_Chamber_Door_Trigger 触发，等待 Open_Chamber_Door_Complete 完成后复位。"""
        logger.info("腔室开门...")
        self.set_node_value("Open_Chamber_Door_Trigger", True)
        if not self._wait_until_true("Open_Chamber_Door_Complete", description="腔室开门完成"):
            raise ValueError("腔室开门失败：动作未完成")
        self.set_node_value("Open_Chamber_Door_Trigger", False)
        if not self._wait_until_false("Open_Chamber_Door_Complete", description="腔室开门完成复位"):
            raise ValueError("腔室开门失败：完成状态复位超时")
        return {"success": True, "message": "腔室开门完成"}

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
    def deposition_completed(self) -> bool:
        """沉积完成（读节点 Deposition_Completed）。"""
        v = self.get_node_value("Deposition_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_deposition_temperature(self) -> float:
        """沉积温度实际值（读节点 Current_Deposition_Temperature）。"""
        v = self.get_node_value("Current_Deposition_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_process_pressure(self) -> float:
        """工艺压力实际值（读节点 Current_Process_Pressure）。"""
        v = self.get_node_value("Current_Process_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_gas_flow_1(self) -> float:
        """气体流量 1 实际值（读节点 Current_Gas_Flow_1）。"""
        v = self.get_node_value("Current_Gas_Flow_1")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def deposition_time_remaining(self) -> float:
        """沉积时间剩余值（读节点 Deposition_Time_Remaining）。"""
        v = self.get_node_value("Deposition_Time_Remaining")
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
