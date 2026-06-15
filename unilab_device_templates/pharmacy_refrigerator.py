"""
药品柜 — 标准设备类模板 (Device Class Template)

定义「药品柜」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="pharmacy_refrigerator",
    category=["药品柜"],
    description="药品柜标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="药品柜",
)
class PharmacyRefrigerator:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "pharmacy_refrigerator"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="运行")
    def run(self, mode: int = 0) -> Dict[str, Any]:
        """
        运行。

        Args:
            mode[运行模式设置]: 运行模式编号。
        """
        pass

    @action(description="备份")
    def backup(self) -> Dict[str, Any]:
        """备份。"""
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
    def door_open(self) -> bool:
        """门打开状态。"""
        return self.data.get("door_open", False)

    @property
    @topic_config()
    def data_logging_state(self) -> bool:
        """数据记录状态。"""
        return self.data.get("data_logging_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> int:
        """当前温度。"""
        return self.data.get("current_temperature", 0)
