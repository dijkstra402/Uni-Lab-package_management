"""
真空吸液系统 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「真空吸液系统」标准动作/属性映射为 PLC 节点读写：
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
    id="vacuum_aspiration_system_plc",
    category=["合成制备仪器与设备", "液体分配设备", "真空吸液系统"],
    description="真空吸液系统 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="真空吸液系统(PLC)",
)
class VacuumAspirationSystemPLC(OpcUaClientWithSubscription):

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

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """设置真空度：写入设定值节点 Vacuum_Setpoint。"""
        self.set_node_value("Vacuum_Setpoint", vacuum)
        return {"success": True, "message": "设置真空度已下发", "vacuum": vacuum}

    @action(description="设置吸液时间")
    def set_aspirate_time(self, aspirate_time: float = 0.0) -> Dict[str, Any]:
        """设置吸液时间：写入设定值节点 Aspirate_Time_Setpoint。"""
        self.set_node_value("Aspirate_Time_Setpoint", aspirate_time)
        return {"success": True, "message": "设置吸液时间已下发", "aspirate_time": aspirate_time}

    @action(description="设置吸液体积")
    def set_aspirate_volume(self, aspirate_volume: float = 0.0) -> Dict[str, Any]:
        """设置吸液体积：写入设定值节点 Aspirate_Volume_Setpoint。"""
        self.set_node_value("Aspirate_Volume_Setpoint", aspirate_volume)
        return {"success": True, "message": "设置吸液体积已下发", "aspirate_volume": aspirate_volume}

    @action(description="吸液启动")
    def start_draw_liquid(self) -> Dict[str, Any]:
        """吸液启动：写 Start_Draw_Liquid_Trigger 触发，等待 Start_Draw_Liquid_Complete 完成后复位。"""
        logger.info("吸液启动...")
        self.set_node_value("Start_Draw_Liquid_Trigger", True)
        if not self._wait_until_true("Start_Draw_Liquid_Complete", description="吸液启动完成"):
            raise ValueError("吸液启动失败：动作未完成")
        self.set_node_value("Start_Draw_Liquid_Trigger", False)
        if not self._wait_until_false("Start_Draw_Liquid_Complete", description="吸液启动完成复位"):
            raise ValueError("吸液启动失败：完成状态复位超时")
        return {"success": True, "message": "吸液启动完成"}

    @action(description="真空启动")
    def start_vacuum(self) -> Dict[str, Any]:
        """真空启动：写 Start_Vacuum_Trigger 触发，等待 Start_Vacuum_Complete 完成后复位。"""
        logger.info("真空启动...")
        self.set_node_value("Start_Vacuum_Trigger", True)
        if not self._wait_until_true("Start_Vacuum_Complete", description="真空启动完成"):
            raise ValueError("真空启动失败：动作未完成")
        self.set_node_value("Start_Vacuum_Trigger", False)
        if not self._wait_until_false("Start_Vacuum_Complete", description="真空启动完成复位"):
            raise ValueError("真空启动失败：完成状态复位超时")
        return {"success": True, "message": "真空启动完成"}

    @action(description="排液")
    def dispense(self) -> Dict[str, Any]:
        """排液：写 Dispense_Trigger 触发，等待 Dispense_Complete 完成后复位。"""
        logger.info("排液...")
        self.set_node_value("Dispense_Trigger", True)
        if not self._wait_until_true("Dispense_Complete", description="排液完成"):
            raise ValueError("排液失败：动作未完成")
        self.set_node_value("Dispense_Trigger", False)
        if not self._wait_until_false("Dispense_Complete", description="排液完成复位"):
            raise ValueError("排液失败：完成状态复位超时")
        return {"success": True, "message": "排液完成"}

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗：写 Clean_Trigger 触发，等待 Clean_Complete 完成后复位。"""
        logger.info("清洗...")
        self.set_node_value("Clean_Trigger", True)
        if not self._wait_until_true("Clean_Complete", description="清洗完成"):
            raise ValueError("清洗失败：动作未完成")
        self.set_node_value("Clean_Trigger", False)
        if not self._wait_until_false("Clean_Complete", description="清洗完成复位"):
            raise ValueError("清洗失败：完成状态复位超时")
        return {"success": True, "message": "清洗完成"}

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
    def vacuum_completed(self) -> bool:
        """真空完成（读节点 Vacuum_Completed）。"""
        v = self.get_node_value("Vacuum_Completed")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """实际真空度（读节点 Current_Vacuum）。"""
        v = self.get_node_value("Current_Vacuum")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_aspirate_time(self) -> float:
        """实际吸液时间（读节点 Current_Aspirate_Time）。"""
        v = self.get_node_value("Current_Aspirate_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_aspirate_volume(self) -> float:
        """实际吸液体积（读节点 Current_Aspirate_Volume）。"""
        v = self.get_node_value("Current_Aspirate_Volume")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def filter_state(self) -> int:
        """过滤器状态（读节点 Filter_State）。"""
        v = self.get_node_value("Filter_State")
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
