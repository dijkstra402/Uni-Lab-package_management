"""
真空吸液系统 — 标准设备类模板 (Device Class Template)

定义「真空吸液系统」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vacuum_aspiration_system",
    category=["真空吸液系统"],
    description="真空吸液系统标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="真空吸液系统",
)
class VacuumAspirationSystem:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "vacuum_aspiration_system"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="吸液启动")
    def start_draw_liquid(self, mode: int = 0, aspirate_time: int = 0, aspirate_volume: int = 0) -> Dict[str, Any]:
        """
        吸液启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            aspirate_time[吸液时间设置]: 吸液时间设置。
            aspirate_volume[吸液体积设置]: 吸液体积设置。
        """
        pass

    @action(description="真空启动")
    def start_vacuum(self, mode: int = 0, vacuum: int = 0) -> Dict[str, Any]:
        """
        真空启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            vacuum[真空度设置]: 真空度设置。
        """
        pass

    @action(description="排液")
    def dispense(self, mode: int = 0) -> Dict[str, Any]:
        """
        排液。

        Args:
            mode[运行模式设置]: 运行模式设置。
        """
        pass

    @action(description="清洗")
    def clean(self, mode: int = 0) -> Dict[str, Any]:
        """
        清洗。

        Args:
            mode[运行模式设置]: 运行模式设置。
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
    def current_vacuum(self) -> int:
        """实际真空度。"""
        return self.data.get("current_vacuum", 0)

    @property
    @topic_config()
    def current_aspirate_time(self) -> int:
        """实际吸液时间。"""
        return self.data.get("current_aspirate_time", 0)

    @property
    @topic_config()
    def current_aspirate_volume(self) -> int:
        """实际吸液体积。"""
        return self.data.get("current_aspirate_volume", 0)

    @property
    @topic_config()
    def guo_lv_qi_state(self) -> int:
        """过滤器状态。"""
        return self.data.get("guo_lv_qi_state", 0)
