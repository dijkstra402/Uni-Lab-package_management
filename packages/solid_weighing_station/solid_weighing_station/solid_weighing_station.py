"""
固体称量工作站 — 标准设备类模板 (Device Class Template)

定义「固体称量工作站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="solid_weighing_station",
    category=["合成制备仪器与设备", "固体分配设备", "固体称量工作站"],
    description="固体称量工作站标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="固体称量工作站",
)
class SolidWeighingStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "solid_weighing_station"
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

    @action(description="设置称量精度")
    def set_weighing_precision(self, weighing_precision: int = 0) -> Dict[str, Any]:
        """
        设置称量精度。

        Args:
            weighing_precision[称量精度]: 目标称量精度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置卸料速度")
    def set_discharge_speed(self, discharge_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置卸料速度。

        Args:
            discharge_speed[卸料速度]: 目标卸料速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置称量重量")
    def set_weighed_weight(self, weighed_weight: float = 0.0) -> Dict[str, Any]:
        """
        设置称量重量。

        Args:
            weighed_weight[称量重量]: 目标称量重量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="称量")
    def weigh(self) -> Dict[str, Any]:
        """称量。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="卸料")
    def discharge(self) -> Dict[str, Any]:
        """卸料。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="校准")
    def calibrate(self) -> Dict[str, Any]:
        """校准。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="去皮")
    def tare(self) -> Dict[str, Any]:
        """去皮。"""
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_weighed_weight(self) -> float:
        """实际称量重量。"""
        return self.data.get("current_weighed_weight", 0.0)
