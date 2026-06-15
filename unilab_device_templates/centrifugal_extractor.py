"""
离心萃取机 — 标准设备类模板 (Device Class Template)

定义「离心萃取机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="centrifugal_extractor",
    category=["离心萃取机"],
    description="离心萃取机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="离心萃取机",
)
class CentrifugalExtractor:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "centrifugal_extractor"
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

    @action(description="设置运行时间")
    def set_run_time(self, run_time: int = 0) -> Dict[str, Any]:
        """
        设置运行时间。

        Args:
            run_time[设置运行时间]: 设置运行时间。
        """
        pass

    @action(description="设置转速")
    def set_speed(self, speed: int = 0) -> Dict[str, Any]:
        """
        设置转速。

        Args:
            speed[设置转速]: 设置转速。
        """
        pass

    @action(description="设置分离时间")
    def set_separation_time(self, separation_time: int = 0) -> Dict[str, Any]:
        """
        设置分离时间。

        Args:
            separation_time[设置分离时间]: 设置分离时间。
        """
        pass

    @action(description="设置进料流量")
    def set_feed_flow(self, feed_flow: int = 0) -> Dict[str, Any]:
        """
        设置进料流量。

        Args:
            feed_flow[设置进料流量]: 设置进料流量。
        """
        pass

    @action(description="设置轻重相界面")
    def set_phase_interface(self, phase_interface: int = 0) -> Dict[str, Any]:
        """
        设置轻重相界面。

        Args:
            phase_interface[设置轻重相界面]: 设置轻重相界面。
        """
        pass

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行。"""
        pass

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
        pass

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位。"""
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
    def li_xin_on_state(self) -> bool:
        """离心开启状态。"""
        return self.data.get("li_xin_on_state", False)

    @property
    @topic_config()
    def feeding_state(self) -> bool:
        """进料状态。"""
        return self.data.get("feeding_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_run_time(self) -> int:
        """实际运行时间。"""
        return self.data.get("current_run_time", 0)

    @property
    @topic_config()
    def current_speed(self) -> int:
        """实际转速。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_separation_time(self) -> int:
        """实际分离时间。"""
        return self.data.get("current_separation_time", 0)

    @property
    @topic_config()
    def current_feed_flow(self) -> int:
        """实际进料流量。"""
        return self.data.get("current_feed_flow", 0)

    @property
    @topic_config()
    def current_phase_interface(self) -> int:
        """实际轻重相界面。"""
        return self.data.get("current_phase_interface", 0)
