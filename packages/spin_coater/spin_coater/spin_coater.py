"""
均胶机 — 标准设备类模板 (Device Class Template)

定义「均胶机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="spin_coater",
    category=["均胶机"],
    description="均胶机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="均胶机",
)
class SpinCoater:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "spin_coater"
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

    @action(description="设置低速时间")
    def set_low_speed_time(self, low_speed_time: int = 0) -> Dict[str, Any]:
        """
        设置低速时间。

        Args:
            low_speed_time[设置低速时间]: 设置低速时间。
        """
        pass

    @action(description="设置高速时间")
    def set_high_speed_time(self, high_speed_time: int = 0) -> Dict[str, Any]:
        """
        设置高速时间。

        Args:
            high_speed_time[设置高速时间]: 设置高速时间。
        """
        pass

    @action(description="设置加速度")
    def set_acceleration(self, acceleration: int = 0) -> Dict[str, Any]:
        """
        设置加速度。

        Args:
            acceleration[设置加速度]: 设置加速度。
        """
        pass

    @action(description="设置减速度")
    def set_deceleration(self, deceleration: int = 0) -> Dict[str, Any]:
        """
        设置减速度。

        Args:
            deceleration[设置减速度]: 设置减速度。
        """
        pass

    @action(description="设置样品尺寸")
    def set_sample_size(self, sample_size: int = 0) -> Dict[str, Any]:
        """
        设置样品尺寸。

        Args:
            sample_size[设置样品尺寸]: 设置样品尺寸。
        """
        pass

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
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
