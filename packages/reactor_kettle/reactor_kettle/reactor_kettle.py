"""
反应釜 — 标准设备类模板 (Device Class Template)

定义「反应釜」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="reactor_kettle",
    category=["合成制备仪器与设备", "反应器", "反应釜"],
    description="反应釜标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="反应釜",
)
class ReactorKettle:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "reactor_kettle"
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

    @action(description="设置目标内温")
    def set_target_internal_temp(self, target_internal_temp: int = 0) -> Dict[str, Any]:
        """
        设置目标内温。

        Args:
            target_internal_temp[目标内温]: 目标目标内温（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置搅拌转速")
    def set_stir_speed(self, stir_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌转速。

        Args:
            stir_speed[搅拌转速]: 目标搅拌转速（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="搅拌启动")
    def start_stirring(self) -> Dict[str, Any]:
        """搅拌启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="控温")
    def control_temperature(self) -> Dict[str, Any]:
        """控温。"""
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
    def stir_completed(self) -> bool:
        """搅拌完成。"""
        return self.data.get("stir_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_stir_speed(self) -> float:
        """实际搅拌转速。"""
        return self.data.get("current_stir_speed", 0.0)

    @property
    @topic_config()
    def current_internal_temp(self) -> int:
        """实际内温监测。"""
        return self.data.get("current_internal_temp", 0)
