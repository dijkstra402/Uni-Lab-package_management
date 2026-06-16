"""
移液工作站 — 标准设备类模板 (Device Class Template)

定义「移液工作站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="liquid_handling_workstation",
    category=["移液工作站"],
    description="移液工作站标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="移液工作站",
)
class LiquidHandlingWorkstation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "liquid_handling_workstation"
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

    @action(description="设置移液速度")
    def set_pipette_speed(self, pipette_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置移液速度。

        Args:
            pipette_speed[移液速度]: 目标移液速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置目标孔位")
    def set_target_well(self, target_well: int = 0) -> Dict[str, Any]:
        """
        设置目标孔位。

        Args:
            target_well[目标孔位]: 目标目标孔位（单位依设备量程而定）。
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

    @action(description="移液路径")
    def pipette_path(self) -> Dict[str, Any]:
        """移液路径。"""
        pass

    @action(description="枪头更换")
    def change_tip(self) -> Dict[str, Any]:
        """枪头更换。"""
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
    def current_pipette_speed(self) -> float:
        """实际移液速度。"""
        return self.data.get("current_pipette_speed", 0.0)

    @property
    @topic_config()
    def tip_state(self) -> int:
        """枪头状态。"""
        return self.data.get("tip_state", 0)

    @property
    @topic_config()
    def liquid_level(self) -> float:
        """液位检测值。"""
        return self.data.get("liquid_level", 0.0)
