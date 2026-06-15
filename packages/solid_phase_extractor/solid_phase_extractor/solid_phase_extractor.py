"""
固相萃取设备 — 标准设备类模板 (Device Class Template)

定义「固相萃取设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="solid_phase_extractor",
    category=["固相萃取设备"],
    description="固相萃取设备标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="固相萃取设备",
)
class SolidPhaseExtractor:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "solid_phase_extractor"
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

    @action(description="设置萃取柱压力")
    def set_extraction_column_pressure(self, extraction_column_pressure: int = 0) -> Dict[str, Any]:
        """
        设置萃取柱压力。

        Args:
            extraction_column_pressure[设置萃取柱压力]: 设置萃取柱压力。
        """
        pass

    @action(description="设置洗脱液流量")
    def set_eluent_flow(self, eluent_flow: int = 0) -> Dict[str, Any]:
        """
        设置洗脱液流量。

        Args:
            eluent_flow[设置洗脱液流量]: 设置洗脱液流量。
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
    def column_pressure_protection_state(self) -> bool:
        """柱压保护状态。"""
        return self.data.get("column_pressure_protection_state", False)

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
    def current_extraction_column_pressure(self) -> int:
        """实际萃取柱压力。"""
        return self.data.get("current_extraction_column_pressure", 0)

    @property
    @topic_config()
    def current_eluent_flow(self) -> int:
        """实际洗脱液流量。"""
        return self.data.get("current_eluent_flow", 0)
