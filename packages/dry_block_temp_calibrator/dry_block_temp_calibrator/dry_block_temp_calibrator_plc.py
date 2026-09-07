"""
干体温度校正炉 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「干体温度校正炉」标准动作/属性映射为 PLC 节点读写：
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
    id="dry_block_temp_calibrator_plc",
    category=["加热、制冷及空气净化与调节设备", "固体浴", "干体温度校正炉"],
    description="干体温度校正炉 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="干体温度校正炉(PLC)",
)
class DryBlockTempCalibratorPLC(OpcUaClientWithSubscription):

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

    @action(description="设置温度")
    def set_temperature(self, temperature: float = 0.0) -> Dict[str, Any]:
        """设置温度：写入设定值节点 Temperature_Setpoint。"""
        self.set_node_value("Temperature_Setpoint", temperature)
        return {"success": True, "message": "设置温度已下发", "temperature": temperature}

    @action(description="设置恒温时间")
    def set_hold_time(self, hold_time: float = 0.0) -> Dict[str, Any]:
        """设置恒温时间：写入设定值节点 Hold_Time_Setpoint。"""
        self.set_node_value("Hold_Time_Setpoint", hold_time)
        return {"success": True, "message": "设置恒温时间已下发", "hold_time": hold_time}

    @action(description="运行倒计时")
    def run_countdown(self) -> Dict[str, Any]:
        """运行倒计时：写 Run_Countdown_Trigger 触发，等待 Run_Countdown_Complete 完成后复位。"""
        logger.info("运行倒计时...")
        self.set_node_value("Run_Countdown_Trigger", True)
        if not self._wait_until_true("Run_Countdown_Complete", description="运行倒计时完成"):
            raise ValueError("运行倒计时失败：动作未完成")
        self.set_node_value("Run_Countdown_Trigger", False)
        if not self._wait_until_false("Run_Countdown_Complete", description="运行倒计时完成复位"):
            raise ValueError("运行倒计时失败：完成状态复位超时")
        return {"success": True, "message": "运行倒计时完成"}

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

    @action(description="恒温")
    def hold_temperature(self) -> Dict[str, Any]:
        """恒温：写 Hold_Temperature_Trigger 触发，等待 Hold_Temperature_Complete 完成后复位。"""
        logger.info("恒温...")
        self.set_node_value("Hold_Temperature_Trigger", True)
        if not self._wait_until_true("Hold_Temperature_Complete", description="恒温完成"):
            raise ValueError("恒温失败：动作未完成")
        self.set_node_value("Hold_Temperature_Trigger", False)
        if not self._wait_until_false("Hold_Temperature_Complete", description="恒温完成复位"):
            raise ValueError("恒温失败：完成状态复位超时")
        return {"success": True, "message": "恒温完成"}

    @action(description="温度校正")
    def correct_temperature(self) -> Dict[str, Any]:
        """温度校正：写 Correct_Temperature_Trigger 触发，等待 Correct_Temperature_Complete 完成后复位。"""
        logger.info("温度校正...")
        self.set_node_value("Correct_Temperature_Trigger", True)
        if not self._wait_until_true("Correct_Temperature_Complete", description="温度校正完成"):
            raise ValueError("温度校正失败：动作未完成")
        self.set_node_value("Correct_Temperature_Trigger", False)
        if not self._wait_until_false("Correct_Temperature_Complete", description="温度校正完成复位"):
            raise ValueError("温度校正失败：完成状态复位超时")
        return {"success": True, "message": "温度校正完成"}

    @action(description="均匀性检测")
    def check_uniformity(self) -> Dict[str, Any]:
        """均匀性检测：写 Check_Uniformity_Trigger 触发，等待 Check_Uniformity_Complete 完成后复位。"""
        logger.info("均匀性检测...")
        self.set_node_value("Check_Uniformity_Trigger", True)
        if not self._wait_until_true("Check_Uniformity_Complete", description="均匀性检测完成"):
            raise ValueError("均匀性检测失败：动作未完成")
        self.set_node_value("Check_Uniformity_Trigger", False)
        if not self._wait_until_false("Check_Uniformity_Complete", description="均匀性检测完成复位"):
            raise ValueError("均匀性检测失败：完成状态复位超时")
        return {"success": True, "message": "均匀性检测完成"}

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
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """实际温度（读节点 Current_Temperature）。"""
        v = self.get_node_value("Current_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def run_time(self) -> float:
        """运行时间（读节点 Run_Time）。"""
        v = self.get_node_value("Run_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def remaining_time(self) -> float:
        """剩余时间（读节点 Remaining_Time）。"""
        v = self.get_node_value("Remaining_Time")
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
