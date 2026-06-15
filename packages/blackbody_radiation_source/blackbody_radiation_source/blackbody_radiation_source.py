"""
黑体辐射源 — 标准设备类模板 (Device Class Template)

定义「黑体辐射源」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="blackbody_radiation_source",
    category=["黑体辐射源"],
    description="黑体辐射源标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="黑体辐射源",
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
        pass

    @action(description="设置辐射强度")
    def set_radiation_intensity(self, radiation_intensity: int = 0) -> Dict[str, Any]:
        """
        设置辐射强度。

        Args:
            radiation_intensity[设置辐射强度]: 设置辐射强度。
        """
        pass

    @action(description="运行倒计时")
    def run_countdown(self) -> Dict[str, Any]:
        """运行倒计时。"""
        pass

    @action(description="加热启动")
    def start_heating(self) -> Dict[str, Any]:
        """加热启动。"""
        pass

    @action(description="辐射输出")
    def radiation_output(self) -> Dict[str, Any]:
        """辐射输出。"""
        pass

    @action(description="辐射率校准")
    def calibrate_emissivity(self) -> Dict[str, Any]:
        """辐射率校准。"""
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
    def current_temperature(self) -> int:
        """实际温度。"""
        return self.data.get("current_temperature", 0)

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
