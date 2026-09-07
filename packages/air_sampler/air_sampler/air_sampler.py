"""
大气采样器 — 标准设备类模板 (Device Class Template)

定义「大气采样器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="air_sampler",
    category=["样品处理仪器与设备", "提取设备", "大气采样器"],
    description="大气采样器标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="大气采样器",
)
class AirSampler:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "air_sampler"
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

    @action(description="设置采样流量")
    def set_sampling_flow(self, sampling_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置采样流量。

        Args:
            sampling_flow[采样流量]: 目标采样流量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置采样时间")
    def set_sampling_time(self, sampling_time: float = 0.0) -> Dict[str, Any]:
        """
        设置采样时间。

        Args:
            sampling_time[采样时间]: 目标采样时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置采样压力")
    def set_sampling_pressure(self, sampling_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置采样压力。

        Args:
            sampling_pressure[采样压力]: 目标采样压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置采样温度")
    def set_sampling_temperature(self, sampling_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置采样温度。

        Args:
            sampling_temperature[采样温度]: 目标采样温度（单位依设备量程而定）。
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
    def flow_stable_state(self) -> bool:
        """流量稳定状态。"""
        return self.data.get("flow_stable_state", False)

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
    def current_sampling_flow(self) -> float:
        """实际采样流量。"""
        return self.data.get("current_sampling_flow", 0.0)

    @property
    @topic_config()
    def current_sampling_time(self) -> float:
        """实际采样时间。"""
        return self.data.get("current_sampling_time", 0.0)

    @property
    @topic_config()
    def current_sampling_pressure(self) -> float:
        """实际采样压力。"""
        return self.data.get("current_sampling_pressure", 0.0)

    @property
    @topic_config()
    def current_sampling_temperature(self) -> float:
        """实际采样温度。"""
        return self.data.get("current_sampling_temperature", 0.0)

    @property
    @topic_config()
    def sampling_state(self) -> bool:
        """采样状态。"""
        return self.data.get("sampling_state", False)
