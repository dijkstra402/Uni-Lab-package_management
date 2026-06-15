"""
电热消解仪 — 标准设备类模板 (Device Class Template)

定义「电热消解仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="electric_digester",
    category=["电热消解仪"],
    description="电热消解仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="电热消解仪",
)
class ElectricDigester:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "electric_digester"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="消解")
    def digest(self, mode: int = 0, target_temperature: int = 0, digestion_time: int = 0, ramp_rate: int = 0) -> Dict[str, Any]:
        """
        消解。

        Args:
            mode[运行模式设置]: 运行模式设置。
            target_temperature[目标温度设置]: 目标温度设置。
            digestion_time[消解时间设置]: 消解时间设置。
            ramp_rate[升温速率设置]: 升温速率设置。
        """
        pass

    @action(description="加热")
    def heat(self, mode: int = 0, target_temperature: int = 0, heating_power: int = 0, ramp_rate: int = 0) -> Dict[str, Any]:
        """
        加热。

        Args:
            mode[运行模式设置]: 运行模式设置。
            target_temperature[目标温度设置]: 目标温度设置。
            heating_power[加热功率设置]: 加热功率设置。
            ramp_rate[升温速率设置]: 升温速率设置。
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
    def heng_wen_state(self) -> bool:
        """恒温状态。"""
        return self.data.get("heng_wen_state", False)

    @property
    @topic_config()
    def door_switch_state(self) -> bool:
        """门开关状态。"""
        return self.data.get("door_switch_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> int:
        """实际温度检测。"""
        return self.data.get("current_temperature", 0)

    @property
    @topic_config()
    def remaining_time(self) -> int:
        """剩余时间显示。"""
        return self.data.get("remaining_time", 0)
