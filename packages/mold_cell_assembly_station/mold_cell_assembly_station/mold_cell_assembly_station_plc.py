"""
模具电池组装工站 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「模具电池组装工站」标准动作/属性映射为 PLC 节点读写：
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
    id="mold_cell_assembly_station_plc",
    category=["模具电池组装工站"],
    description="模具电池组装工站 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="模具电池组装工站(PLC)",
)
class MoldCellAssemblyStationPLC(OpcUaClientWithSubscription):

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

    @action(description="设置模具温度")
    def set_mold_temperature(self, mold_temperature: float = 0.0) -> Dict[str, Any]:
        """设置模具温度：写入设定值节点 Mold_Temperature_Setpoint。"""
        self.set_node_value("Mold_Temperature_Setpoint", mold_temperature)
        return {"success": True, "message": "设置模具温度已下发", "mold_temperature": mold_temperature}

    @action(description="设置注塑压力")
    def set_injection_pressure(self, injection_pressure: float = 0.0) -> Dict[str, Any]:
        """设置注塑压力：写入设定值节点 Injection_Pressure_Setpoint。"""
        self.set_node_value("Injection_Pressure_Setpoint", injection_pressure)
        return {"success": True, "message": "设置注塑压力已下发", "injection_pressure": injection_pressure}

    @action(description="设置注塑速度")
    def set_injection_speed(self, injection_speed: float = 0.0) -> Dict[str, Any]:
        """设置注塑速度：写入设定值节点 Injection_Speed_Setpoint。"""
        self.set_node_value("Injection_Speed_Setpoint", injection_speed)
        return {"success": True, "message": "设置注塑速度已下发", "injection_speed": injection_speed}

    @action(description="设置保压压力")
    def set_holding_pressure(self, holding_pressure: float = 0.0) -> Dict[str, Any]:
        """设置保压压力：写入设定值节点 Holding_Pressure_Setpoint。"""
        self.set_node_value("Holding_Pressure_Setpoint", holding_pressure)
        return {"success": True, "message": "设置保压压力已下发", "holding_pressure": holding_pressure}

    @action(description="设置保压时间")
    def set_holding_time(self, holding_time: float = 0.0) -> Dict[str, Any]:
        """设置保压时间：写入设定值节点 Holding_Time_Setpoint。"""
        self.set_node_value("Holding_Time_Setpoint", holding_time)
        return {"success": True, "message": "设置保压时间已下发", "holding_time": holding_time}

    @action(description="设置冷却时间")
    def set_cooling_time(self, cooling_time: float = 0.0) -> Dict[str, Any]:
        """设置冷却时间：写入设定值节点 Cooling_Time_Setpoint。"""
        self.set_node_value("Cooling_Time_Setpoint", cooling_time)
        return {"success": True, "message": "设置冷却时间已下发", "cooling_time": cooling_time}

    @action(description="设置预热温度")
    def set_preheat_temperature(self, preheat_temperature: float = 0.0) -> Dict[str, Any]:
        """设置预热温度：写入设定值节点 Preheat_Temperature_Setpoint。"""
        self.set_node_value("Preheat_Temperature_Setpoint", preheat_temperature)
        return {"success": True, "message": "设置预热温度已下发", "preheat_temperature": preheat_temperature}

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: float = 0.0) -> Dict[str, Any]:
        """设置加热功率：写入设定值节点 Heating_Power_Setpoint。"""
        self.set_node_value("Heating_Power_Setpoint", heating_power)
        return {"success": True, "message": "设置加热功率已下发", "heating_power": heating_power}

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
    def mold_closed_state(self) -> bool:
        """模具闭合状态（读节点 Mold_Closed_State）。"""
        v = self.get_node_value("Mold_Closed_State")
        return v if v is not None else False

    @property
    @topic_config()
    def injection_process_state(self) -> bool:
        """注塑工序状态（读节点 Injection_Process_State）。"""
        v = self.get_node_value("Injection_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def demold_process_state(self) -> bool:
        """脱模工序状态（读节点 Demold_Process_State）。"""
        v = self.get_node_value("Demold_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def preheat_process_state(self) -> bool:
        """预热工序状态（读节点 Preheat_Process_State）。"""
        v = self.get_node_value("Preheat_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def material_in_place_state(self) -> bool:
        """物料到位状态（读节点 Material_In_Place_State）。"""
        v = self.get_node_value("Material_In_Place_State")
        return v if v is not None else False

    @property
    @topic_config()
    def hydraulic_system_state(self) -> bool:
        """液压系统状态（读节点 Hydraulic_System_State）。"""
        v = self.get_node_value("Hydraulic_System_State")
        return v if v is not None else False

    @property
    @topic_config()
    def heating_system_state(self) -> bool:
        """加热系统状态（读节点 Heating_System_State）。"""
        v = self.get_node_value("Heating_System_State")
        return v if v is not None else False

    @property
    @topic_config()
    def device_status_code(self) -> int:
        """设备状态码（读节点 Device_Status_Code）。"""
        v = self.get_node_value("Device_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def mold_status_code(self) -> int:
        """模具状态码（读节点 Mold_Status_Code）。"""
        v = self.get_node_value("Mold_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def injection_status_code(self) -> int:
        """注塑状态码（读节点 Injection_Status_Code）。"""
        v = self.get_node_value("Injection_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def demold_status_code(self) -> int:
        """脱模状态码（读节点 Demold_Status_Code）。"""
        v = self.get_node_value("Demold_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_mold_temperature(self) -> float:
        """模具温度实际（读节点 Current_Mold_Temperature）。"""
        v = self.get_node_value("Current_Mold_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_injection_pressure(self) -> float:
        """注塑压力实际（读节点 Current_Injection_Pressure）。"""
        v = self.get_node_value("Current_Injection_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_injection_speed(self) -> float:
        """注塑速度实际（读节点 Current_Injection_Speed）。"""
        v = self.get_node_value("Current_Injection_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_holding_pressure(self) -> float:
        """保压压力实际（读节点 Current_Holding_Pressure）。"""
        v = self.get_node_value("Current_Holding_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_holding_time(self) -> float:
        """保压时间实际（读节点 Current_Holding_Time）。"""
        v = self.get_node_value("Current_Holding_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_cooling_time(self) -> float:
        """冷却时间实际（读节点 Current_Cooling_Time）。"""
        v = self.get_node_value("Current_Cooling_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_preheat_temperature(self) -> float:
        """预热温度实际（读节点 Current_Preheat_Temperature）。"""
        v = self.get_node_value("Current_Preheat_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_heating_power(self) -> float:
        """加热功率实际（读节点 Current_Heating_Power）。"""
        v = self.get_node_value("Current_Heating_Power")
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
