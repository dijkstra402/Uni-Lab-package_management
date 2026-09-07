"""
切片机 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「切片机」标准动作/属性映射为 PLC 节点读写：
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
    id="microtome_plc",
    category=["样品处理仪器与设备", "样品制备设备", "切片机"],
    description="切片机 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="切片机(PLC)",
)
class MicrotomePLC(OpcUaClientWithSubscription):

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

    @action(description="设置切片厚度")
    def set_slice_thickness(self, slice_thickness: float = 0.0) -> Dict[str, Any]:
        """设置切片厚度：写入设定值节点 Slice_Thickness_Setpoint。"""
        self.set_node_value("Slice_Thickness_Setpoint", slice_thickness)
        return {"success": True, "message": "设置切片厚度已下发", "slice_thickness": slice_thickness}

    @action(description="设置切片速度")
    def set_slice_speed(self, slice_speed: float = 0.0) -> Dict[str, Any]:
        """设置切片速度：写入设定值节点 Slice_Speed_Setpoint。"""
        self.set_node_value("Slice_Speed_Setpoint", slice_speed)
        return {"success": True, "message": "设置切片速度已下发", "slice_speed": slice_speed}

    @action(description="设置进给量")
    def set_feed_amount(self, feed_amount: int = 0) -> Dict[str, Any]:
        """设置进给量：写入设定值节点 Feed_Amount_Setpoint。"""
        self.set_node_value("Feed_Amount_Setpoint", feed_amount)
        return {"success": True, "message": "设置进给量已下发", "feed_amount": feed_amount}

    @action(description="设置刀架角度")
    def set_tool_holder_angle(self, tool_holder_angle: float = 0.0) -> Dict[str, Any]:
        """设置刀架角度：写入设定值节点 Tool_Holder_Angle_Setpoint。"""
        self.set_node_value("Tool_Holder_Angle_Setpoint", tool_holder_angle)
        return {"success": True, "message": "设置刀架角度已下发", "tool_holder_angle": tool_holder_angle}

    @action(description="设置样品转速")
    def set_sample_speed(self, sample_speed: float = 0.0) -> Dict[str, Any]:
        """设置样品转速：写入设定值节点 Sample_Speed_Setpoint。"""
        self.set_node_value("Sample_Speed_Setpoint", sample_speed)
        return {"success": True, "message": "设置样品转速已下发", "sample_speed": sample_speed}

    @action(description="设置切片精度")
    def set_slice_precision(self, slice_precision: int = 0) -> Dict[str, Any]:
        """设置切片精度：写入设定值节点 Slice_Precision_Setpoint。"""
        self.set_node_value("Slice_Precision_Setpoint", slice_precision)
        return {"success": True, "message": "设置切片精度已下发", "slice_precision": slice_precision}

    @action(description="设置切片数量")
    def set_slicing_count(self, slicing_count: int = 0) -> Dict[str, Any]:
        """设置切片数量：写入设定值节点 Slicing_Count_Setpoint。"""
        self.set_node_value("Slicing_Count_Setpoint", slicing_count)
        return {"success": True, "message": "设置切片数量已下发", "slicing_count": slicing_count}

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
    def slicing_interval_time(self) -> float:
        """切片间隔时间（读节点 Slicing_Interval_Time）。"""
        v = self.get_node_value("Slicing_Interval_Time")
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
