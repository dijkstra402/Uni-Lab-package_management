"""
分散机 — 标准设备类模板 (Device Class Template)

定义「分散机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="disperser",
    category=["分散机"],
    description="分散机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="分散机",
)
class Disperser:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "disperser"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="分散")
    def disperse(self, dispersion_speed: int = 0, dispersion_time: int = 0, disperser_head_height: int = 0, dispersion_mode: int = 0, speed_increment: int = 0, increment_time: int = 0, torque_limit: int = 0) -> Dict[str, Any]:
        """
        分散。

        Args:
            dispersion_speed[分散转速设置]: 分散转速设置。
            dispersion_time[分散时间设置]: 分散时间设置。
            disperser_head_height[分散头高度设置]: 分散头高度设置。
            dispersion_mode[分散模式设置]: 分散模式设置。
            speed_increment[转速增量设置]: 转速增量设置。
            increment_time[增量时间设置]: 增量时间设置。
            torque_limit[扭矩限制设置]: 扭矩限制设置。
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
    def current_speed(self) -> int:
        """当前转速显示。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_time(self) -> int:
        """当前时间显示。"""
        return self.data.get("current_time", 0)

    @property
    @topic_config()
    def current_height(self) -> int:
        """当前高度显示。"""
        return self.data.get("current_height", 0)

    @property
    @topic_config()
    def current_torque(self) -> int:
        """当前扭矩显示。"""
        return self.data.get("current_torque", 0)
