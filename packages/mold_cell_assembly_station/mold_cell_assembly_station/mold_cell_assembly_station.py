"""
模具电池组装工站 — 标准设备类模板 (Device Class Template)

定义「模具电池组装工站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="mold_cell_assembly_station",
    category=["器件制备设备", "电池组装设备", "模具电池组装工站"],
    description="模具电池组装工站标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="模具电池组装工站",
)
class MoldCellAssemblyStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "mold_cell_assembly_station"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="设置模具温度")
    def set_mold_temperature(self, mold_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置模具温度。

        Args:
            mold_temperature[模具温度]: 目标模具温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置注塑压力")
    def set_injection_pressure(self, injection_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置注塑压力。

        Args:
            injection_pressure[注塑压力]: 目标注塑压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置注塑速度")
    def set_injection_speed(self, injection_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置注塑速度。

        Args:
            injection_speed[注塑速度]: 目标注塑速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置保压压力")
    def set_holding_pressure(self, holding_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置保压压力。

        Args:
            holding_pressure[保压压力]: 目标保压压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置保压时间")
    def set_holding_time(self, holding_time: float = 0.0) -> Dict[str, Any]:
        """
        设置保压时间。

        Args:
            holding_time[保压时间]: 目标保压时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置冷却时间")
    def set_cooling_time(self, cooling_time: float = 0.0) -> Dict[str, Any]:
        """
        设置冷却时间。

        Args:
            cooling_time[冷却时间]: 目标冷却时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置预热温度")
    def set_preheat_temperature(self, preheat_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置预热温度。

        Args:
            preheat_temperature[预热温度]: 目标预热温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: float = 0.0) -> Dict[str, Any]:
        """
        设置加热功率。

        Args:
            heating_power[加热功率]: 目标加热功率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态。"""
        return self.data.get("status", "idle")

    @property
    @topic_config()
    def device_running_state(self) -> bool:
        """设备运行状态。"""
        return self.data.get("device_running_state", False)

    @property
    @topic_config()
    def device_fault_state(self) -> bool:
        """设备故障状态。"""
        return self.data.get("device_fault_state", False)

    @property
    @topic_config()
    def mold_closed_state(self) -> bool:
        """模具闭合状态。"""
        return self.data.get("mold_closed_state", False)

    @property
    @topic_config()
    def injection_process_state(self) -> bool:
        """注塑工序状态。"""
        return self.data.get("injection_process_state", False)

    @property
    @topic_config()
    def demold_process_state(self) -> bool:
        """脱模工序状态。"""
        return self.data.get("demold_process_state", False)

    @property
    @topic_config()
    def preheat_process_state(self) -> bool:
        """预热工序状态。"""
        return self.data.get("preheat_process_state", False)

    @property
    @topic_config()
    def material_in_place_state(self) -> bool:
        """物料到位状态。"""
        return self.data.get("material_in_place_state", False)

    @property
    @topic_config()
    def hydraulic_system_state(self) -> bool:
        """液压系统状态。"""
        return self.data.get("hydraulic_system_state", False)

    @property
    @topic_config()
    def heating_system_state(self) -> bool:
        """加热系统状态。"""
        return self.data.get("heating_system_state", False)

    @property
    @topic_config()
    def device_status_code(self) -> int:
        """设备状态码。"""
        return self.data.get("device_status_code", 0)

    @property
    @topic_config()
    def mold_status_code(self) -> int:
        """模具状态码。"""
        return self.data.get("mold_status_code", 0)

    @property
    @topic_config()
    def injection_status_code(self) -> int:
        """注塑状态码。"""
        return self.data.get("injection_status_code", 0)

    @property
    @topic_config()
    def demold_status_code(self) -> int:
        """脱模状态码。"""
        return self.data.get("demold_status_code", 0)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_mold_temperature(self) -> float:
        """模具温度实际。"""
        return self.data.get("current_mold_temperature", 0.0)

    @property
    @topic_config()
    def current_injection_pressure(self) -> float:
        """注塑压力实际。"""
        return self.data.get("current_injection_pressure", 0.0)

    @property
    @topic_config()
    def current_injection_speed(self) -> float:
        """注塑速度实际。"""
        return self.data.get("current_injection_speed", 0.0)

    @property
    @topic_config()
    def current_holding_pressure(self) -> float:
        """保压压力实际。"""
        return self.data.get("current_holding_pressure", 0.0)

    @property
    @topic_config()
    def current_holding_time(self) -> float:
        """保压时间实际。"""
        return self.data.get("current_holding_time", 0.0)

    @property
    @topic_config()
    def current_cooling_time(self) -> float:
        """冷却时间实际。"""
        return self.data.get("current_cooling_time", 0.0)

    @property
    @topic_config()
    def current_preheat_temperature(self) -> float:
        """预热温度实际。"""
        return self.data.get("current_preheat_temperature", 0.0)

    @property
    @topic_config()
    def current_heating_power(self) -> float:
        """加热功率实际。"""
        return self.data.get("current_heating_power", 0.0)
