"""
一体化配粉配液站 — 标准设备类模板 (Device Class Template)

定义「一体化配粉配液站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="integrated_powder_liquid_station",
    category=["一体化配粉配液站"],
    description="一体化配粉配液站标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="一体化配粉配液站",
)
class IntegratedPowderLiquidStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "integrated_powder_liquid_station"
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

    @action(description="设置配方编号")
    def set_recipe_number(self, recipe_number: int = 0) -> Dict[str, Any]:
        """
        设置配方编号。

        Args:
            recipe_number[设置配方编号]: 设置配方编号。
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

    @action(description="设置搅拌时间")
    def set_stir_time(self, stir_time: int = 0) -> Dict[str, Any]:
        """
        设置搅拌时间。

        Args:
            stir_time[设置搅拌时间]: 设置搅拌时间。
        """
        pass

    @action(description="配粉启动")
    def start_powder_prep(self) -> Dict[str, Any]:
        """配粉启动。"""
        pass

    @action(description="配液启动")
    def start_liquid_prep(self) -> Dict[str, Any]:
        """配液启动。"""
        pass

    @action(description="搅拌启动")
    def start_stirring(self) -> Dict[str, Any]:
        """搅拌启动。"""
        pass

    @action(description="排空")
    def drain(self) -> Dict[str, Any]:
        """排空。"""
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
    def current_powder_prep_weight(self) -> int:
        """实际配粉重量。"""
        return self.data.get("current_powder_prep_weight", 0)

    @property
    @topic_config()
    def current_liquid_prep_volume(self) -> int:
        """实际配液体积。"""
        return self.data.get("current_liquid_prep_volume", 0)

    @property
    @topic_config()
    def current_stir_speed(self) -> int:
        """实际搅拌速度。"""
        return self.data.get("current_stir_speed", 0)

    @property
    @topic_config()
    def device_temperature(self) -> int:
        """设备温度显示。"""
        return self.data.get("device_temperature", 0)
