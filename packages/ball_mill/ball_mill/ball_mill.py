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
    def set_mode(self, mode: int = 0) -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[设置运行模式]: 设置运行模式。
        """
        pass

    @action(description="设置球料比")
    def set_ball_to_powder_ratio(self, ball_to_powder_ratio: int = 0) -> Dict[str, Any]:
        """
        设置球料比。

        Args:
            ball_to_powder_ratio[设置球料比]: 设置球料比。
        """
        pass

    @action(description="设置正反转间隔")
    def set_fwd_rev_interval(self, fwd_rev_interval: int = 0) -> Dict[str, Any]:
        """
        设置正反转间隔。

        Args:
            fwd_rev_interval[设置正反转间隔]: 设置正反转间隔。
        """
        pass

    @action(description="研磨")
    def grind(self, grinding_time: int = 0, grinding_temperature: int = 0) -> Dict[str, Any]:
        """
        研磨。

        Args:
            grinding_time[研磨时间设置]: 研磨时间设置。
            grinding_temperature[研磨温度设置]: 研磨温度设置。
        """
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> int:
        """实际转速。"""
        return self.data.get("current_speed", 0)
