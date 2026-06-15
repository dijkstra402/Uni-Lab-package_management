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

    @action(description="吸液")
    def draw_liquid(self, mode: int = 0, aspirate_volume: int = 0, aspirate_speed: int = 0) -> Dict[str, Any]:
        """
        吸液。

        Args:
            mode[运行模式设置]: 运行模式设置。
            aspirate_volume[吸液体积设置]: 吸液体积设置。
            aspirate_speed[吸液速度设置]: 吸液速度设置。
        """
        pass

    @action(description="排液")
    def dispense(self, mode: int = 0, dispense_volume: int = 0, dispense_speed: int = 0) -> Dict[str, Any]:
        """
        排液。

        Args:
            mode[运行模式设置]: 运行模式设置。
            dispense_volume[排液体积设置]: 排液体积设置。
            dispense_speed[排液速度设置]: 排液速度设置。
        """
        pass

    @action(description="枪头安装")
    def attach_tip(self, mode: int = 0, tip_position: int = 0) -> Dict[str, Any]:
        """
        枪头安装。

        Args:
            mode[运行模式设置]: 运行模式设置。
            tip_position[枪头位置设置]: 枪头位置设置。
        """
        pass

    @action(description="枪头丢弃")
    def discard_tip(self, mode: int = 0, tip_position: int = 0) -> Dict[str, Any]:
        """
        枪头丢弃。

        Args:
            mode[运行模式设置]: 运行模式设置。
            tip_position[枪头位置设置]: 枪头位置设置。
        """
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
    def current_aspirate_volume(self) -> int:
        """实际吸液体积。"""
        return self.data.get("current_aspirate_volume", 0)

    @property
    @topic_config()
    def current_dispense_volume(self) -> int:
        """实际排液体积。"""
        return self.data.get("current_dispense_volume", 0)

    @property
    @topic_config()
    def current_tip_position(self) -> int:
        """实际枪头位置。"""
        return self.data.get("current_tip_position", 0)

    @property
    @topic_config()
    def tip_state(self) -> int:
        """枪头状态。"""
        return self.data.get("tip_state", 0)
