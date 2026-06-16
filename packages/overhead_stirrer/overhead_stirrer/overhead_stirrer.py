"""
机械搅拌器 — 标准设备类模板 (Device Class Template)

定义「机械搅拌器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="overhead_stirrer",
    category=["机械搅拌器"],
    description="机械搅拌器标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="机械搅拌器",
)
class OverheadStirrer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "overhead_stirrer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置搅拌速度")
    def set_stir_speed(self, stir_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌速度。

        Args:
            stir_speed[搅拌速度]: 目标搅拌速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置搅拌时间")
    def set_stir_time(self, stir_time: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌时间。

        Args:
            stir_time[搅拌时间]: 目标搅拌时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置搅拌模式")
    def set_stir_mode(self, stir_mode: str = "") -> Dict[str, Any]:
        """
        设置搅拌模式。

        Args:
            stir_mode[搅拌模式]: 目标搅拌模式（具体取值由设备型号定义）。
        """
        pass

    @action(description="设置搅拌桨高度")
    def set_impeller_height(self, impeller_height: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌桨高度。

        Args:
            impeller_height[搅拌桨高度]: 目标搅拌桨高度（单位依设备量程而定）。
        """
        pass

    @action(description="设置扭矩限制")
    def set_torque_limit(self, torque_limit: float = 0.0) -> Dict[str, Any]:
        """
        设置扭矩限制。

        Args:
            torque_limit[扭矩限制]: 目标扭矩限制（单位依设备量程而定）。
        """
        pass

    @action(description="设置转速上限")
    def set_speed_upper_limit(self, speed_upper_limit: float = 0.0) -> Dict[str, Any]:
        """
        设置转速上限。

        Args:
            speed_upper_limit[转速上限]: 目标转速上限（单位依设备量程而定）。
        """
        pass

    @action(description="设置安全保护")
    def set_safety_protection(self, safety_protection: int = 0) -> Dict[str, Any]:
        """
        设置安全保护。

        Args:
            safety_protection[安全保护]: 目标安全保护（单位依设备量程而定）。
        """
        pass

    @action(description="搅拌")
    def stir(self) -> Dict[str, Any]:
        """搅拌。"""
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
    def lift_motor_state(self) -> bool:
        """升降电机状态。"""
        return self.data.get("lift_motor_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """当前速度显示。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示。"""
        return self.data.get("current_time", 0.0)

    @property
    @topic_config()
    def current_height(self) -> float:
        """当前高度显示。"""
        return self.data.get("current_height", 0.0)

    @property
    @topic_config()
    def current_torque(self) -> float:
        """当前扭矩显示。"""
        return self.data.get("current_torque", 0.0)
