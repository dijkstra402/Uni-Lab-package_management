"""
干体温度校正炉 — 标准设备类模板 (Device Class Template)

定义「干体温度校正炉」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="dry_block_temp_calibrator",
    category=["加热、制冷及空气净化与调节设备", "固体浴", "干体温度校正炉"],
    description="干体温度校正炉标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="干体温度校正炉",
)
class DryBlockTempCalibrator:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "dry_block_temp_calibrator"
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

    @action(description="设置恒温时间")
    def set_hold_time(self, hold_time: float = 0.0) -> Dict[str, Any]:
        """
        设置恒温时间。

        Args:
            hold_time[恒温时间]: 目标恒温时间（单位依设备量程而定）。
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

    @action(description="恒温")
    def hold_temperature(self) -> Dict[str, Any]:
        """恒温。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="温度校正")
    def correct_temperature(self) -> Dict[str, Any]:
        """温度校正。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="均匀性检测")
    def check_uniformity(self) -> Dict[str, Any]:
        """均匀性检测。"""
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
    def run_time(self) -> float:
        """运行时间。"""
        return self.data.get("run_time", 0.0)

    @property
    @topic_config()
    def remaining_time(self) -> float:
        """剩余时间。"""
        return self.data.get("remaining_time", 0.0)
