"""
电子束刻蚀系统 — 标准设备类模板 (Device Class Template)

定义「电子束刻蚀系统」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="electron_beam_etching_system",
    category=["电子束刻蚀系统"],
    description="电子束刻蚀系统标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="电子束刻蚀系统",
)
class ElectronBeamEtchingSystem:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "electron_beam_etching_system"
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

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: int = 0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[设置真空度]: 设置真空度。
        """
        pass

    @action(description="设置样品台温度")
    def set_sample_stage_temp(self, sample_stage_temp: int = 0) -> Dict[str, Any]:
        """
        设置样品台温度。

        Args:
            sample_stage_temp[设置样品台温度]: 设置样品台温度。
        """
        pass

    @action(description="刻蚀")
    def etch(self, etching_power: int = 0, etching_time: int = 0, etching_depth: int = 0) -> Dict[str, Any]:
        """
        刻蚀。

        Args:
            etching_power[刻蚀功率设置]: 刻蚀功率设置。
            etching_time[刻蚀时间设置]: 刻蚀时间设置。
            etching_depth[刻蚀深度设置]: 刻蚀深度设置。
        """
        pass

    @action(description="等离子体")
    def plasma(self) -> Dict[str, Any]:
        """等离子体。"""
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
    def gas_supply_state(self) -> bool:
        """气体供应状态。"""
        return self.data.get("gas_supply_state", False)

    @property
    @topic_config()
    def sample_stage_moving_state(self) -> bool:
        """样品台移动状态。"""
        return self.data.get("sample_stage_moving_state", False)

    @property
    @topic_config()
    def shield_door_off_state(self) -> bool:
        """屏蔽门关闭状态。"""
        return self.data.get("shield_door_off_state", False)

    @property
    @topic_config()
    def power_stable_state(self) -> bool:
        """功率稳定状态。"""
        return self.data.get("power_stable_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_power(self) -> int:
        """实际功率检测。"""
        return self.data.get("current_power", 0)

    @property
    @topic_config()
    def current_vacuum(self) -> int:
        """实际真空度检测。"""
        return self.data.get("current_vacuum", 0)
