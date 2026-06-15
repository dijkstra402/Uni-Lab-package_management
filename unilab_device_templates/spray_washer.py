"""
喷淋式清洗机 — 标准设备类模板 (Device Class Template)

定义「喷淋式清洗机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="spray_washer",
    category=["喷淋式清洗机"],
    description="喷淋式清洗机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="喷淋式清洗机",
)
class SprayWasher:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "spray_washer"
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
    def set_qing_xi_pressure(self, qing_xi_pressure: int = 0) -> Dict[str, Any]:
        """
        设置清洗压力。

        Args:
            qing_xi_pressure[设置清洗压力]: 设置清洗压力。
        """
        pass

    @action(description="设置喷淋压力")
    def set_spray_pressure(self, spray_pressure: int = 0) -> Dict[str, Any]:
        """
        设置喷淋压力。

        Args:
            spray_pressure[设置喷淋压力]: 设置喷淋压力。
        """
        pass

    @action(description="设置喷淋温度")
    def set_spray_temperature(self, spray_temperature: int = 0) -> Dict[str, Any]:
        """
        设置喷淋温度。

        Args:
            spray_temperature[设置喷淋温度]: 设置喷淋温度。
        """
        pass

    @action(description="设置喷淋时间")
    def set_spray_time(self, spray_time: int = 0) -> Dict[str, Any]:
        """
        设置喷淋时间。

        Args:
            spray_time[设置喷淋时间]: 设置喷淋时间。
        """
        pass

    @action(description="设置洗涤剂浓度")
    def set_detergent_concentration(self, detergent_concentration: int = 0) -> Dict[str, Any]:
        """
        设置洗涤剂浓度。

        Args:
            detergent_concentration[设置洗涤剂浓度]: 设置洗涤剂浓度。
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
    def spray_pressure_feedback(self) -> int:
        """喷淋压力反馈。"""
        return self.data.get("spray_pressure_feedback", 0)

    @property
    @topic_config()
    def spray_temperature_feedback(self) -> int:
        """喷淋温度反馈。"""
        return self.data.get("spray_temperature_feedback", 0)

    @property
    @topic_config()
    def spray_time_feedback(self) -> int:
        """喷淋时间反馈。"""
        return self.data.get("spray_time_feedback", 0)

    @property
    @topic_config()
    def detergent_concentration_feedback(self) -> int:
        """洗涤剂浓度反馈。"""
        return self.data.get("detergent_concentration_feedback", 0)
