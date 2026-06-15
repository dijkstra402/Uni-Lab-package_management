"""
匀浆机 — 标准设备类模板 (Device Class Template)

定义「匀浆机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="blender_homogenizer",
    category=["匀浆机"],
    description="匀浆机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="匀浆机",
)
class BlenderHomogenizer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "blender_homogenizer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置脉冲间隔")
    def set_pulse_interval(self, pulse_interval: int = 0) -> Dict[str, Any]:
        """
        设置脉冲间隔。

        Args:
            pulse_interval[设置脉冲间隔]: 设置脉冲间隔。
        """
        pass

    @action(description="设置脉冲宽度")
    def set_pulse_width(self, pulse_width: int = 0) -> Dict[str, Any]:
        """
        设置脉冲宽度。

        Args:
            pulse_width[设置脉冲宽度]: 设置脉冲宽度。
        """
        pass

    @action(description="设置扭矩限制")
    def set_torque_limit(self, torque_limit: int = 0) -> Dict[str, Any]:
        """
        设置扭矩限制。

        Args:
            torque_limit[设置扭矩限制]: 设置扭矩限制。
        """
        pass

    @action(description="匀浆")
    def blend(self, blend_speed: int = 0, blend_time: int = 0, blend_mode: int = 0) -> Dict[str, Any]:
        """
        匀浆。

        Args:
            blend_speed[匀浆转速设置]: 匀浆转速设置。
            blend_time[匀浆时间设置]: 匀浆时间设置。
            blend_mode[匀浆模式设置]: 匀浆模式设置。
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
    def safety_lock_state(self) -> bool:
        """安全锁状态。"""
        return self.data.get("safety_lock_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> int:
        """当前转速显示。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_time(self) -> int:
        """当前时间显示。"""
        return self.data.get("current_time", 0)

    @property
    @topic_config()
    def current_torque(self) -> int:
        """当前扭矩显示。"""
        return self.data.get("current_torque", 0)
