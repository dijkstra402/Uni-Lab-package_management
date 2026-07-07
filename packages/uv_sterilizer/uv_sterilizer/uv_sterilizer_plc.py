"""
紫外消毒机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「紫外消毒机」标准动作/属性映射为 PLC 节点读写：
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
    id="uv_sterilizer_plc",
    category=["紫外消毒机"],
    description="紫外消毒机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="紫外消毒机(PLC)",
)
class UvSterilizerPLC(OpcUaClientWithSubscription):

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

    @action(description="设置消毒时间")
    def set_disinfection_time(self, disinfection_time: float = 0.0) -> Dict[str, Any]:
        """设置消毒时间：写入设定值节点 Disinfection_Time_Setpoint。"""
        self.set_node_value("Disinfection_Time_Setpoint", disinfection_time)
        return {"success": True, "message": "设置消毒时间已下发", "disinfection_time": disinfection_time}

    @action(description="设置紫外灯功率")
    def set_uv_lamp_power(self, uv_lamp_power: float = 0.0) -> Dict[str, Any]:
        """设置紫外灯功率：写入设定值节点 Uv_Lamp_Power_Setpoint。"""
        self.set_node_value("Uv_Lamp_Power_Setpoint", uv_lamp_power)
        return {"success": True, "message": "设置紫外灯功率已下发", "uv_lamp_power": uv_lamp_power}

    @action(description="消毒")
    def disinfect(self) -> Dict[str, Any]:
        """消毒：写 Disinfect_Trigger 触发，等待 Disinfect_Complete 完成后复位。"""
        logger.info("消毒...")
        self.set_node_value("Disinfect_Trigger", True)
        if not self._wait_until_true("Disinfect_Complete", description="消毒完成"):
            raise ValueError("消毒失败：动作未完成")
        self.set_node_value("Disinfect_Trigger", False)
        if not self._wait_until_false("Disinfect_Complete", description="消毒完成复位"):
            raise ValueError("消毒失败：完成状态复位超时")
        return {"success": True, "message": "消毒完成"}

    @action(description="消毒准备")
    def prepare_disinfection(self) -> Dict[str, Any]:
        """消毒准备：写 Prepare_Disinfection_Trigger 触发，等待 Prepare_Disinfection_Complete 完成后复位。"""
        logger.info("消毒准备...")
        self.set_node_value("Prepare_Disinfection_Trigger", True)
        if not self._wait_until_true("Prepare_Disinfection_Complete", description="消毒准备完成"):
            raise ValueError("消毒准备失败：动作未完成")
        self.set_node_value("Prepare_Disinfection_Trigger", False)
        if not self._wait_until_false("Prepare_Disinfection_Complete", description="消毒准备完成复位"):
            raise ValueError("消毒准备失败：完成状态复位超时")
        return {"success": True, "message": "消毒准备完成"}

    @action(description="消毒结束")
    def finish_disinfection(self) -> Dict[str, Any]:
        """消毒结束：写 Finish_Disinfection_Trigger 触发，等待 Finish_Disinfection_Complete 完成后复位。"""
        logger.info("消毒结束...")
        self.set_node_value("Finish_Disinfection_Trigger", True)
        if not self._wait_until_true("Finish_Disinfection_Complete", description="消毒结束完成"):
            raise ValueError("消毒结束失败：动作未完成")
        self.set_node_value("Finish_Disinfection_Trigger", False)
        if not self._wait_until_false("Finish_Disinfection_Complete", description="消毒结束完成复位"):
            raise ValueError("消毒结束失败：完成状态复位超时")
        return {"success": True, "message": "消毒结束完成"}

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
    def lamp_door_state(self) -> bool:
        """灯门状态（读节点 Lamp_Door_State）。"""
        v = self.get_node_value("Lamp_Door_State")
        return v if v is not None else False

    @property
    @topic_config()
    def radiation_shield_state(self) -> bool:
        """辐射防护状态（读节点 Radiation_Shield_State）。"""
        v = self.get_node_value("Radiation_Shield_State")
        return v if v is not None else False

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_disinfection_time(self) -> float:
        """实际消毒时间（读节点 Current_Disinfection_Time）。"""
        v = self.get_node_value("Current_Disinfection_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def uv_lamp_power_feedback(self) -> float:
        """紫外灯功率反馈（读节点 Uv_Lamp_Power_Feedback）。"""
        v = self.get_node_value("Uv_Lamp_Power_Feedback")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def disinfection_time_feedback(self) -> float:
        """消毒时间反馈（读节点 Disinfection_Time_Feedback）。"""
        v = self.get_node_value("Disinfection_Time_Feedback")
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
