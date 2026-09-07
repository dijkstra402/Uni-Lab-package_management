"""
软包电池组装工站 — 标准设备类模板 (Device Class Template)

定义「软包电池组装工站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="pouch_cell_assembly_station",
    category=["器件制备设备", "电池组装设备", "软包电池组装工站"],
    description="软包电池组装工站标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="软包电池组装工站",
)
class PouchCellAssemblyStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "pouch_cell_assembly_station"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="设置封装温度")
    def set_packaging_temperature(self, packaging_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置封装温度。

        Args:
            packaging_temperature[封装温度]: 目标封装温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置封装压力")
    def set_packaging_pressure(self, packaging_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置封装压力。

        Args:
            packaging_pressure[封装压力]: 目标封装压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置封装时间")
    def set_packaging_time(self, packaging_time: float = 0.0) -> Dict[str, Any]:
        """
        设置封装时间。

        Args:
            packaging_time[封装时间]: 目标封装时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置热压温度")
    def set_hot_press_temperature(self, hot_press_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置热压温度。

        Args:
            hot_press_temperature[热压温度]: 目标热压温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置热压压力")
    def set_hot_press_pressure(self, hot_press_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置热压压力。

        Args:
            hot_press_pressure[热压压力]: 目标热压压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置热压时间")
    def set_hot_press_time(self, hot_press_time: float = 0.0) -> Dict[str, Any]:
        """
        设置热压时间。

        Args:
            hot_press_time[热压时间]: 目标热压时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置裁切速度")
    def set_cutting_speed(self, cutting_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置裁切速度。

        Args:
            cutting_speed[裁切速度]: 目标裁切速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[真空度]: 目标真空度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置冷却水温")
    def set_cooling_water_temp(self, cooling_water_temp: float = 0.0) -> Dict[str, Any]:
        """
        设置冷却水温。

        Args:
            cooling_water_temp[冷却水温]: 目标冷却水温（单位依设备量程而定）。
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
    def packaging_process_state(self) -> bool:
        """封装工序状态。"""
        return self.data.get("packaging_process_state", False)

    @property
    @topic_config()
    def cutting_process_state(self) -> bool:
        """裁切工序状态。"""
        return self.data.get("cutting_process_state", False)

    @property
    @topic_config()
    def hot_press_process_state(self) -> bool:
        """热压工序状态。"""
        return self.data.get("hot_press_process_state", False)

    @property
    @topic_config()
    def device_ready_state(self) -> bool:
        """设备就绪状态。"""
        return self.data.get("device_ready_state", False)

    @property
    @topic_config()
    def material_in_place_state(self) -> bool:
        """物料到位状态。"""
        return self.data.get("material_in_place_state", False)

    @property
    @topic_config()
    def vacuum_state(self) -> bool:
        """真空状态。"""
        return self.data.get("vacuum_state", False)

    @property
    @topic_config()
    def cooling_system_state(self) -> bool:
        """冷却系统状态。"""
        return self.data.get("cooling_system_state", False)

    @property
    @topic_config()
    def device_status_code(self) -> int:
        """设备状态码。"""
        return self.data.get("device_status_code", 0)

    @property
    @topic_config()
    def packaging_status_code(self) -> int:
        """封装状态码。"""
        return self.data.get("packaging_status_code", 0)

    @property
    @topic_config()
    def cutting_status_code(self) -> int:
        """裁切状态码。"""
        return self.data.get("cutting_status_code", 0)

    @property
    @topic_config()
    def hot_press_status_code(self) -> int:
        """热压状态码。"""
        return self.data.get("hot_press_status_code", 0)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_packaging_temperature(self) -> float:
        """封装温度实际。"""
        return self.data.get("current_packaging_temperature", 0.0)

    @property
    @topic_config()
    def current_packaging_pressure(self) -> float:
        """封装压力实际。"""
        return self.data.get("current_packaging_pressure", 0.0)

    @property
    @topic_config()
    def current_packaging_time(self) -> float:
        """封装时间实际。"""
        return self.data.get("current_packaging_time", 0.0)

    @property
    @topic_config()
    def current_hot_press_temperature(self) -> float:
        """热压温度实际。"""
        return self.data.get("current_hot_press_temperature", 0.0)

    @property
    @topic_config()
    def current_hot_press_pressure(self) -> float:
        """热压压力实际。"""
        return self.data.get("current_hot_press_pressure", 0.0)

    @property
    @topic_config()
    def current_hot_press_time(self) -> float:
        """热压时间实际。"""
        return self.data.get("current_hot_press_time", 0.0)

    @property
    @topic_config()
    def current_cutting_speed(self) -> float:
        """裁切速度实际。"""
        return self.data.get("current_cutting_speed", 0.0)

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """真空度实际。"""
        return self.data.get("current_vacuum", 0.0)

    @property
    @topic_config()
    def packaging_mold_position(self) -> float:
        """封装模具位置。"""
        return self.data.get("packaging_mold_position", 0.0)

    @property
    @topic_config()
    def current_cooling_water_temp(self) -> float:
        """冷却水温实际。"""
        return self.data.get("current_cooling_water_temp", 0.0)

    @property
    @topic_config()
    def current_heating_power(self) -> float:
        """加热功率实际。"""
        return self.data.get("current_heating_power", 0.0)
