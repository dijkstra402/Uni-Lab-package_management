"""
涡旋混匀仪 — 标准设备类模板 (Device Class Template)

定义「涡旋混匀仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vortex_mixer",
    category=["样品处理仪器与设备", "混合与分散设备", "涡旋混匀仪"],
    description="涡旋混匀仪标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="涡旋混匀仪",
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
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置混匀速度")
    def set_mix_speed(self, mix_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置混匀速度。

        Args:
            mix_speed[混匀速度]: 目标混匀速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置混匀时间")
    def set_mix_time(self, mix_time: float = 0.0) -> Dict[str, Any]:
        """
        设置混匀时间。

        Args:
            mix_time[混匀时间]: 目标混匀时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置工作模式")
    def set_work_mode(self, work_mode: str = "") -> Dict[str, Any]:
        """
        设置工作模式。

        Args:
            work_mode[工作模式]: 目标工作模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置速度档位")
    def set_speed_gear(self, speed_gear: int = 0) -> Dict[str, Any]:
        """
        设置速度档位。

        Args:
            speed_gear[速度档位]: 目标速度档位（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置启动延迟")
    def set_start_delay(self, start_delay: int = 0) -> Dict[str, Any]:
        """
        设置启动延迟。

        Args:
            start_delay[启动延迟]: 目标启动延迟（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置循环次数")
    def set_cycle_count(self, cycle_count: int = 0) -> Dict[str, Any]:
        """
        设置循环次数。

        Args:
            cycle_count[循环次数]: 目标循环次数（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置时间")
    def set_time(self, time: float = 0.0) -> Dict[str, Any]:
        """
        设置时间。

        Args:
            time[时间]: 目标时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="混匀")
    def mix(self) -> Dict[str, Any]:
        """混匀。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="脚踏开关")
    def foot_switch(self) -> Dict[str, Any]:
        """脚踏开关。"""
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """当前速度显示。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示。"""
        return self.data.get("current_time", 0.0)

    @property
    @topic_config()
    def current_cycle_count(self) -> int:
        """当前循环次数。"""
        return self.data.get("current_cycle_count", 0)
