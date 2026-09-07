"""
索氏提取仪 — 标准设备类模板 (Device Class Template)

定义「索氏提取仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="soxhlet_extractor",
    category=["样品处理仪器与设备", "提取设备", "索氏提取仪"],
    description="索氏提取仪标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="索氏提取仪",
)
class SoxhletExtractor:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "soxhlet_extractor"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置运行时间")
    def set_run_time(self, run_time: float = 0.0) -> Dict[str, Any]:
        """
        设置运行时间。

        Args:
            run_time[运行时间]: 目标运行时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置加热温度")
    def set_heating_temperature(self, heating_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置加热温度。

        Args:
            heating_temperature[加热温度]: 目标加热温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置提取次数")
    def set_extraction_count(self, extraction_count: int = 0) -> Dict[str, Any]:
        """
        设置提取次数。

        Args:
            extraction_count[提取次数]: 目标提取次数（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置回流时间")
    def set_reflux_time(self, reflux_time: float = 0.0) -> Dict[str, Any]:
        """
        设置回流时间。

        Args:
            reflux_time[回流时间]: 目标回流时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位。"""
        raise NotImplementedError("请在设备包中实现该动作")

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
    def heating_state(self) -> bool:
        """加热状态。"""
        return self.data.get("heating_state", False)

    @property
    @topic_config()
    def reflux_state(self) -> bool:
        """回流状态。"""
        return self.data.get("reflux_state", False)

    @property
    @topic_config()
    def solvent_level_state(self) -> bool:
        """溶剂液位状态。"""
        return self.data.get("solvent_level_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_run_time(self) -> float:
        """实际运行时间。"""
        return self.data.get("current_run_time", 0.0)

    @property
    @topic_config()
    def current_heating_temperature(self) -> float:
        """实际加热温度。"""
        return self.data.get("current_heating_temperature", 0.0)

    @property
    @topic_config()
    def current_extraction_count(self) -> int:
        """实际提取次数。"""
        return self.data.get("current_extraction_count", 0)

    @property
    @topic_config()
    def current_reflux_time(self) -> float:
        """实际回流时间。"""
        return self.data.get("current_reflux_time", 0.0)
