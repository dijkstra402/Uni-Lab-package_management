"""
蒸镀仪 — 标准设备类模板 (Device Class Template)

定义「蒸镀仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="evaporation_coater",
    category=["器件制备设备", "蒸镀与表面沉积设备", "蒸镀仪"],
    description="蒸镀仪标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="蒸镀仪",
)
class EvaporationCoater:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "evaporation_coater"
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

    @action(description="设置蒸发源温度")
    def set_evaporation_source_temp(self, evaporation_source_temp: float = 0.0) -> Dict[str, Any]:
        """
        设置蒸发源温度。

        Args:
            evaporation_source_temp[蒸发源温度]: 目标蒸发源温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置蒸镀速率")
    def set_evaporation_rate(self, evaporation_rate: float = 0.0) -> Dict[str, Any]:
        """
        设置蒸镀速率。

        Args:
            evaporation_rate[蒸镀速率]: 目标蒸镀速率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置目标膜厚")
    def set_target_film_thickness(self, target_film_thickness: int = 0) -> Dict[str, Any]:
        """
        设置目标膜厚。

        Args:
            target_film_thickness[目标膜厚]: 目标目标膜厚（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置基板温度")
    def set_substrate_temperature(self, substrate_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置基板温度。

        Args:
            substrate_temperature[基板温度]: 目标基板温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="抽真空")
    def evacuate(self) -> Dict[str, Any]:
        """抽真空。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="蒸镀启动")
    def start_evaporation_coating(self) -> Dict[str, Any]:
        """蒸镀启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="蒸发源停止")
    def stop_evaporation_source(self) -> Dict[str, Any]:
        """蒸发源停止。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="腔室充气")
    def inflate_chamber(self) -> Dict[str, Any]:
        """腔室充气。"""
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
    def evaporation_source_heating_completed(self) -> bool:
        """蒸发源加热完成。"""
        return self.data.get("evaporation_source_heating_completed", False)

    @property
    @topic_config()
    def film_thickness_ready(self) -> bool:
        """膜厚监测就绪。"""
        return self.data.get("film_thickness_ready", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_evaporation_source_temp(self) -> float:
        """蒸发源温度实际值。"""
        return self.data.get("current_evaporation_source_temp", 0.0)

    @property
    @topic_config()
    def current_evaporation_rate(self) -> float:
        """蒸镀速率实际值。"""
        return self.data.get("current_evaporation_rate", 0.0)

    @property
    @topic_config()
    def current_film_thickness(self) -> int:
        """实际膜厚。"""
        return self.data.get("current_film_thickness", 0)

    @property
    @topic_config()
    def current_substrate_temperature(self) -> float:
        """基板温度实际值。"""
        return self.data.get("current_substrate_temperature", 0.0)
