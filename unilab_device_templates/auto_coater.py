"""
自动涂布机 — 标准设备类模板 (Device Class Template)

定义「自动涂布机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="auto_coater",
    category=["自动涂布机"],
    description="自动涂布机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="自动涂布机",
)
class AutoCoater:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "auto_coater"
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

    @action(description="设置涂布速度")
    def set_coating_speed(self, coating_speed: int = 0) -> Dict[str, Any]:
        """
        设置涂布速度。

        Args:
            coating_speed[设置涂布速度]: 设置涂布速度。
        """
        pass

    @action(description="设置涂布厚度")
    def set_coating_thickness(self, coating_thickness: int = 0) -> Dict[str, Any]:
        """
        设置涂布厚度。

        Args:
            coating_thickness[设置涂布厚度]: 设置涂布厚度。
        """
        pass

    @action(description="设置涂布宽度")
    def set_coating_width(self, coating_width: int = 0) -> Dict[str, Any]:
        """
        设置涂布宽度。

        Args:
            coating_width[设置涂布宽度]: 设置涂布宽度。
        """
        pass

    @action(description="设置刮刀压力")
    def set_blade_pressure(self, blade_pressure: int = 0) -> Dict[str, Any]:
        """
        设置刮刀压力。

        Args:
            blade_pressure[设置刮刀压力]: 设置刮刀压力。
        """
        pass

    @action(description="设置干燥温度")
    def set_gan_zao_temperature(self, gan_zao_temperature: int = 0) -> Dict[str, Any]:
        """
        设置干燥温度。

        Args:
            gan_zao_temperature[设置干燥温度]: 设置干燥温度。
        """
        pass

    @action(description="设置干燥时间")
    def set_gan_zao_time(self, gan_zao_time: int = 0) -> Dict[str, Any]:
        """
        设置干燥时间。

        Args:
            gan_zao_time[设置干燥时间]: 设置干燥时间。
        """
        pass

    @action(description="设置涂布次数")
    def set_coating_count(self, coating_count: int = 0) -> Dict[str, Any]:
        """
        设置涂布次数。

        Args:
            coating_count[设置涂布次数]: 设置涂布次数。
        """
        pass

    @action(description="设置刮刀角度")
    def set_blade_angle(self, blade_angle: int = 0) -> Dict[str, Any]:
        """
        设置刮刀角度。

        Args:
            blade_angle[设置刮刀角度]: 设置刮刀角度。
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
