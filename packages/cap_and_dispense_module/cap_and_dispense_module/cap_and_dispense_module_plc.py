"""
开关盖加液模块 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「开关盖加液模块」标准动作/属性映射为 PLC 节点读写：
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
    id="cap_and_dispense_module_plc",
    category=["合成制备仪器与设备", "液体分配设备", "开关盖加液模块"],
    description="开关盖加液模块 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="开关盖加液模块(PLC)",
)
class CapAndDispenseModulePLC(OpcUaClientWithSubscription):

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

    @action(description="设置加液体积")
    def set_add_volume(self, add_volume: float = 0.0) -> Dict[str, Any]:
        """设置加液体积：写入设定值节点 Add_Volume_Setpoint。"""
        self.set_node_value("Add_Volume_Setpoint", add_volume)
        return {"success": True, "message": "设置加液体积已下发", "add_volume": add_volume}

    @action(description="设置开盖高度")
    def set_cap_height(self, cap_height: float = 0.0) -> Dict[str, Any]:
        """设置开盖高度：写入设定值节点 Cap_Height_Setpoint。"""
        self.set_node_value("Cap_Height_Setpoint", cap_height)
        return {"success": True, "message": "设置开盖高度已下发", "cap_height": cap_height}

    @action(description="设置关盖扭矩")
    def set_cap_torque(self, cap_torque: float = 0.0) -> Dict[str, Any]:
        """设置关盖扭矩：写入设定值节点 Cap_Torque_Setpoint。"""
        self.set_node_value("Cap_Torque_Setpoint", cap_torque)
        return {"success": True, "message": "设置关盖扭矩已下发", "cap_torque": cap_torque}

    @action(description="设置容器位置")
    def set_container_position(self, container_position: float = 0.0) -> Dict[str, Any]:
        """设置容器位置：写入设定值节点 Container_Position_Setpoint。"""
        self.set_node_value("Container_Position_Setpoint", container_position)
        return {"success": True, "message": "设置容器位置已下发", "container_position": container_position}

    @action(description="开盖")
    def open_cap(self) -> Dict[str, Any]:
        """开盖：写 Open_Cap_Trigger 触发，等待 Open_Cap_Complete 完成后复位。"""
        logger.info("开盖...")
        self.set_node_value("Open_Cap_Trigger", True)
        if not self._wait_until_true("Open_Cap_Complete", description="开盖完成"):
            raise ValueError("开盖失败：动作未完成")
        self.set_node_value("Open_Cap_Trigger", False)
        if not self._wait_until_false("Open_Cap_Complete", description="开盖完成复位"):
            raise ValueError("开盖失败：完成状态复位超时")
        return {"success": True, "message": "开盖完成"}

    @action(description="关盖")
    def close_cap(self) -> Dict[str, Any]:
        """关盖：写 Close_Cap_Trigger 触发，等待 Close_Cap_Complete 完成后复位。"""
        logger.info("关盖...")
        self.set_node_value("Close_Cap_Trigger", True)
        if not self._wait_until_true("Close_Cap_Complete", description="关盖完成"):
            raise ValueError("关盖失败：动作未完成")
        self.set_node_value("Close_Cap_Trigger", False)
        if not self._wait_until_false("Close_Cap_Complete", description="关盖完成复位"):
            raise ValueError("关盖失败：完成状态复位超时")
        return {"success": True, "message": "关盖完成"}

    @action(description="加液")
    def add_liquid(self) -> Dict[str, Any]:
        """加液：写 Add_Liquid_Trigger 触发，等待 Add_Liquid_Complete 完成后复位。"""
        logger.info("加液...")
        self.set_node_value("Add_Liquid_Trigger", True)
        if not self._wait_until_true("Add_Liquid_Complete", description="加液完成"):
            raise ValueError("加液失败：动作未完成")
        self.set_node_value("Add_Liquid_Trigger", False)
        if not self._wait_until_false("Add_Liquid_Complete", description="加液完成复位"):
            raise ValueError("加液失败：完成状态复位超时")
        return {"success": True, "message": "加液完成"}

    @action(description="定位")
    def position(self) -> Dict[str, Any]:
        """定位：写 Position_Trigger 触发，等待 Position_Complete 完成后复位。"""
        logger.info("定位...")
        self.set_node_value("Position_Trigger", True)
        if not self._wait_until_true("Position_Complete", description="定位完成"):
            raise ValueError("定位失败：动作未完成")
        self.set_node_value("Position_Trigger", False)
        if not self._wait_until_false("Position_Complete", description="定位完成复位"):
            raise ValueError("定位失败：完成状态复位超时")
        return {"success": True, "message": "定位完成"}

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
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_add_volume(self) -> float:
        """实际加液体积（读节点 Current_Add_Volume）。"""
        v = self.get_node_value("Current_Add_Volume")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_cap_height(self) -> float:
        """实际开盖高度（读节点 Current_Cap_Height）。"""
        v = self.get_node_value("Current_Cap_Height")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_cap_torque(self) -> float:
        """实际关盖扭矩（读节点 Current_Cap_Torque）。"""
        v = self.get_node_value("Current_Cap_Torque")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_container_position(self) -> float:
        """实际容器位置（读节点 Current_Container_Position）。"""
        v = self.get_node_value("Current_Container_Position")
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
