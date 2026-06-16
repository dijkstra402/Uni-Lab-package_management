"""
臭氧消毒机 — 标准设备类模板 (Device Class Template)

定义「臭氧消毒机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="ozone_sterilizer",
    category=["臭氧消毒机"],
    description="臭氧消毒机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="臭氧消毒机",
)
class OzoneSterilizer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "ozone_sterilizer"
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

    @action(description="设置消毒时间")
    def set_disinfection_time(self, disinfection_time: float = 0.0) -> Dict[str, Any]:
        """
        设置消毒时间。

        Args:
            disinfection_time[消毒时间]: 目标消毒时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置臭氧浓度")
    def set_ozone_concentration(self, ozone_concentration: float = 0.0) -> Dict[str, Any]:
        """
        设置臭氧浓度。

        Args:
            ozone_concentration[臭氧浓度]: 目标臭氧浓度（单位依设备量程而定）。
        """
        pass

    @action(description="消毒")
    def disinfect(self) -> Dict[str, Any]:
        """消毒。"""
        pass

    @action(description="消毒准备")
    def prepare_disinfection(self) -> Dict[str, Any]:
        """消毒准备。"""
        pass

    @action(description="消毒结束")
    def finish_disinfection(self) -> Dict[str, Any]:
        """消毒结束。"""
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
    def ozone_generator_state(self) -> bool:
        """臭氧发生器状态。"""
        return self.data.get("ozone_generator_state", False)

    @property
    @topic_config()
    def exhaust_treatment_state(self) -> bool:
        """尾气处理状态。"""
        return self.data.get("exhaust_treatment_state", False)

    @property
    @topic_config()
    def ventilation_system_state(self) -> bool:
        """通风系统状态。"""
        return self.data.get("ventilation_system_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_disinfection_time(self) -> float:
        """实际消毒时间。"""
        return self.data.get("current_disinfection_time", 0.0)

    @property
    @topic_config()
    def ozone_concentration_feedback(self) -> float:
        """臭氧浓度反馈。"""
        return self.data.get("ozone_concentration_feedback", 0.0)

    @property
    @topic_config()
    def disinfection_time_feedback(self) -> float:
        """消毒时间反馈。"""
        return self.data.get("disinfection_time_feedback", 0.0)
