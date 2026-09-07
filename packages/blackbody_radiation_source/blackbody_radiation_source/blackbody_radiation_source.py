"""
黑体辐射源 — 标准设备类模板 (Device Class Template)

定义「黑体辐射源」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="blackbody_radiation_source",
    category=["加热、制冷及空气净化与调节设备", "固体浴", "黑体辐射源"],
    description="黑体辐射源标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="黑体辐射源",
)
class BlackbodyRadiationSource:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "blackbody_radiation_source"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置温度")
    def set_temperature(self, temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置温度。

        Args:
            temperature[温度]: 目标温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置辐射率")
    def set_emissivity(self, emissivity: float = 0.0) -> Dict[str, Any]:
        """
        设置辐射率。

        Args:
            emissivity[辐射率]: 目标辐射率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置辐射强度")
    def set_radiation_intensity(self, radiation_intensity: float = 0.0) -> Dict[str, Any]:
        """
        设置辐射强度。

        Args:
            radiation_intensity[辐射强度]: 目标辐射强度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="运行倒计时")
    def run_countdown(self) -> Dict[str, Any]:
        """运行倒计时。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="加热启动")
    def start_heating(self) -> Dict[str, Any]:
        """加热启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="辐射输出")
    def radiation_output(self) -> Dict[str, Any]:
        """辐射输出。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="辐射率校准")
    def calibrate_emissivity(self) -> Dict[str, Any]:
        """辐射率校准。"""
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """实际温度。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def current_emissivity(self) -> int:
        """实际辐射率。"""
        return self.data.get("current_emissivity", 0)

    @property
    @topic_config()
    def radiation_intensity_feedback(self) -> int:
        """辐射强度反馈。"""
        return self.data.get("radiation_intensity_feedback", 0)

    @property
    @topic_config()
    def run_time(self) -> float:
        """运行时间。"""
        return self.data.get("run_time", 0.0)

    @property
    @topic_config()
    def remaining_time(self) -> float:
        """剩余时间。"""
        return self.data.get("remaining_time", 0.0)

    @property
    @topic_config()
    def radiation_stable_time(self) -> float:
        """辐射稳定时间。"""
        return self.data.get("radiation_stable_time", 0.0)

    @property
    @topic_config()
    def preheat_stable_time(self) -> float:
        """预热稳定时间。"""
        return self.data.get("preheat_stable_time", 0.0)
