"""
涡旋混匀仪 — 标准设备类模板 (Device Class Template)

定义「涡旋混匀仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vortex_mixer",
    category=["涡旋混匀仪"],
    description="涡旋混匀仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="涡旋混匀仪",
)
class VortexMixer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "vortex_mixer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="混匀")
    def mix(self, mix_speed: int = 0, mix_time: int = 0, work_mode: int = 0, speed_gear: int = 0, start_delay: int = 0) -> Dict[str, Any]:
        """
        混匀。

        Args:
            mix_speed[混匀速度设置]: 混匀速度设置。
            mix_time[混匀时间设置]: 混匀时间设置。
            work_mode[工作模式设置]: 工作模式设置。
            speed_gear[速度档位设置]: 速度档位设置。
            start_delay[启动延迟设置]: 启动延迟设置。
        """
        pass

    @action(description="脚踏开关")
    def foot_switch(self, work_mode: int = 0, speed_gear: int = 0, start_delay: int = 0) -> Dict[str, Any]:
        """
        脚踏开关。

        Args:
            work_mode[工作模式设置]: 工作模式设置。
            speed_gear[速度档位设置]: 速度档位设置。
            start_delay[启动延迟设置]: 启动延迟设置。
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
        """当前速度显示。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_time(self) -> int:
        """当前时间显示。"""
        return self.data.get("current_time", 0)

    @property
    @topic_config()
    def current_cycle_count(self) -> int:
        """当前循环次数。"""
        return self.data.get("current_cycle_count", 0)
