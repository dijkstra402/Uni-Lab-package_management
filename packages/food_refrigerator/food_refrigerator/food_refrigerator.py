"""
食品柜 — 标准设备类模板 (Device Class Template)

定义「食品柜」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="food_refrigerator",
    category=["食品柜"],
    description="食品柜标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="食品柜",
)
class FoodRefrigerator:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "food_refrigerator"
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

    @action(description="设置温度")
    def set_temperature(self, temperature: int = 0) -> Dict[str, Any]:
        """
        设置温度。

        Args:
            temperature[设置温度]: 设置温度。
        """
        pass

    @action(description="设置湿度")
    def set_humidity(self, humidity: int = 0) -> Dict[str, Any]:
        """
        设置湿度。

        Args:
            humidity[设置湿度]: 设置湿度。
        """
        pass

    @action(description="设置杀菌时间")
    def set_sterilization_time(self, sterilization_time: int = 0) -> Dict[str, Any]:
        """
        设置杀菌时间。

        Args:
            sterilization_time[设置杀菌时间]: 设置杀菌时间。
        """
        pass

    @action(description="设置保鲜周期")
    def set_fresh_keeping_cycle(self, fresh_keeping_cycle: int = 0) -> Dict[str, Any]:
        """
        设置保鲜周期。

        Args:
            fresh_keeping_cycle[设置保鲜周期]: 设置保鲜周期。
        """
        pass

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行。"""
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
    def door_open_state(self) -> bool:
        """门打开状态。"""
        return self.data.get("door_open_state", False)

    @property
    @topic_config()
    def humidity_state(self) -> bool:
        """湿度监控状态。"""
        return self.data.get("humidity_state", False)

    @property
    @topic_config()
    def sterilization_function_state(self) -> bool:
        """杀菌功能状态。"""
        return self.data.get("sterilization_function_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> int:
        """实际温度。"""
        return self.data.get("current_temperature", 0)

    @property
    @topic_config()
    def current_humidity(self) -> int:
        """实际湿度。"""
        return self.data.get("current_humidity", 0)
