"""
电磁开关阀 — 标准设备类模板 (Device Class Template)

定义「电磁开关阀」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="solenoid_on_off_valve",
    category=["合成制备仪器与设备", "实验阀与气路设备", "电磁开关阀"],
    description="电磁开关阀标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="电磁开关阀",
)
class SolenoidOnOffValve:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "solenoid_on_off_valve"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置打开时间")
    def set_open_time(self, open_time: float = 0.0) -> Dict[str, Any]:
        """
        设置打开时间。

        Args:
            open_time[打开时间]: 目标打开时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置关闭时间")
    def set_close_time(self, close_time: float = 0.0) -> Dict[str, Any]:
        """
        设置关闭时间。

        Args:
            close_time[关闭时间]: 目标关闭时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="打开")
    def open(self) -> Dict[str, Any]:
        """打开。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="关闭")
    def close(self) -> Dict[str, Any]:
        """关闭。"""
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
    def current_switch(self) -> bool:
        """当前开关显示。"""
        return self.data.get("current_switch", False)
