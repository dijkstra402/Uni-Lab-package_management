"""
球磨机 — 标准设备类模板 (Device Class Template)

定义「球磨机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="ball_mill",
    category=["球磨机"],
    description="球磨机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="球磨机",
)
class BallMill:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "ball_mill"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        pass

    @action(description="设置研磨时间")
    def set_grinding_time(self, grinding_time: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨时间。

        Args:
            grinding_time[研磨时间]: 目标研磨时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置球料比")
    def set_ball_to_powder_ratio(self, ball_to_powder_ratio: float = 0.0) -> Dict[str, Any]:
        """
        设置球料比。

        Args:
            ball_to_powder_ratio[球料比]: 目标球料比（单位依设备量程而定）。
        """
        pass

    @action(description="设置研磨温度")
    def set_grinding_temperature(self, grinding_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨温度。

        Args:
            grinding_temperature[研磨温度]: 目标研磨温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置正反转间隔")
    def set_fwd_rev_interval(self, fwd_rev_interval: float = 0.0) -> Dict[str, Any]:
        """
        设置正反转间隔。

        Args:
            fwd_rev_interval[正反转间隔]: 目标正反转间隔（单位依设备量程而定）。
        """
        pass

    @action(description="研磨")
    def grind(self) -> Dict[str, Any]:
        """研磨。"""
        pass

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态。"""
        return self.data.get("status", "idle")

    @property
    @topic_config()
    def fault(self) -> bool:
        """故障。"""
        return self.data.get("fault", False)

    @property
    @topic_config()
    def idle(self) -> bool:
        """空闲。"""
        return self.data.get("idle", False)

    @property
    @topic_config()
    def device_ready(self) -> bool:
        """设备就绪。"""
        return self.data.get("device_ready", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """实际转速。"""
        return self.data.get("current_speed", 0.0)
