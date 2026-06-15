"""
熔样机 — 标准设备类模板 (Device Class Template)

定义「熔样机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="sample_fusion_machine",
    category=["熔样机"],
    description="熔样机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="熔样机",
)
class SampleFusionMachine:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "sample_fusion_machine"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: int = 0) -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[设置运行模式]: 设置运行模式。
        """
        pass

    @action(description="设置目标温度")
    def set_target_temperature(self, target_temperature: int = 0) -> Dict[str, Any]:
        """
        设置目标温度。

        Args:
            target_temperature[设置目标温度]: 设置目标温度。
        """
        pass

    @action(description="设置升温速率")
    def set_ramp_rate(self, ramp_rate: int = 0) -> Dict[str, Any]:
        """
        设置升温速率。

        Args:
            ramp_rate[设置升温速率]: 设置升温速率。
        """
        pass

    @action(description="设置保温时间")
    def set_holding_time(self, holding_time: int = 0) -> Dict[str, Any]:
        """
        设置保温时间。

        Args:
            holding_time[设置保温时间]: 设置保温时间。
        """
        pass

    @action(description="设置冷却速率")
    def set_cooling_rate(self, cooling_rate: int = 0) -> Dict[str, Any]:
        """
        设置冷却速率。

        Args:
            cooling_rate[设置冷却速率]: 设置冷却速率。
        """
        pass

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: int = 0) -> Dict[str, Any]:
        """
        设置加热功率。

        Args:
            heating_power[设置加热功率]: 设置加热功率。
        """
        pass

    @action(description="设置搅拌速度")
    def set_stir_speed(self, stir_speed: int = 0) -> Dict[str, Any]:
        """
        设置搅拌速度。

        Args:
            stir_speed[设置搅拌速度]: 设置搅拌速度。
        """
        pass

    @action(description="设置样品重量")
    def set_sample_weight(self, sample_weight: int = 0) -> Dict[str, Any]:
        """
        设置样品重量。

        Args:
            sample_weight[设置样品重量]: 设置样品重量。
        """
        pass

    @action(description="设置熔样时间")
    def set_fusion_time(self, fusion_time: int = 0) -> Dict[str, Any]:
        """
        设置熔样时间。

        Args:
            fusion_time[设置熔样时间]: 设置熔样时间。
        """
        pass

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
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
    def current_temperature(self) -> int:
        """实际温度监测。"""
        return self.data.get("current_temperature", 0)
