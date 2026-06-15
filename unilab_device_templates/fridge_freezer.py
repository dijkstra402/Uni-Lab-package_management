"""
冷冻冷藏箱 — 标准设备类模板 (Device Class Template)

定义「冷冻冷藏箱」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="fridge_freezer",
    category=["冷冻冷藏箱"],
    description="冷冻冷藏箱标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="冷冻冷藏箱",
)
class FridgeFreezer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "fridge_freezer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="除霜")
    def defrost(self, mode: int = 0) -> Dict[str, Any]:
        """
        除霜。

        Args:
            mode[运行模式设置]: 运行模式设置。
        """
        pass

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行。"""
        pass

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
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
    def running_state(self) -> bool:
        """运行状态。"""
        return self.data.get("running_state", False)

    @property
    @topic_config()
    def door_open_state(self) -> bool:
        """门打开状态。"""
        return self.data.get("door_open_state", False)

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
