"""
投料反应站 — 标准设备类模板 (Device Class Template)

定义「投料反应站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="charging_reaction_station",
    category=["投料反应站"],
    description="投料反应站标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="投料反应站",
)
class ChargingReactionStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "charging_reaction_station"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="投料启动")
    def start_charging(self, mode: int = 0) -> Dict[str, Any]:
        """
        投料启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
        """
        pass

    @action(description="反应启动")
    def start_reaction(self, mode: int = 0, reaction_temperature: int = 0, reaction_time: int = 0) -> Dict[str, Any]:
        """
        反应启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            reaction_temperature[反应温度设置]: 反应温度设置。
            reaction_time[反应时间设置]: 反应时间设置。
        """
        pass

    @action(description="搅拌启动")
    def start_stirring(self, mode: int = 0, stir_speed: int = 0) -> Dict[str, Any]:
        """
        搅拌启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            stir_speed[搅拌速度设置]: 搅拌速度设置。
        """
        pass

    @action(description="温控启动")
    def start_temp_control(self, mode: int = 0) -> Dict[str, Any]:
        """
        温控启动。

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
    def current_charge_weight(self) -> int:
        """实际投料重量。"""
        return self.data.get("current_charge_weight", 0)

    @property
    @topic_config()
    def current_reaction_temperature(self) -> int:
        """实际反应温度。"""
        return self.data.get("current_reaction_temperature", 0)

    @property
    @topic_config()
    def current_stir_speed(self) -> int:
        """实际搅拌速度。"""
        return self.data.get("current_stir_speed", 0)

    @property
    @topic_config()
    def current_reaction_time(self) -> int:
        """实际反应时间。"""
        return self.data.get("current_reaction_time", 0)

    @property
    @topic_config()
    def liquid_level(self) -> int:
        """液位高度显示。"""
        return self.data.get("liquid_level", 0)
