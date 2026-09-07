"""
蒸镀仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「蒸镀仪」标准动作/属性映射为 PLC 节点读写：
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
    id="evaporation_coater_plc",
    category=["器件制备设备", "蒸镀与表面沉积设备", "蒸镀仪"],
    description="蒸镀仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="蒸镀仪(PLC)",
)
class EvaporationCoaterPLC(OpcUaClientWithSubscription):

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

    @action(description="设置蒸发源温度")
    def set_evaporation_source_temp(self, evaporation_source_temp: float = 0.0) -> Dict[str, Any]:
        """设置蒸发源温度：写入设定值节点 Evaporation_Source_Temp_Setpoint。"""
        self.set_node_value("Evaporation_Source_Temp_Setpoint", evaporation_source_temp)
        return {"success": True, "message": "设置蒸发源温度已下发", "evaporation_source_temp": evaporation_source_temp}

    @action(description="设置蒸镀速率")
    def set_evaporation_rate(self, evaporation_rate: float = 0.0) -> Dict[str, Any]:
        """设置蒸镀速率：写入设定值节点 Evaporation_Rate_Setpoint。"""
        self.set_node_value("Evaporation_Rate_Setpoint", evaporation_rate)
        return {"success": True, "message": "设置蒸镀速率已下发", "evaporation_rate": evaporation_rate}

    @action(description="设置目标膜厚")
    def set_target_film_thickness(self, target_film_thickness: int = 0) -> Dict[str, Any]:
        """设置目标膜厚：写入设定值节点 Target_Film_Thickness_Setpoint。"""
        self.set_node_value("Target_Film_Thickness_Setpoint", target_film_thickness)
        return {"success": True, "message": "设置目标膜厚已下发", "target_film_thickness": target_film_thickness}

    @action(description="设置基板温度")
    def set_substrate_temperature(self, substrate_temperature: float = 0.0) -> Dict[str, Any]:
        """设置基板温度：写入设定值节点 Substrate_Temperature_Setpoint。"""
        self.set_node_value("Substrate_Temperature_Setpoint", substrate_temperature)
        return {"success": True, "message": "设置基板温度已下发", "substrate_temperature": substrate_temperature}

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

    @action(description="蒸镀启动")
    def start_evaporation_coating(self) -> Dict[str, Any]:
        """蒸镀启动：写 Start_Evaporation_Coating_Trigger 触发，等待 Start_Evaporation_Coating_Complete 完成后复位。"""
        logger.info("蒸镀启动...")
        self.set_node_value("Start_Evaporation_Coating_Trigger", True)
        if not self._wait_until_true("Start_Evaporation_Coating_Complete", description="蒸镀启动完成"):
            raise ValueError("蒸镀启动失败：动作未完成")
        self.set_node_value("Start_Evaporation_Coating_Trigger", False)
        if not self._wait_until_false("Start_Evaporation_Coating_Complete", description="蒸镀启动完成复位"):
            raise ValueError("蒸镀启动失败：完成状态复位超时")
        return {"success": True, "message": "蒸镀启动完成"}

    @action(description="蒸发源停止")
    def stop_evaporation_source(self) -> Dict[str, Any]:
        """蒸发源停止：写 Stop_Evaporation_Source_Trigger 触发，等待 Stop_Evaporation_Source_Complete 完成后复位。"""
        logger.info("蒸发源停止...")
        self.set_node_value("Stop_Evaporation_Source_Trigger", True)
        if not self._wait_until_true("Stop_Evaporation_Source_Complete", description="蒸发源停止完成"):
            raise ValueError("蒸发源停止失败：动作未完成")
        self.set_node_value("Stop_Evaporation_Source_Trigger", False)
        if not self._wait_until_false("Stop_Evaporation_Source_Complete", description="蒸发源停止完成复位"):
            raise ValueError("蒸发源停止失败：完成状态复位超时")
        return {"success": True, "message": "蒸发源停止完成"}

    @action(description="腔室充气")
    def inflate_chamber(self) -> Dict[str, Any]:
        """腔室充气：写 Inflate_Chamber_Trigger 触发，等待 Inflate_Chamber_Complete 完成后复位。"""
        logger.info("腔室充气...")
        self.set_node_value("Inflate_Chamber_Trigger", True)
        if not self._wait_until_true("Inflate_Chamber_Complete", description="腔室充气完成"):
            raise ValueError("腔室充气失败：动作未完成")
        self.set_node_value("Inflate_Chamber_Trigger", False)
        if not self._wait_until_false("Inflate_Chamber_Complete", description="腔室充气完成复位"):
            raise ValueError("腔室充气失败：完成状态复位超时")
        return {"success": True, "message": "腔室充气完成"}

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
    def evaporation_source_heating_completed(self) -> bool:
        """蒸发源加热完成（读节点 Evaporation_Source_Heating_Completed）。"""
        v = self.get_node_value("Evaporation_Source_Heating_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def film_thickness_ready(self) -> bool:
        """膜厚监测就绪（读节点 Film_Thickness_Ready）。"""
        v = self.get_node_value("Film_Thickness_Ready")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_evaporation_source_temp(self) -> float:
        """蒸发源温度实际值（读节点 Current_Evaporation_Source_Temp）。"""
        v = self.get_node_value("Current_Evaporation_Source_Temp")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_evaporation_rate(self) -> float:
        """蒸镀速率实际值（读节点 Current_Evaporation_Rate）。"""
        v = self.get_node_value("Current_Evaporation_Rate")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_film_thickness(self) -> int:
        """实际膜厚（读节点 Current_Film_Thickness）。"""
        v = self.get_node_value("Current_Film_Thickness")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_substrate_temperature(self) -> float:
        """基板温度实际值（读节点 Current_Substrate_Temperature）。"""
        v = self.get_node_value("Current_Substrate_Temperature")
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
