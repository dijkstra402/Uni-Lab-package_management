"""
蒸镀仪 — 标准设备类模板 (Device Class Template)

定义「蒸镀仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="evaporation_coater",
    category=["蒸镀仪"],
    description="蒸镀仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="蒸镀仪",
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
        pass

    @action(description="抽真空")
    def evacuate(self, mode: int = 0, target_film_thickness: int = 0, substrate_temperature: int = 0) -> Dict[str, Any]:
        """
        抽真空。

        Args:
            mode[运行模式设置]: 运行模式设置。
            target_film_thickness[目标膜厚设置]: 目标膜厚设置。
            substrate_temperature[基板温度设置]: 基板温度设置。
        """
        pass

    @action(description="蒸镀启动")
    def start_evaporation_coating(self, mode: int = 0, evaporation_rate: int = 0, target_film_thickness: int = 0, substrate_temperature: int = 0) -> Dict[str, Any]:
        """
        蒸镀启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            evaporation_rate[蒸镀速率设置]: 蒸镀速率设置。
            target_film_thickness[目标膜厚设置]: 目标膜厚设置。
            substrate_temperature[基板温度设置]: 基板温度设置。
        """
        pass

    @action(description="蒸发源停止")
    def stop_evaporation_source(self, mode: int = 0, evaporation_source_temp: int = 0, target_film_thickness: int = 0, substrate_temperature: int = 0) -> Dict[str, Any]:
        """
        蒸发源停止。

        Args:
            mode[运行模式设置]: 运行模式设置。
            evaporation_source_temp[蒸发源温度设置]: 蒸发源温度设置。
            target_film_thickness[目标膜厚设置]: 目标膜厚设置。
            substrate_temperature[基板温度设置]: 基板温度设置。
        """
        pass

    @action(description="腔室充气")
    def inflate_chamber(self, mode: int = 0, target_film_thickness: int = 0, substrate_temperature: int = 0) -> Dict[str, Any]:
        """
        腔室充气。

        Args:
            mode[运行模式设置]: 运行模式设置。
            target_film_thickness[目标膜厚设置]: 目标膜厚设置。
            substrate_temperature[基板温度设置]: 基板温度设置。
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
    def current_film_thickness(self) -> int:
        """实际膜厚。"""
        return self.data.get("current_film_thickness", 0)
