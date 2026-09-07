"""
真空吸液系统 — 标准设备类模板 (Device Class Template)

定义「真空吸液系统」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vacuum_aspiration_system",
    category=["合成制备仪器与设备", "液体分配设备", "真空吸液系统"],
    description="真空吸液系统标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="真空吸液系统",
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
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[真空度]: 目标真空度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置吸液时间")
    def set_aspirate_time(self, aspirate_time: float = 0.0) -> Dict[str, Any]:
        """
        设置吸液时间。

        Args:
            aspirate_time[吸液时间]: 目标吸液时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置吸液体积")
    def set_aspirate_volume(self, aspirate_volume: float = 0.0) -> Dict[str, Any]:
        """
        设置吸液体积。

        Args:
            aspirate_volume[吸液体积]: 目标吸液体积（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="吸液启动")
    def start_draw_liquid(self) -> Dict[str, Any]:
        """吸液启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="真空启动")
    def start_vacuum(self) -> Dict[str, Any]:
        """真空启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="排液")
    def dispense(self) -> Dict[str, Any]:
        """排液。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗。"""
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
    def vacuum_completed(self) -> bool:
        """真空完成。"""
        return self.data.get("vacuum_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """实际真空度。"""
        return self.data.get("current_vacuum", 0.0)

    @property
    @topic_config()
    def current_aspirate_time(self) -> float:
        """实际吸液时间。"""
        return self.data.get("current_aspirate_time", 0.0)

    @property
    @topic_config()
    def current_aspirate_volume(self) -> float:
        """实际吸液体积。"""
        return self.data.get("current_aspirate_volume", 0.0)

    @property
    @topic_config()
    def filter_state(self) -> int:
        """过滤器状态。"""
        return self.data.get("filter_state", 0)
