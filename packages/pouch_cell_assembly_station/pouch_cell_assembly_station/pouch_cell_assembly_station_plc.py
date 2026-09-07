"""
软包电池组装工站 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「软包电池组装工站」标准动作/属性映射为 PLC 节点读写：
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
    id="pouch_cell_assembly_station_plc",
    category=["器件制备设备", "电池组装设备", "软包电池组装工站"],
    description="软包电池组装工站 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    displayname="软包电池组装工站(PLC)",
)
class PouchCellAssemblyStationPLC(OpcUaClientWithSubscription):

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

    @action(description="设置封装温度")
    def set_packaging_temperature(self, packaging_temperature: float = 0.0) -> Dict[str, Any]:
        """设置封装温度：写入设定值节点 Packaging_Temperature_Setpoint。"""
        self.set_node_value("Packaging_Temperature_Setpoint", packaging_temperature)
        return {"success": True, "message": "设置封装温度已下发", "packaging_temperature": packaging_temperature}

    @action(description="设置封装压力")
    def set_packaging_pressure(self, packaging_pressure: float = 0.0) -> Dict[str, Any]:
        """设置封装压力：写入设定值节点 Packaging_Pressure_Setpoint。"""
        self.set_node_value("Packaging_Pressure_Setpoint", packaging_pressure)
        return {"success": True, "message": "设置封装压力已下发", "packaging_pressure": packaging_pressure}

    @action(description="设置封装时间")
    def set_packaging_time(self, packaging_time: float = 0.0) -> Dict[str, Any]:
        """设置封装时间：写入设定值节点 Packaging_Time_Setpoint。"""
        self.set_node_value("Packaging_Time_Setpoint", packaging_time)
        return {"success": True, "message": "设置封装时间已下发", "packaging_time": packaging_time}

    @action(description="设置热压温度")
    def set_hot_press_temperature(self, hot_press_temperature: float = 0.0) -> Dict[str, Any]:
        """设置热压温度：写入设定值节点 Hot_Press_Temperature_Setpoint。"""
        self.set_node_value("Hot_Press_Temperature_Setpoint", hot_press_temperature)
        return {"success": True, "message": "设置热压温度已下发", "hot_press_temperature": hot_press_temperature}

    @action(description="设置热压压力")
    def set_hot_press_pressure(self, hot_press_pressure: float = 0.0) -> Dict[str, Any]:
        """设置热压压力：写入设定值节点 Hot_Press_Pressure_Setpoint。"""
        self.set_node_value("Hot_Press_Pressure_Setpoint", hot_press_pressure)
        return {"success": True, "message": "设置热压压力已下发", "hot_press_pressure": hot_press_pressure}

    @action(description="设置热压时间")
    def set_hot_press_time(self, hot_press_time: float = 0.0) -> Dict[str, Any]:
        """设置热压时间：写入设定值节点 Hot_Press_Time_Setpoint。"""
        self.set_node_value("Hot_Press_Time_Setpoint", hot_press_time)
        return {"success": True, "message": "设置热压时间已下发", "hot_press_time": hot_press_time}

    @action(description="设置裁切速度")
    def set_cutting_speed(self, cutting_speed: float = 0.0) -> Dict[str, Any]:
        """设置裁切速度：写入设定值节点 Cutting_Speed_Setpoint。"""
        self.set_node_value("Cutting_Speed_Setpoint", cutting_speed)
        return {"success": True, "message": "设置裁切速度已下发", "cutting_speed": cutting_speed}

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """设置真空度：写入设定值节点 Vacuum_Setpoint。"""
        self.set_node_value("Vacuum_Setpoint", vacuum)
        return {"success": True, "message": "设置真空度已下发", "vacuum": vacuum}

    @action(description="设置冷却水温")
    def set_cooling_water_temp(self, cooling_water_temp: float = 0.0) -> Dict[str, Any]:
        """设置冷却水温：写入设定值节点 Cooling_Water_Temp_Setpoint。"""
        self.set_node_value("Cooling_Water_Temp_Setpoint", cooling_water_temp)
        return {"success": True, "message": "设置冷却水温已下发", "cooling_water_temp": cooling_water_temp}

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
    def packaging_process_state(self) -> bool:
        """封装工序状态（读节点 Packaging_Process_State）。"""
        v = self.get_node_value("Packaging_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def cutting_process_state(self) -> bool:
        """裁切工序状态（读节点 Cutting_Process_State）。"""
        v = self.get_node_value("Cutting_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def hot_press_process_state(self) -> bool:
        """热压工序状态（读节点 Hot_Press_Process_State）。"""
        v = self.get_node_value("Hot_Press_Process_State")
        return v if v is not None else False

    @property
    @topic_config()
    def device_ready_state(self) -> bool:
        """设备就绪状态（读节点 Device_Ready_State）。"""
        v = self.get_node_value("Device_Ready_State")
        return v if v is not None else False

    @property
    @topic_config()
    def material_in_place_state(self) -> bool:
        """物料到位状态（读节点 Material_In_Place_State）。"""
        v = self.get_node_value("Material_In_Place_State")
        return v if v is not None else False

    @property
    @topic_config()
    def vacuum_state(self) -> bool:
        """真空状态（读节点 Vacuum_State）。"""
        v = self.get_node_value("Vacuum_State")
        return v if v is not None else False

    @property
    @topic_config()
    def cooling_system_state(self) -> bool:
        """冷却系统状态（读节点 Cooling_System_State）。"""
        v = self.get_node_value("Cooling_System_State")
        return v if v is not None else False

    @property
    @topic_config()
    def device_status_code(self) -> int:
        """设备状态码（读节点 Device_Status_Code）。"""
        v = self.get_node_value("Device_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def packaging_status_code(self) -> int:
        """封装状态码（读节点 Packaging_Status_Code）。"""
        v = self.get_node_value("Packaging_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def cutting_status_code(self) -> int:
        """裁切状态码（读节点 Cutting_Status_Code）。"""
        v = self.get_node_value("Cutting_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def hot_press_status_code(self) -> int:
        """热压状态码（读节点 Hot_Press_Status_Code）。"""
        v = self.get_node_value("Hot_Press_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码（读节点 Fault_Code）。"""
        v = self.get_node_value("Fault_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_packaging_temperature(self) -> float:
        """封装温度实际（读节点 Current_Packaging_Temperature）。"""
        v = self.get_node_value("Current_Packaging_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_packaging_pressure(self) -> float:
        """封装压力实际（读节点 Current_Packaging_Pressure）。"""
        v = self.get_node_value("Current_Packaging_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_packaging_time(self) -> float:
        """封装时间实际（读节点 Current_Packaging_Time）。"""
        v = self.get_node_value("Current_Packaging_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_hot_press_temperature(self) -> float:
        """热压温度实际（读节点 Current_Hot_Press_Temperature）。"""
        v = self.get_node_value("Current_Hot_Press_Temperature")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_hot_press_pressure(self) -> float:
        """热压压力实际（读节点 Current_Hot_Press_Pressure）。"""
        v = self.get_node_value("Current_Hot_Press_Pressure")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_hot_press_time(self) -> float:
        """热压时间实际（读节点 Current_Hot_Press_Time）。"""
        v = self.get_node_value("Current_Hot_Press_Time")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_cutting_speed(self) -> float:
        """裁切速度实际（读节点 Current_Cutting_Speed）。"""
        v = self.get_node_value("Current_Cutting_Speed")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """真空度实际（读节点 Current_Vacuum）。"""
        v = self.get_node_value("Current_Vacuum")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def packaging_mold_position(self) -> float:
        """封装模具位置（读节点 Packaging_Mold_Position）。"""
        v = self.get_node_value("Packaging_Mold_Position")
        return v if v is not None else 0.0

    @property
    @topic_config()
    def current_cooling_water_temp(self) -> float:
        """冷却水温实际（读节点 Current_Cooling_Water_Temp）。"""
        v = self.get_node_value("Current_Cooling_Water_Temp")
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
