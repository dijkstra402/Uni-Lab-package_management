"""
控温磁力搅拌器 — 标准设备类模板 (Device Class Template)

定义「控温磁力搅拌器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="temperature_controlled_magnetic_stirrer",
    category=["控温磁力搅拌器"],
    description="控温磁力搅拌器标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="控温磁力搅拌器",
)
class TemperatureControlledMagneticStirrer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "temperature_controlled_magnetic_stirrer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="搅拌")
    def stir(self, stir_speed: int = 0, temperature: int = 0, duration: int = 0, work_mode: int = 0, heat_mode: int = 0, temperature_unit: int = 0, safety_temperature: int = 0) -> Dict[str, Any]:
        """
        搅拌。

        Args:
            stir_speed[搅拌速度设置]: 搅拌转速 (rpm)。
            temperature[加热温度设置]: 目标加热温度。
            duration[时间设置]: 运行时长 (s)。
            work_mode[工作模式设置]: 工作模式编号。
            heat_mode[加热模式设置]: 加热模式编号。
            temperature_unit[温度单位设置]: 温度单位 (0=°C,1=°F)。
            safety_temperature[安全温度设置]: 安全保护温度上限。
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
        """故障标志。"""
        return self.data.get("fault", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> int:
        """当前转速。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_temperature(self) -> int:
        """当前温度。"""
        return self.data.get("current_temperature", 0)

    @property
    @topic_config()
    def current_time(self) -> int:
        """当前计时。"""
        return self.data.get("current_time", 0)
