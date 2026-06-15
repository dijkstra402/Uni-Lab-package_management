"""
振动固体加料模块 — 标准设备类模板 (Device Class Template)

定义「振动固体加料模块」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vibratory_solid_feeder",
    category=["振动固体加料模块"],
    description="振动固体加料模块标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="振动固体加料模块",
)
class VibratorySolidFeeder:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "vibratory_solid_feeder"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="加料")
    def feed(self, mode: int = 0, vibration_frequency: int = 0, vibration_amplitude: int = 0, feed_time: int = 0) -> Dict[str, Any]:
        """
        加料。

        Args:
            mode[运行模式设置]: 运行模式设置。
            vibration_frequency[振动频率设置]: 振动频率设置。
            vibration_amplitude[振动振幅设置]: 振动振幅设置。
            feed_time[加料时间设置]: 加料时间设置。
        """
        pass

    @action(description="清堵")
    def clear_clog(self, mode: int = 0, vibration_frequency: int = 0, vibration_amplitude: int = 0) -> Dict[str, Any]:
        """
        清堵。

        Args:
            mode[运行模式设置]: 运行模式设置。
            vibration_frequency[振动频率设置]: 振动频率设置。
            vibration_amplitude[振动振幅设置]: 振动振幅设置。
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
    def current_feed_amount(self) -> int:
        """实际加料量。"""
        return self.data.get("current_feed_amount", 0)

    @property
    @topic_config()
    def current_vibration_frequency(self) -> int:
        """实际振动频率。"""
        return self.data.get("current_vibration_frequency", 0)
