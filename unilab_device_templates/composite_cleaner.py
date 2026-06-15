"""
复合型清洗机 — 标准设备类模板 (Device Class Template)

定义「复合型清洗机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="composite_cleaner",
    category=["复合型清洗机"],
    description="复合型清洗机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="复合型清洗机",
)
class CompositeCleaner:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "composite_cleaner"
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

    @action(description="设置清洗温度")
    def set_cleaning_temperature(self, cleaning_temperature: int = 0) -> Dict[str, Any]:
        """
        设置清洗温度。

        Args:
            cleaning_temperature[设置清洗温度]: 设置清洗温度。
        """
        pass

    @action(description="设置清洗压力")
    def set_cleaning_pressure(self, cleaning_pressure: int = 0) -> Dict[str, Any]:
        """
        设置清洗压力。

        Args:
            cleaning_pressure[设置清洗压力]: 设置清洗压力。
        """
        pass

    @action(description="设置主清洗功率")
    def set_main_wash_power(self, main_wash_power: int = 0) -> Dict[str, Any]:
        """
        设置主清洗功率。

        Args:
            main_wash_power[设置主清洗功率]: 设置主清洗功率。
        """
        pass

    @action(description="设置辅助清洗功率")
    def set_aux_wash_power(self, aux_wash_power: int = 0) -> Dict[str, Any]:
        """
        设置辅助清洗功率。

        Args:
            aux_wash_power[设置辅助清洗功率]: 设置辅助清洗功率。
        """
        pass

    @action(description="设置总清洗时间")
    def set_total_wash_time(self, total_wash_time: int = 0) -> Dict[str, Any]:
        """
        设置总清洗时间。

        Args:
            total_wash_time[设置总清洗时间]: 设置总清洗时间。
        """
        pass

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗。"""
        pass

    @action(description="清洗准备")
    def prepare_cleaning(self) -> Dict[str, Any]:
        """清洗准备。"""
        pass

    @action(description="清洗结束")
    def finish_cleaning(self) -> Dict[str, Any]:
        """清洗结束。"""
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
    def modules_sync_state(self) -> bool:
        """各模块协同状态。"""
        return self.data.get("modules_sync_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_cleaning_time(self) -> int:
        """实际清洗时间。"""
        return self.data.get("current_cleaning_time", 0)

    @property
    @topic_config()
    def main_wash_power_feedback(self) -> int:
        """主清洗功率反馈。"""
        return self.data.get("main_wash_power_feedback", 0)

    @property
    @topic_config()
    def aux_wash_power_feedback(self) -> int:
        """辅助清洗功率反馈。"""
        return self.data.get("aux_wash_power_feedback", 0)

    @property
    @topic_config()
    def total_wash_time_feedback(self) -> int:
        """总清洗时间反馈。"""
        return self.data.get("total_wash_time_feedback", 0)
