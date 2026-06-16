"""
自动滴定仪 — 标准设备类模板 (Device Class Template)

定义「自动滴定仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="auto_titrator",
    category=["自动滴定仪"],
    description="自动滴定仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="自动滴定仪",
)
class AutoTitrator:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "auto_titrator"
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

    @action(description="设置滴定终点")
    def set_titration_endpoint(self, titration_endpoint: int = 0) -> Dict[str, Any]:
        """
        设置滴定终点。

        Args:
            titration_endpoint[滴定终点]: 目标滴定终点（单位依设备量程而定）。
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

    @action(description="滴定启动")
    def start_titration(self) -> Dict[str, Any]:
        """滴定启动。"""
        pass

    @action(description="加液启动")
    def start_add_liquid(self) -> Dict[str, Any]:
        """加液启动。"""
        pass

    @action(description="搅拌启动")
    def start_stirring(self) -> Dict[str, Any]:
        """搅拌启动。"""
        pass

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗。"""
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
    def titration_completed(self) -> bool:
        """滴定完成。"""
        return self.data.get("titration_completed", False)

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
    def titrant_volume(self) -> float:
        """滴定液体积。"""
        return self.data.get("titrant_volume", 0.0)

    @property
    @topic_config()
    def current_titrant_volume(self) -> float:
        """实际滴定液体积。"""
        return self.data.get("current_titrant_volume", 0.0)

    @property
    @topic_config()
    def current_titration_endpoint(self) -> int:
        """实际滴定终点。"""
        return self.data.get("current_titration_endpoint", 0)

    @property
    @topic_config()
    def current_stir_speed(self) -> float:
        """实际搅拌速度。"""
        return self.data.get("current_stir_speed", 0.0)
