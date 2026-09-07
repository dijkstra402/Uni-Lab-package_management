"""
封膜仪 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「封膜仪」标准动作/属性映射为 PLC 节点读写：
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
    id="plate_sealer_plc",
    category=["合成制备仪器与设备", "液体分配设备", "封膜仪"],
    description="封膜仪 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="封膜仪(PLC)",
)
class PlateSealerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置封膜温度")
    def set_sealing_temperature(self, sealing_temperature: float = 0.0) -> Dict[str, Any]:
        """设置封膜温度：写入设定值节点 Sealing_Temperature_Setpoint。"""
        self.set_node_value("Sealing_Temperature_Setpoint", sealing_temperature)
        return {"success": True, "message": "设置封膜温度已下发", "sealing_temperature": sealing_temperature}

    @action(description="设置封膜时间")
    def set_sealing_time(self, sealing_time: float = 0.0) -> Dict[str, Any]:
        """设置封膜时间：写入设定值节点 Sealing_Time_Setpoint。"""
        self.set_node_value("Sealing_Time_Setpoint", sealing_time)
        return {"success": True, "message": "设置封膜时间已下发", "sealing_time": sealing_time}

    @action(description="设置送膜长度")
    def set_film_feed_length(self, film_feed_length: int = 0) -> Dict[str, Any]:
        """设置送膜长度：写入设定值节点 Film_Feed_Length_Setpoint。"""
        self.set_node_value("Film_Feed_Length_Setpoint", film_feed_length)
        return {"success": True, "message": "设置送膜长度已下发", "film_feed_length": film_feed_length}

    @action(description="设置压力")
    def set_pressure(self, pressure: float = 0.0) -> Dict[str, Any]:
        """设置压力：写入设定值节点 Pressure_Setpoint。"""
        self.set_node_value("Pressure_Setpoint", pressure)
        return {"success": True, "message": "设置压力已下发", "pressure": pressure}

    @action(description="封膜启动")
    def start_sealing(self) -> Dict[str, Any]:
        """封膜启动：写 Start_Sealing_Trigger 触发，等待 Start_Sealing_Complete 完成后复位。"""
        logger.info("封膜启动...")
        self.set_node_value("Start_Sealing_Trigger", True)
        if not self._wait_until_true("Start_Sealing_Complete", description="封膜启动完成"):
            raise ValueError("封膜启动失败：动作未完成")
        self.set_node_value("Start_Sealing_Trigger", False)
        if not self._wait_until_false("Start_Sealing_Complete", description="封膜启动完成复位"):
            raise ValueError("封膜启动失败：完成状态复位超时")
        return {"success": True, "message": "封膜启动完成"}

    @action(description="送膜")
    def feed_film(self) -> Dict[str, Any]:
        """送膜：写 Feed_Film_Trigger 触发，等待 Feed_Film_Complete 完成后复位。"""
        logger.info("送膜...")
        self.set_node_value("Feed_Film_Trigger", True)
        if not self._wait_until_true("Feed_Film_Complete", description="送膜完成"):
            raise ValueError("送膜失败：动作未完成")
        self.set_node_value("Feed_Film_Trigger", False)
        if not self._wait_until_false("Feed_Film_Complete", description="送膜完成复位"):
            raise ValueError("送膜失败：完成状态复位超时")
        return {"success": True, "message": "送膜完成"}

    @action(description="加热启动")
    def start_heating(self) -> Dict[str, Any]:
        """加热启动：写 Start_Heating_Trigger 触发，等待 Start_Heating_Complete 完成后复位。"""
        logger.info("加热启动...")
        self.set_node_value("Start_Heating_Trigger", True)
        if not self._wait_until_true("Start_Heating_Complete", description="加热启动完成"):
            raise ValueError("加热启动失败：动作未完成")
        self.set_node_value("Start_Heating_Trigger", False)
        if not self._wait_until_false("Start_Heating_Complete", description="加热启动完成复位"):
            raise ValueError("加热启动失败：完成状态复位超时")
        return {"success": True, "message": "加热启动完成"}

    @action(description="切割")
    def cut(self) -> Dict[str, Any]:
        """切割：写 Cut_Trigger 触发，等待 Cut_Complete 完成后复位。"""
        logger.info("切割...")
        self.set_node_value("Cut_Trigger", True)
        if not self._wait_until_true("Cut_Complete", description="切割完成"):
            raise ValueError("切割失败：动作未完成")
        self.set_node_value("Cut_Trigger", False)
        if not self._wait_until_false("Cut_Complete", description="切割完成复位"):
            raise ValueError("切割失败：完成状态复位超时")
        return {"success": True, "message": "切割完成"}

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
    def sealing_completed(self) -> bool:
        """封膜完成（读节点 Sealing_Completed）。"""
        v = self.get_node_value("Sealing_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def heating_completed(self) -> bool:
        """加热完成（读节点 Heating_Completed）。"""
        v = self.get_node_value("Heating_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_sealing_temperature(self) -> float:
        """实际封膜温度（读节点 Current_Sealing_Temperature）。"""
        v = self.get_node_value("Current_Sealing_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_sealing_time(self) -> float:
        """实际封膜时间（读节点 Current_Sealing_Time）。"""
        v = self.get_node_value("Current_Sealing_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_film_feed_length(self) -> int:
        """实际送膜长度（读节点 Current_Film_Feed_Length）。"""
        v = self.get_node_value("Current_Film_Feed_Length")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_pressure(self) -> float:
        """实际压力（读节点 Current_Pressure）。"""
        v = self.get_node_value("Current_Pressure")
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
