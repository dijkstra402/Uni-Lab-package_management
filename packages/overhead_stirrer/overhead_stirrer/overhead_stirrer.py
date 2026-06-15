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

    @action(description="设置扭矩限制")
    def set_torque_limit(self, torque_limit: int = 0) -> Dict[str, Any]:
        """
        设置扭矩限制。

        Args:
            torque_limit[设置扭矩限制]: 设置扭矩限制。
        """
        pass

    @action(description="设置转速上限")
    def set_speed_upper_limit(self, speed_upper_limit: int = 0) -> Dict[str, Any]:
        """
        设置转速上限。

        Args:
            speed_upper_limit[设置转速上限]: 设置转速上限。
        """
        pass

    @action(description="设置安全保护")
    def set_safety_protection(self, safety_protection: int = 0) -> Dict[str, Any]:
        """
        设置安全保护。

        Args:
            safety_protection[设置安全保护]: 设置安全保护。
        """
        pass

    @action(description="搅拌")
    def stir(self, stir_speed: int = 0, stir_time: int = 0, stir_mode: int = 0, impeller_height: int = 0) -> Dict[str, Any]:
        """
        搅拌。

        Args:
            stir_speed[搅拌速度设置]: 搅拌速度设置。
            stir_time[搅拌时间设置]: 搅拌时间设置。
            stir_mode[搅拌模式设置]: 搅拌模式设置。
            impeller_height[搅拌桨高度设置]: 搅拌桨高度设置。
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
    def current_speed(self) -> int:
        """当前速度显示。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_time(self) -> int:
        """当前时间显示。"""
        return self.data.get("current_time", 0)

    @property
    @topic_config()
    def current_height(self) -> int:
        """当前高度显示。"""
        return self.data.get("current_height", 0)

    @property
    @topic_config()
    def current_torque(self) -> int:
        """当前扭矩显示。"""
        return self.data.get("current_torque", 0)
