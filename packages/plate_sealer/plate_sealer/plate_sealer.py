"""
封膜仪 — 标准设备类模板 (Device Class Template)

定义「封膜仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="plate_sealer",
    category=["封膜仪"],
    description="封膜仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="封膜仪",
)
class PlateSealer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "plate_sealer"
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

    @action(description="设置封膜温度")
    def set_sealing_temperature(self, sealing_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置封膜温度。

        Args:
            sealing_temperature[封膜温度]: 目标封膜温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置封膜时间")
    def set_sealing_time(self, sealing_time: float = 0.0) -> Dict[str, Any]:
        """
        设置封膜时间。

        Args:
            sealing_time[封膜时间]: 目标封膜时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置送膜长度")
    def set_film_feed_length(self, film_feed_length: int = 0) -> Dict[str, Any]:
        """
        设置送膜长度。

        Args:
            film_feed_length[送膜长度]: 目标送膜长度（单位依设备量程而定）。
        """
        pass

    @action(description="设置压力")
    def set_pressure(self, pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置压力。

        Args:
            pressure[压力]: 目标压力（单位依设备量程而定）。
        """
        pass

    @action(description="封膜启动")
    def start_sealing(self) -> Dict[str, Any]:
        """封膜启动。"""
        pass

    @action(description="送膜")
    def feed_film(self) -> Dict[str, Any]:
        """送膜。"""
        pass

    @action(description="加热启动")
    def start_heating(self) -> Dict[str, Any]:
        """加热启动。"""
        pass

    @action(description="切割")
    def cut(self) -> Dict[str, Any]:
        """切割。"""
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
    def sealing_completed(self) -> bool:
        """封膜完成。"""
        return self.data.get("sealing_completed", False)

    @property
    @topic_config()
    def heating_completed(self) -> bool:
        """加热完成。"""
        return self.data.get("heating_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_sealing_temperature(self) -> float:
        """实际封膜温度。"""
        return self.data.get("current_sealing_temperature", 0.0)

    @property
    @topic_config()
    def current_sealing_time(self) -> float:
        """实际封膜时间。"""
        return self.data.get("current_sealing_time", 0.0)

    @property
    @topic_config()
    def current_film_feed_length(self) -> int:
        """实际送膜长度。"""
        return self.data.get("current_film_feed_length", 0)

    @property
    @topic_config()
    def current_pressure(self) -> float:
        """实际压力。"""
        return self.data.get("current_pressure", 0.0)
