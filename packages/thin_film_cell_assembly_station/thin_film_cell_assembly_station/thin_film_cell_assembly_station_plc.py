"""
薄膜电池组装工站 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「薄膜电池组装工站」标准动作/属性映射为 PLC 节点读写：
- 触发类动作：写 <X>_Trigger=True → 等 <X>_Complete=True → 复位 → 等 <X>_Complete=False
- 设定类动作：写 <Param>_Setpoint = 值
- 状态属性：  读对应状态节点
节点均可在设备接入时通过 CSV(NodeId 映射) 注册。
"""

import time
from typing import Any, Dict

from unilabos.registry.decorators import device, action, topic_config
from unilabos.utils.log import logger

from base_opcua_client import OpcUaClientWithSubscription


@device(
    id="thin_film_cell_assembly_station_plc",
    category=["器件制备设备", "电池组装设备", "薄膜电池组装工站"],
    description="薄膜电池组装工站 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="薄膜电池组装工站(PLC)",
)
class ThinFilmCellAssemblyStationPLC(OpcUaClientWithSubscription):

    def __init__(
        self,
        url: str,
        csv_path: str = None,
        username: str = None,
        password: str = None,
        use_subscription: bool = True,
        cache_timeout: float = 5.0,
        subscription_interval: int = 500,
        *args,
        **kwargs,
    ):
        super().__init__(
            url=url,
            username=username,
            password=password,
            use_subscription=use_subscription,
            cache_timeout=cache_timeout,
            subscription_interval=subscription_interval,
            *args,
            **kwargs,
        )
        if csv_path:
            self.load_nodes_from_csv(csv_path)

    @action(description="设置沉积温度")
    def set_deposition_temperature(self, deposition_temperature: float = 0.0) -> Dict[str, Any]:
        """设置沉积温度：写入设定值节点 Deposition_Temperature_Setpoint。"""
        self.set_node_value("Deposition_Temperature_Setpoint", deposition_temperature)
        return {"success": True, "message": "设置沉积温度已下发", "deposition_temperature": deposition_temperature}

    @action(description="设置沉积速率")
    def set_deposition_rate(self, deposition_rate: float = 0.0) -> Dict[str, Any]:
        """设置沉积速率：写入设定值节点 Deposition_Rate_Setpoint。"""
        self.set_node_value("Deposition_Rate_Setpoint", deposition_rate)
        return {"success": True, "message": "设置沉积速率已下发", "deposition_rate": deposition_rate}

    @action(description="设置沉积时间")
    def set_deposition_time(self, deposition_time: float = 0.0) -> Dict[str, Any]:
        """设置沉积时间：写入设定值节点 Deposition_Time_Setpoint。"""
        self.set_node_value("Deposition_Time_Setpoint", deposition_time)
        return {"success": True, "message": "设置沉积时间已下发", "deposition_time": deposition_time}

    @action(description="设置溅射功率")
    def set_sputter_power(self, sputter_power: float = 0.0) -> Dict[str, Any]:
        """设置溅射功率：写入设定值节点 Sputter_Power_Setpoint。"""
        self.set_node_value("Sputter_Power_Setpoint", sputter_power)
        return {"success": True, "message": "设置溅射功率已下发", "sputter_power": sputter_power}

    @action(description="设置溅射气压")
    def set_sputter_pressure(self, sputter_pressure: float = 0.0) -> Dict[str, Any]:
        """设置溅射气压：写入设定值节点 Sputter_Pressure_Setpoint。"""
        self.set_node_value("Sputter_Pressure_Setpoint", sputter_pressure)
        return {"success": True, "message": "设置溅射气压已下发", "sputter_pressure": sputter_pressure}

    @action(description="设置退火温度")
    def set_annealing_temperature(self, annealing_temperature: float = 0.0) -> Dict[str, Any]:
        """设置退火温度：写入设定值节点 Annealing_Temperature_Setpoint。"""
        self.set_node_value("Annealing_Temperature_Setpoint", annealing_temperature)
        return {"success": True, "message": "设置退火温度已下发", "annealing_temperature": annealing_temperature}

    @action(description="设置退火时间")
    def set_annealing_time(self, annealing_time: float = 0.0) -> Dict[str, Any]:
        """设置退火时间：写入设定值节点 Annealing_Time_Setpoint。"""
        self.set_node_value("Annealing_Time_Setpoint", annealing_time)
        return {"success": True, "message": "设置退火时间已下发", "annealing_time": annealing_time}

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """设置真空度：写入设定值节点 Vacuum_Setpoint。"""
        self.set_node_value("Vacuum_Setpoint", vacuum)
        return {"success": True, "message": "设置真空度已下发", "vacuum": vacuum}

    @action(description="设置Ar气流量")
    def set_ar_gas_flow(self, ar_gas_flow: float = 0.0) -> Dict[str, Any]:
        """设置Ar气流量：写入设定值节点 Ar_Gas_Flow_Setpoint。"""
        self.set_node_value("Ar_Gas_Flow_Setpoint", ar_gas_flow)
        return {"success": True, "message": "设置Ar气流量已下发", "ar_gas_flow": ar_gas_flow}

    @action(description="设置O2气流量")
    def set_o2_gas_flow(self, o2_gas_flow: float = 0.0) -> Dict[str, Any]:
        """设置O2气流量：写入设定值节点 O2_Gas_Flow_Setpoint。"""
        self.set_node_value("O2_Gas_Flow_Setpoint", o2_gas_flow)
        return {"success": True, "message": "设置O2气流量已下发", "o2_gas_flow": o2_gas_flow}

    @action(description="设置N2气流量")
    def set_n2_gas_flow(self, n2_gas_flow: float = 0.0) -> Dict[str, Any]:
        """设置N2气流量：写入设定值节点 N2_Gas_Flow_Setpoint。"""
        self.set_node_value("N2_Gas_Flow_Setpoint", n2_gas_flow)
        return {"success": True, "message": "设置N2气流量已下发", "n2_gas_flow": n2_gas_flow}

    @action(description="设置气体分压比")
    def set_gas_partial_pressure_ratio(self, gas_partial_pressure_ratio: float = 0.0) -> Dict[str, Any]:
        """设置气体分压比：写入设定值节点 Gas_Partial_Pressure_Ratio_Setpoint。"""
        self.set_node_value("Gas_Partial_Pressure_Ratio_Setpoint", gas_partial_pressure_ratio)
        return {"success": True, "message": "设置气体分压比已下发", "gas_partial_pressure_ratio": gas_partial_pressure_ratio}

    @action(description="设置薄膜厚度")
    def set_film_thickness(self, film_thickness: float = 0.0) -> Dict[str, Any]:
        """设置薄膜厚度：写入设定值节点 Film_Thickness_Setpoint。"""
        self.set_node_value("Film_Thickness_Setpoint", film_thickness)
        return {"success": True, "message": "设置薄膜厚度已下发", "film_thickness": film_thickness}

    @action(description="设置射频功率")
    def set_rf_power(self, rf_power: float = 0.0) -> Dict[str, Any]:
        """设置射频功率：写入设定值节点 Rf_Power_Setpoint。"""
        self.set_node_value("Rf_Power_Setpoint", rf_power)
        return {"success": True, "message": "设置射频功率已下发", "rf_power": rf_power}

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动：写 Start_Trigger 触发，等待 Start_Complete 完成后复位。"""
        logger.info("启动...")
        self.set_node_value("Start_Trigger", True)
        if not self._wait_until_true("Start_Complete", description="启动完成"):
            raise ValueError("启动失败：动作未完成")
        self.set_node_value("Start_Trigger", False)
        if not self._wait_until_false("Start_Complete", description="启动完成复位"):
            raise ValueError("启动失败：完成状态复位超时")
        return {"success": True, "message": "启动完成"}

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止：写 Stop_Trigger 触发，等待 Stop_Complete 完成后复位。"""
        logger.info("停止...")
        self.set_node_value("Stop_Trigger", True)
        if not self._wait_until_true("Stop_Complete", description="停止完成"):
            raise ValueError("停止失败：动作未完成")
        self.set_node_value("Stop_Trigger", False)
        if not self._wait_until_false("Stop_Complete", description="停止完成复位"):
            raise ValueError("停止失败：完成状态复位超时")
        return {"success": True, "message": "停止完成"}

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位：写 Reset_Trigger 触发，等待 Reset_Complete 完成后复位。"""
        logger.info("复位...")
        self.set_node_value("Reset_Trigger", True)
        if not self._wait_until_true("Reset_Complete", description="复位完成"):
            raise ValueError("复位失败：动作未完成")
        self.set_node_value("Reset_Trigger", False)
        if not self._wait_until_false("Reset_Complete", description="复位完成复位"):
            raise ValueError("复位失败：完成状态复位超时")
        return {"success": True, "message": "复位完成"}

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态（读节点 Status）。"""
        v = self.get_node_value("Status")
        return v if v is not None else ""

    @property
    @topic_config()
    def device_running_state(self) -> bool:
        """设备运行状态（读节点 Device_Running_State）。"""
        v = self.get_node_value("Device_Running_State")
        return v if v is not None else False

    @property
    @topic_config()
    def device_fault_state(self) -> bool:
        """设备故障状态（读节点 Device_Fault_State）。"""
        v = self.get_node_value("Device_Fault_State")
        return v if v is not None else False

    @property
    @topic_config()
    def deposition_process_state(self) -> bool:
        """沉积工序状态（读节点 Deposition_Process_State）。"""
        v = self.get_node_value("Deposition_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def sputter_process_state(self) -> bool:
        """溅射工序状态（读节点 Sputter_Process_State）。"""
        v = self.get_node_value("Sputter_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def annealing_process_state(self) -> bool:
        """退火工序状态（读节点 Annealing_Process_State）。"""
        v = self.get_node_value("Annealing_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def vacuum_system_state(self) -> bool:
        """真空系统状态（读节点 Vacuum_System_State）。"""
        v = self.get_node_value("Vacuum_System_State")
        return v if v is not None else False

    @property
    @topic_config()
    def target_state(self) -> bool:
        """靶材状态（读节点 Target_State）。"""
        v = self.get_node_value("Target_State")
        return v if v is not None else False

    @property
    @topic_config()
    def substrate_in_place_state(self) -> bool:
        """基片到位状态（读节点 Substrate_In_Place_State）。"""
        v = self.get_node_value("Substrate_In_Place_State")
        return v if v is not None else False

    @property
    @topic_config()
    def gas_supply_state(self) -> bool:
        """气体供应状态（读节点 Gas_Supply_State）。"""
        v = self.get_node_value("Gas_Supply_State")
        return v if v is not None else False

    @property
    @topic_config()
    def device_status_code(self) -> int:
        """设备状态码（读节点 Device_Status_Code）。"""
        v = self.get_node_value("Device_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def deposition_status_code(self) -> int:
        """沉积状态码（读节点 Deposition_Status_Code）。"""
        v = self.get_node_value("Deposition_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def sputter_status_code(self) -> int:
        """溅射状态码（读节点 Sputter_Status_Code）。"""
        v = self.get_node_value("Sputter_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def annealing_status_code(self) -> int:
        """退火状态码（读节点 Annealing_Status_Code）。"""
        v = self.get_node_value("Annealing_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def vacuum_status_code(self) -> float:
        """真空状态码（读节点 Vacuum_Status_Code）。"""
        v = self.get_node_value("Vacuum_Status_Code")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_deposition_temperature(self) -> float:
        """沉积温度实际（读节点 Current_Deposition_Temperature）。"""
        v = self.get_node_value("Current_Deposition_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_deposition_rate(self) -> float:
        """沉积速率实际（读节点 Current_Deposition_Rate）。"""
        v = self.get_node_value("Current_Deposition_Rate")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_deposition_time(self) -> float:
        """沉积时间实际（读节点 Current_Deposition_Time）。"""
        v = self.get_node_value("Current_Deposition_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_sputter_power(self) -> float:
        """溅射功率实际（读节点 Current_Sputter_Power）。"""
        v = self.get_node_value("Current_Sputter_Power")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_sputter_pressure(self) -> float:
        """溅射气压实际（读节点 Current_Sputter_Pressure）。"""
        v = self.get_node_value("Current_Sputter_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_annealing_temperature(self) -> float:
        """退火温度实际（读节点 Current_Annealing_Temperature）。"""
        v = self.get_node_value("Current_Annealing_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_annealing_time(self) -> float:
        """退火时间实际（读节点 Current_Annealing_Time）。"""
        v = self.get_node_value("Current_Annealing_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """真空度实际（读节点 Current_Vacuum）。"""
        v = self.get_node_value("Current_Vacuum")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_ar_gas_flow(self) -> float:
        """Ar气流量实际（读节点 Current_Ar_Gas_Flow）。"""
        v = self.get_node_value("Current_Ar_Gas_Flow")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_o2_gas_flow(self) -> float:
        """O2气流量实际（读节点 Current_O2_Gas_Flow）。"""
        v = self.get_node_value("Current_O2_Gas_Flow")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_n2_gas_flow(self) -> float:
        """N2气流量实际（读节点 Current_N2_Gas_Flow）。"""
        v = self.get_node_value("Current_N2_Gas_Flow")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_gas_partial_pressure_ratio(self) -> float:
        """气体分压比实际（读节点 Current_Gas_Partial_Pressure_Ratio）。"""
        v = self.get_node_value("Current_Gas_Partial_Pressure_Ratio")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def substrate_rotation_speed(self) -> float:
        """基片旋转速度（读节点 Substrate_Rotation_Speed）。"""
        v = self.get_node_value("Substrate_Rotation_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_film_thickness(self) -> float:
        """薄膜厚度实际（读节点 Current_Film_Thickness）。"""
        v = self.get_node_value("Current_Film_Thickness")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def target_temperature(self) -> float:
        """靶材温度监测（读节点 Target_Temperature）。"""
        v = self.get_node_value("Target_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def substrate_temperature(self) -> float:
        """基片温度监测（读节点 Substrate_Temperature）。"""
        v = self.get_node_value("Substrate_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_rf_power(self) -> float:
        """射频功率实际（读节点 Current_Rf_Power）。"""
        v = self.get_node_value("Current_Rf_Power")
        return v if v is not None else 0.0

    def _wait_until_true(self, node_name: str, timeout: float = 300.0,
                         interval: float = 0.2, description: str = None) -> bool:
        """等待布尔节点变为 True（强制从服务器读取，避免订阅缓存过期）。"""
        desc = description or node_name
        start = time.time()
        while True:
            if self.get_node_value(node_name, force_read=True):
                return True
            if time.time() - start >= timeout:
                logger.error(f"等待 {desc} 超时（{timeout}秒，节点 {node_name}）")
                return False
            time.sleep(interval)

    def _wait_until_false(self, node_name: str, timeout: float = 300.0,
                          interval: float = 0.2, description: str = None) -> bool:
        """等待布尔节点变为 False（强制从服务器读取）。"""
        desc = description or node_name
        start = time.time()
        while True:
            if not self.get_node_value(node_name, force_read=True):
                return True
            if time.time() - start >= timeout:
                logger.error(f"等待 {desc} 超时（{timeout}秒，节点 {node_name}）")
                return False
            time.sleep(interval)
