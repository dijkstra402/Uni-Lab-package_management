"""
开关盖加液模块 — 标准设备类模板 (Device Class Template)

定义「开关盖加液模块」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="cap_and_dispense_module",
    category=["开关盖加液模块"],
    description="开关盖加液模块标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="开关盖加液模块",
)
class CapAndDispenseModule:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "cap_and_dispense_module"
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

    @action(description="设置容器位置")
    def set_container_position(self, container_position: int = 0) -> Dict[str, Any]:
        """
        设置容器位置。

        Args:
            container_position[设置容器位置]: 设置容器位置。
        """
        pass

    @action(description="开盖")
    def open_cap(self, cap_height: int = 0) -> Dict[str, Any]:
        """
        开盖。

        Args:
            cap_height[开盖高度设置]: 开盖高度设置。
        """
        pass

    @action(description="关盖")
    def close_cap(self, cap_torque: int = 0) -> Dict[str, Any]:
        """
        关盖。

        Args:
            cap_torque[关盖扭矩设置]: 关盖扭矩设置。
        """
        pass

    @action(description="加液")
    def add_liquid(self, add_volume: int = 0) -> Dict[str, Any]:
        """
        加液。

        Args:
            add_volume[加液体积设置]: 加液体积设置。
        """
        pass

    @action(description="定位")
    def position(self) -> Dict[str, Any]:
        """定位。"""
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
    def current_add_volume(self) -> int:
        """实际加液体积。"""
        return self.data.get("current_add_volume", 0)

    @property
    @topic_config()
    def current_cap_height(self) -> int:
        """实际开盖高度。"""
        return self.data.get("current_cap_height", 0)

    @property
    @topic_config()
    def current_cap_torque(self) -> int:
        """实际关盖扭矩。"""
        return self.data.get("current_cap_torque", 0)

    @property
    @topic_config()
    def current_container_position(self) -> int:
        """实际容器位置。"""
        return self.data.get("current_container_position", 0)
