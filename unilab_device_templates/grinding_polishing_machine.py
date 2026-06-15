"""
磨抛机 — 标准设备类模板 (Device Class Template)

定义「磨抛机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="grinding_polishing_machine",
    category=["磨抛机"],
    description="磨抛机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="磨抛机",
)
class GrindingPolishingMachine:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "grinding_polishing_machine"
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

    @action(description="设置研磨转速")
    def set_grinding_speed(self, grinding_speed: int = 0) -> Dict[str, Any]:
        """
        设置研磨转速。

        Args:
            grinding_speed[设置研磨转速]: 设置研磨转速。
        """
        pass

    @action(description="设置抛光转速")
    def set_polishing_speed(self, polishing_speed: int = 0) -> Dict[str, Any]:
        """
        设置抛光转速。

        Args:
            polishing_speed[设置抛光转速]: 设置抛光转速。
        """
        pass

    @action(description="设置研磨时间")
    def set_grinding_time(self, grinding_time: int = 0) -> Dict[str, Any]:
        """
        设置研磨时间。

        Args:
            grinding_time[设置研磨时间]: 设置研磨时间。
        """
        pass

    @action(description="设置抛光时间")
    def set_polishing_time(self, polishing_time: int = 0) -> Dict[str, Any]:
        """
        设置抛光时间。

        Args:
            polishing_time[设置抛光时间]: 设置抛光时间。
        """
        pass

    @action(description="设置磨抛压力")
    def set_polishing_pressure(self, polishing_pressure: int = 0) -> Dict[str, Any]:
        """
        设置磨抛压力。

        Args:
            polishing_pressure[设置磨抛压力]: 设置磨抛压力。
        """
        pass

    @action(description="设置样品夹持力")
    def set_sample_clamp_force(self, sample_clamp_force: int = 0) -> Dict[str, Any]:
        """
        设置样品夹持力。

        Args:
            sample_clamp_force[设置样品夹持力]: 设置样品夹持力。
        """
        pass

    @action(description="设置磨抛精度")
    def set_polishing_precision(self, polishing_precision: int = 0) -> Dict[str, Any]:
        """
        设置磨抛精度。

        Args:
            polishing_precision[设置磨抛精度]: 设置磨抛精度。
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
