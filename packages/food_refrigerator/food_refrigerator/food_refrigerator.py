"""
食品柜 — 标准设备类模板 (Device Class Template)

定义「食品柜」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="food_refrigerator",
    category=["加热、制冷及空气净化与调节设备", "冰箱及类似设备", "食品柜"],
    description="食品柜标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="食品柜",
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
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置温度")
    def set_temperature(self, temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置温度。

        Args:
            temperature[温度]: 目标温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置湿度")
    def set_humidity(self, humidity: float = 0.0) -> Dict[str, Any]:
        """
        设置湿度。

        Args:
            humidity[湿度]: 目标湿度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置杀菌时间")
    def set_sterilization_time(self, sterilization_time: float = 0.0) -> Dict[str, Any]:
        """
        设置杀菌时间。

        Args:
            sterilization_time[杀菌时间]: 目标杀菌时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置保鲜周期")
    def set_fresh_keeping_cycle(self, fresh_keeping_cycle: float = 0.0) -> Dict[str, Any]:
        """
        设置保鲜周期。

        Args:
            fresh_keeping_cycle[保鲜周期]: 目标保鲜周期（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行。"""
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
    def current_temperature(self) -> float:
        """实际温度。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def current_humidity(self) -> float:
        """实际湿度。"""
        return self.data.get("current_humidity", 0.0)
