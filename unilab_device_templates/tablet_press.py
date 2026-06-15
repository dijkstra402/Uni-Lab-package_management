"""
压片机 — 标准设备类模板 (Device Class Template)

定义「压片机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="tablet_press",
    category=["压片机"],
    description="压片机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="压片机",
)
class TabletPress:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "tablet_press"
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

    @action(description="设置压制压力")
    def set_pressing_pressure(self, pressing_pressure: int = 0) -> Dict[str, Any]:
        """
        设置压制压力。

        Args:
            pressing_pressure[设置压制压力]: 设置压制压力。
        """
        pass

    @action(description="设置压制时间")
    def set_pressing_time(self, pressing_time: int = 0) -> Dict[str, Any]:
        """
        设置压制时间。

        Args:
            pressing_time[设置压制时间]: 设置压制时间。
        """
        pass

    @action(description="设置保压时间")
    def set_holding_time(self, holding_time: int = 0) -> Dict[str, Any]:
        """
        设置保压时间。

        Args:
            holding_time[设置保压时间]: 设置保压时间。
        """
        pass

    @action(description="设置泄压速率")
    def set_depressurize_rate(self, depressurize_rate: int = 0) -> Dict[str, Any]:
        """
        设置泄压速率。

        Args:
            depressurize_rate[设置泄压速率]: 设置泄压速率。
        """
        pass

    @action(description="设置压模温度")
    def set_mold_temperature(self, mold_temperature: int = 0) -> Dict[str, Any]:
        """
        设置压模温度。

        Args:
            mold_temperature[设置压模温度]: 设置压模温度。
        """
        pass

    @action(description="设置样品直径")
    def set_sample_diameter(self, sample_diameter: int = 0) -> Dict[str, Any]:
        """
        设置样品直径。

        Args:
            sample_diameter[设置样品直径]: 设置样品直径。
        """
        pass

    @action(description="设置压制次数")
    def set_pressing_count(self, pressing_count: int = 0) -> Dict[str, Any]:
        """
        设置压制次数。

        Args:
            pressing_count[设置压制次数]: 设置压制次数。
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

    @property
    @topic_config()
    def current_pressure(self) -> int:
        """实际压力监测。"""
        return self.data.get("current_pressure", 0)
