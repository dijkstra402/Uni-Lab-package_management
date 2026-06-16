"""
等离子体清洗机 — 标准设备类模板 (Device Class Template)

定义「等离子体清洗机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="plasma_cleaner",
    category=["等离子体清洗机"],
    description="等离子体清洗机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="等离子体清洗机",
)
class PlasmaCleaner:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "plasma_cleaner"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        pass

    @action(description="设置清洗时间")
    def set_cleaning_time(self, cleaning_time: float = 0.0) -> Dict[str, Any]:
        """
        设置清洗时间。

        Args:
            cleaning_time[清洗时间]: 目标清洗时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置清洗温度")
    def set_cleaning_temperature(self, cleaning_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置清洗温度。

        Args:
            cleaning_temperature[清洗温度]: 目标清洗温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置清洗压力")
    def set_cleaning_pressure(self, cleaning_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置清洗压力。

        Args:
            cleaning_pressure[清洗压力]: 目标清洗压力（单位依设备量程而定）。
        """
        pass

    @action(description="设置等离子功率")
    def set_plasma_power(self, plasma_power: float = 0.0) -> Dict[str, Any]:
        """
        设置等离子功率。

        Args:
            plasma_power[等离子功率]: 目标等离子功率（单位依设备量程而定）。
        """
        pass

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[真空度]: 目标真空度（单位依设备量程而定）。
        """
        pass

    @action(description="设置处理时间")
    def set_treatment_time(self, treatment_time: float = 0.0) -> Dict[str, Any]:
        """
        设置处理时间。

        Args:
            treatment_time[处理时间]: 目标处理时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置气体流量")
    def set_gas_flow(self, gas_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置气体流量。

        Args:
            gas_flow[气体流量]: 目标气体流量（单位依设备量程而定）。
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
    def idle(self) -> bool:
        """空闲。"""
        return self.data.get("idle", False)

    @property
    @topic_config()
    def device_ready(self) -> bool:
        """设备就绪。"""
        return self.data.get("device_ready", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_cleaning_time(self) -> float:
        """实际清洗时间。"""
        return self.data.get("current_cleaning_time", 0.0)

    @property
    @topic_config()
    def plasma_power_feedback(self) -> float:
        """等离子功率反馈。"""
        return self.data.get("plasma_power_feedback", 0.0)

    @property
    @topic_config()
    def vacuum_feedback(self) -> float:
        """真空度反馈。"""
        return self.data.get("vacuum_feedback", 0.0)

    @property
    @topic_config()
    def treatment_time_feedback(self) -> float:
        """处理时间反馈。"""
        return self.data.get("treatment_time_feedback", 0.0)

    @property
    @topic_config()
    def gas_flow_feedback(self) -> float:
        """气体流量反馈。"""
        return self.data.get("gas_flow_feedback", 0.0)
