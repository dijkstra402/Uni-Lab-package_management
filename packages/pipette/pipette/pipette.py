"""
移液器 — 标准设备类模板 (Device Class Template)

定义「移液器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="pipette",
    category=["移液器"],
    description="移液器标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="移液器",
)
class Pipette:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "pipette"
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

    @action(description="设置吸液体积")
    def set_aspirate_volume(self, aspirate_volume: float = 0.0) -> Dict[str, Any]:
        """
        设置吸液体积。

        Args:
            aspirate_volume[吸液体积]: 目标吸液体积（单位依设备量程而定）。
        """
        pass

    @action(description="设置排液体积")
    def set_dispense_volume(self, dispense_volume: float = 0.0) -> Dict[str, Any]:
        """
        设置排液体积。

        Args:
            dispense_volume[排液体积]: 目标排液体积（单位依设备量程而定）。
        """
        pass

    @action(description="设置吸液速度")
    def set_aspirate_speed(self, aspirate_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置吸液速度。

        Args:
            aspirate_speed[吸液速度]: 目标吸液速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置排液速度")
    def set_dispense_speed(self, dispense_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置排液速度。

        Args:
            dispense_speed[排液速度]: 目标排液速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置枪头位置")
    def set_tip_position(self, tip_position: float = 0.0) -> Dict[str, Any]:
        """
        设置枪头位置。

        Args:
            tip_position[枪头位置]: 目标枪头位置（单位依设备量程而定）。
        """
        pass

    @action(description="吸液")
    def draw_liquid(self) -> Dict[str, Any]:
        """吸液。"""
        pass

    @action(description="排液")
    def dispense(self) -> Dict[str, Any]:
        """排液。"""
        pass

    @action(description="枪头安装")
    def attach_tip(self) -> Dict[str, Any]:
        """枪头安装。"""
        pass

    @action(description="枪头丢弃")
    def discard_tip(self) -> Dict[str, Any]:
        """枪头丢弃。"""
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
    def current_aspirate_volume(self) -> float:
        """实际吸液体积。"""
        return self.data.get("current_aspirate_volume", 0.0)

    @property
    @topic_config()
    def current_dispense_volume(self) -> float:
        """实际排液体积。"""
        return self.data.get("current_dispense_volume", 0.0)

    @property
    @topic_config()
    def current_tip_position(self) -> float:
        """实际枪头位置。"""
        return self.data.get("current_tip_position", 0.0)

    @property
    @topic_config()
    def tip_state(self) -> int:
        """枪头状态。"""
        return self.data.get("tip_state", 0)
