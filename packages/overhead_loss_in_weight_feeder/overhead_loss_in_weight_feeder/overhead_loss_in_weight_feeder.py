"""
顶置失重固体投料模块 — 标准设备类模板 (Device Class Template)

定义「顶置失重固体投料模块」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="overhead_loss_in_weight_feeder",
    category=["顶置失重固体投料模块"],
    description="顶置失重固体投料模块标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="顶置失重固体投料模块",
)
class OverheadLossInWeightFeeder:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "overhead_loss_in_weight_feeder"
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

    @action(description="设置搅拌速度")
    def set_stir_speed(self, stir_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌速度。

        Args:
            stir_speed[搅拌速度]: 目标搅拌速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置投料量")
    def set_charge_amount(self, charge_amount: float = 0.0) -> Dict[str, Any]:
        """
        设置投料量。

        Args:
            charge_amount[投料量]: 目标投料量（单位依设备量程而定）。
        """
        pass

    @action(description="设置失重率")
    def set_weight_loss_rate(self, weight_loss_rate: float = 0.0) -> Dict[str, Any]:
        """
        设置失重率。

        Args:
            weight_loss_rate[失重率]: 目标失重率（单位依设备量程而定）。
        """
        pass

    @action(description="投料")
    def charge(self) -> Dict[str, Any]:
        """投料。"""
        pass

    @action(description="补料")
    def replenish(self) -> Dict[str, Any]:
        """补料。"""
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
    def weight_loss_stable_state(self) -> bool:
        """失重稳定状态。"""
        return self.data.get("weight_loss_stable_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_charge_amount(self) -> int:
        """实际投料量。"""
        return self.data.get("current_charge_amount", 0)

    @property
    @topic_config()
    def current_weight_loss_rate(self) -> int:
        """实际失重率。"""
        return self.data.get("current_weight_loss_rate", 0)
