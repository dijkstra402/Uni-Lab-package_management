"""
化学气相沉积设备 — 标准设备类模板 (Device Class Template)

定义「化学气相沉积设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="cvd_system",
    category=["化学气相沉积设备"],
    description="化学气相沉积设备标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="化学气相沉积设备",
)
class CvdSystem:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "cvd_system"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="沉积启动")
    def start_deposition(self, mode: int = 0, deposition_temperature: int = 0, process_pressure: int = 0, deposition_time: int = 0) -> Dict[str, Any]:
        """
        沉积启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            deposition_temperature[沉积温度设置]: 沉积温度设置。
            process_pressure[工艺压力设置]: 工艺压力设置。
            deposition_time[沉积时间设置]: 沉积时间设置。
        """
        pass

    @action(description="抽真空")
    def evacuate(self, mode: int = 0, process_pressure: int = 0) -> Dict[str, Any]:
        """
        抽真空。

        Args:
            mode[运行模式设置]: 运行模式设置。
            process_pressure[工艺压力设置]: 工艺压力设置。
        """
        pass

    @action(description="气体切换")
    def switch_gas(self, mode: int = 0, process_pressure: int = 0, gas_flow_1: int = 0) -> Dict[str, Any]:
        """
        气体切换。

        Args:
            mode[运行模式设置]: 运行模式设置。
            process_pressure[工艺压力设置]: 工艺压力设置。
            gas_flow_1[气体流量 1 设置]: 气体流量 1 设置。
        """
        pass

    @action(description="降温")
    def cool_down(self, mode: int = 0, process_pressure: int = 0) -> Dict[str, Any]:
        """
        降温。

        Args:
            mode[运行模式设置]: 运行模式设置。
            process_pressure[工艺压力设置]: 工艺压力设置。
        """
        pass

    @action(description="腔室开门")
    def open_chamber_door(self, mode: int = 0, process_pressure: int = 0) -> Dict[str, Any]:
        """
        腔室开门。

        Args:
            mode[运行模式设置]: 运行模式设置。
            process_pressure[工艺压力设置]: 工艺压力设置。
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
