"""
薄膜电池组装工站 — 标准设备类模板 (Device Class Template)

定义「薄膜电池组装工站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="thin_film_cell_assembly_station",
    category=["薄膜电池组装工站"],
    description="薄膜电池组装工站标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="薄膜电池组装工站",
)
class ThinFilmCellAssemblyStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "thin_film_cell_assembly_station"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="设置沉积温度")
    def set_deposition_temperature(self, deposition_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置沉积温度。

        Args:
            deposition_temperature[沉积温度]: 目标沉积温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置沉积速率")
    def set_deposition_rate(self, deposition_rate: float = 0.0) -> Dict[str, Any]:
        """
        设置沉积速率。

        Args:
            deposition_rate[沉积速率]: 目标沉积速率（单位依设备量程而定）。
        """
        pass

    @action(description="设置沉积时间")
    def set_deposition_time(self, deposition_time: float = 0.0) -> Dict[str, Any]:
        """
        设置沉积时间。

        Args:
            deposition_time[沉积时间]: 目标沉积时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置溅射功率")
    def set_sputter_power(self, sputter_power: float = 0.0) -> Dict[str, Any]:
        """
        设置溅射功率。

        Args:
            sputter_power[溅射功率]: 目标溅射功率（单位依设备量程而定）。
        """
        pass

    @action(description="设置溅射气压")
    def set_sputter_pressure(self, sputter_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置溅射气压。

        Args:
            sputter_pressure[溅射气压]: 目标溅射气压（单位依设备量程而定）。
        """
        pass

    @action(description="设置退火温度")
    def set_annealing_temperature(self, annealing_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置退火温度。

        Args:
            annealing_temperature[退火温度]: 目标退火温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置退火时间")
    def set_annealing_time(self, annealing_time: float = 0.0) -> Dict[str, Any]:
        """
        设置退火时间。

        Args:
            annealing_time[退火时间]: 目标退火时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[真空度]: 目标真空度（单位依设备量程而定）。
        """
        pass

    @action(description="设置Ar气流量")
    def set_ar_gas_flow(self, ar_gas_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置Ar气流量。

        Args:
            ar_gas_flow[Ar气流量]: 目标Ar气流量（单位依设备量程而定）。
        """
        pass

    @action(description="设置O2气流量")
    def set_o2_gas_flow(self, o2_gas_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置O2气流量。

        Args:
            o2_gas_flow[O2气流量]: 目标O2气流量（单位依设备量程而定）。
        """
        pass

    @action(description="设置N2气流量")
    def set_n2_gas_flow(self, n2_gas_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置N2气流量。

        Args:
            n2_gas_flow[N2气流量]: 目标N2气流量（单位依设备量程而定）。
        """
        pass

    @action(description="设置气体分压比")
    def set_gas_partial_pressure_ratio(self, gas_partial_pressure_ratio: float = 0.0) -> Dict[str, Any]:
        """
        设置气体分压比。

        Args:
            gas_partial_pressure_ratio[气体分压比]: 目标气体分压比（单位依设备量程而定）。
        """
        pass

    @action(description="设置薄膜厚度")
    def set_film_thickness(self, film_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置薄膜厚度。

        Args:
            film_thickness[薄膜厚度]: 目标薄膜厚度（单位依设备量程而定）。
        """
        pass

    @action(description="设置射频功率")
    def set_rf_power(self, rf_power: float = 0.0) -> Dict[str, Any]:
        """
        设置射频功率。

        Args:
            rf_power[射频功率]: 目标射频功率（单位依设备量程而定）。
        """
        pass

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
        pass

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
        pass

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位。"""
        pass

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
    def deposition_process_state(self) -> bool:
        """沉积工序状态。"""
        return self.data.get("deposition_process_state", False)

    @property
    @topic_config()
    def sputter_process_state(self) -> bool:
        """溅射工序状态。"""
        return self.data.get("sputter_process_state", False)

    @property
    @topic_config()
    def annealing_process_state(self) -> bool:
        """退火工序状态。"""
        return self.data.get("annealing_process_state", False)

    @property
    @topic_config()
    def vacuum_system_state(self) -> bool:
        """真空系统状态。"""
        return self.data.get("vacuum_system_state", False)

    @property
    @topic_config()
    def target_state(self) -> bool:
        """靶材状态。"""
        return self.data.get("target_state", False)

    @property
    @topic_config()
    def substrate_in_place_state(self) -> bool:
        """基片到位状态。"""
        return self.data.get("substrate_in_place_state", False)

    @property
    @topic_config()
    def gas_supply_state(self) -> bool:
        """气体供应状态。"""
        return self.data.get("gas_supply_state", False)

    @property
    @topic_config()
    def device_status_code(self) -> int:
        """设备状态码。"""
        return self.data.get("device_status_code", 0)

    @property
    @topic_config()
    def deposition_status_code(self) -> int:
        """沉积状态码。"""
        return self.data.get("deposition_status_code", 0)

    @property
    @topic_config()
    def sputter_status_code(self) -> int:
        """溅射状态码。"""
        return self.data.get("sputter_status_code", 0)

    @property
    @topic_config()
    def annealing_status_code(self) -> int:
        """退火状态码。"""
        return self.data.get("annealing_status_code", 0)

    @property
    @topic_config()
    def vacuum_status_code(self) -> float:
        """真空状态码。"""
        return self.data.get("vacuum_status_code", 0.0)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_deposition_temperature(self) -> float:
        """沉积温度实际。"""
        return self.data.get("current_deposition_temperature", 0.0)

    @property
    @topic_config()
    def current_deposition_rate(self) -> float:
        """沉积速率实际。"""
        return self.data.get("current_deposition_rate", 0.0)

    @property
    @topic_config()
    def current_deposition_time(self) -> float:
        """沉积时间实际。"""
        return self.data.get("current_deposition_time", 0.0)

    @property
    @topic_config()
    def current_sputter_power(self) -> float:
        """溅射功率实际。"""
        return self.data.get("current_sputter_power", 0.0)

    @property
    @topic_config()
    def current_sputter_pressure(self) -> float:
        """溅射气压实际。"""
        return self.data.get("current_sputter_pressure", 0.0)

    @property
    @topic_config()
    def current_annealing_temperature(self) -> float:
        """退火温度实际。"""
        return self.data.get("current_annealing_temperature", 0.0)

    @property
    @topic_config()
    def current_annealing_time(self) -> float:
        """退火时间实际。"""
        return self.data.get("current_annealing_time", 0.0)

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """真空度实际。"""
        return self.data.get("current_vacuum", 0.0)

    @property
    @topic_config()
    def current_ar_gas_flow(self) -> float:
        """Ar气流量实际。"""
        return self.data.get("current_ar_gas_flow", 0.0)

    @property
    @topic_config()
    def current_o2_gas_flow(self) -> float:
        """O2气流量实际。"""
        return self.data.get("current_o2_gas_flow", 0.0)

    @property
    @topic_config()
    def current_n2_gas_flow(self) -> float:
        """N2气流量实际。"""
        return self.data.get("current_n2_gas_flow", 0.0)

    @property
    @topic_config()
    def current_gas_partial_pressure_ratio(self) -> float:
        """气体分压比实际。"""
        return self.data.get("current_gas_partial_pressure_ratio", 0.0)

    @property
    @topic_config()
    def substrate_rotation_speed(self) -> float:
        """基片旋转速度。"""
        return self.data.get("substrate_rotation_speed", 0.0)

    @property
    @topic_config()
    def current_film_thickness(self) -> float:
        """薄膜厚度实际。"""
        return self.data.get("current_film_thickness", 0.0)

    @property
    @topic_config()
    def target_temperature(self) -> float:
        """靶材温度监测。"""
        return self.data.get("target_temperature", 0.0)

    @property
    @topic_config()
    def substrate_temperature(self) -> float:
        """基片温度监测。"""
        return self.data.get("substrate_temperature", 0.0)

    @property
    @topic_config()
    def current_rf_power(self) -> float:
        """射频功率实际。"""
        return self.data.get("current_rf_power", 0.0)
