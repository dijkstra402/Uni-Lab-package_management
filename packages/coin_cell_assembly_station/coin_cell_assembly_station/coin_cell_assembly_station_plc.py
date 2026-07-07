"""
纽扣电池组装工站 — PLC(OPC UA) 交互驱动 (自动生成，请勿手改)

由 generate_plc_drivers.py 依据 device_templates_actions.csv 生成。
继承 OpcUaClientWithSubscription，把「纽扣电池组装工站」标准动作/属性映射为 PLC 节点读写：
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
    id="coin_cell_assembly_station_plc",
    category=["纽扣电池组装工站"],
    description="纽扣电池组装工站 PLC(OPC UA) 交互驱动：动作映射为节点读写。",
    display_name="纽扣电池组装工站(PLC)",
)
class CoinCellAssemblyStationPLC(OpcUaClientWithSubscription):

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

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化：写 Initialize_Trigger 触发，等待 Initialize_Complete 完成后复位。"""
        logger.info("初始化...")
        self.set_node_value("Initialize_Trigger", True)
        if not self._wait_until_true("Initialize_Complete", description="初始化完成"):
            raise ValueError("初始化失败：动作未完成")
        self.set_node_value("Initialize_Trigger", False)
        if not self._wait_until_false("Initialize_Complete", description="初始化完成复位"):
            raise ValueError("初始化失败：完成状态复位超时")
        return {"success": True, "message": "初始化完成"}

    @action(description="设置电解液使用瓶数")
    def set_electrolyte_bottle_count(self, electrolyte_bottle_count: int = 0) -> Dict[str, Any]:
        """设置电解液使用瓶数：写入设定值节点 Electrolyte_Bottle_Count_Setpoint。"""
        self.set_node_value("Electrolyte_Bottle_Count_Setpoint", electrolyte_bottle_count)
        return {"success": True, "message": "设置电解液使用瓶数已下发", "electrolyte_bottle_count": electrolyte_bottle_count}

    @action(description="设置负极片盘数")
    def set_anode_sheet_reels(self, anode_sheet_reels: int = 0) -> Dict[str, Any]:
        """设置负极片盘数：写入设定值节点 Anode_Sheet_Reels_Setpoint。"""
        self.set_node_value("Anode_Sheet_Reels_Setpoint", anode_sheet_reels)
        return {"success": True, "message": "设置负极片盘数已下发", "anode_sheet_reels": anode_sheet_reels}

    @action(description="设置隔膜盘数")
    def set_separator_reels(self, separator_reels: int = 0) -> Dict[str, Any]:
        """设置隔膜盘数：写入设定值节点 Separator_Reels_Setpoint。"""
        self.set_node_value("Separator_Reels_Setpoint", separator_reels)
        return {"success": True, "message": "设置隔膜盘数已下发", "separator_reels": separator_reels}

    @action(description="设置单瓶电解液使用次数")
    def set_electrolyte_uses_per_bottle(self, electrolyte_uses_per_bottle: int = 0) -> Dict[str, Any]:
        """设置单瓶电解液使用次数：写入设定值节点 Electrolyte_Uses_Per_Bottle_Setpoint。"""
        self.set_node_value("Electrolyte_Uses_Per_Bottle_Setpoint", electrolyte_uses_per_bottle)
        return {"success": True, "message": "设置单瓶电解液使用次数已下发", "electrolyte_uses_per_bottle": electrolyte_uses_per_bottle}

    @action(description="设置电解液吸取量")
    def set_electrolyte_draw_volume(self, electrolyte_draw_volume: int = 0) -> Dict[str, Any]:
        """设置电解液吸取量：写入设定值节点 Electrolyte_Draw_Volume_Setpoint。"""
        self.set_node_value("Electrolyte_Draw_Volume_Setpoint", electrolyte_draw_volume)
        return {"success": True, "message": "设置电解液吸取量已下发", "electrolyte_draw_volume": electrolyte_draw_volume}

    @action(description="设置电池组装压制力")
    def set_cell_assembly_press_force(self, cell_assembly_press_force: int = 0) -> Dict[str, Any]:
        """设置电池组装压制力：写入设定值节点 Cell_Assembly_Press_Force_Setpoint。"""
        self.set_node_value("Cell_Assembly_Press_Force_Setpoint", cell_assembly_press_force)
        return {"success": True, "message": "设置电池组装压制力已下发", "cell_assembly_press_force": cell_assembly_press_force}

    @action(description="设置电解液二维码序列号")
    def set_electrolyte_qr_serial(self, electrolyte_qr_serial: str = "") -> Dict[str, Any]:
        """设置电解液二维码序列号：写入设定值节点 Electrolyte_Qr_Serial_Setpoint。"""
        self.set_node_value("Electrolyte_Qr_Serial_Setpoint", electrolyte_qr_serial)
        return {"success": True, "message": "设置电解液二维码序列号已下发", "electrolyte_qr_serial": electrolyte_qr_serial}

    @action(description="设置移液枪排液量")
    def set_pipette_dispense_volume(self, pipette_dispense_volume: int = 0) -> Dict[str, Any]:
        """设置移液枪排液量：写入设定值节点 Pipette_Dispense_Volume_Setpoint。"""
        self.set_node_value("Pipette_Dispense_Volume_Setpoint", pipette_dispense_volume)
        return {"success": True, "message": "设置移液枪排液量已下发", "pipette_dispense_volume": pipette_dispense_volume}

    @action(description="设置极片堆叠方式")
    def set_electrode_stacking_mode(self, electrode_stacking_mode: str = "") -> Dict[str, Any]:
        """设置极片堆叠方式：写入设定值节点 Electrode_Stacking_Mode_Setpoint。"""
        self.set_node_value("Electrode_Stacking_Mode_Setpoint", electrode_stacking_mode)
        return {"success": True, "message": "设置极片堆叠方式已下发", "electrode_stacking_mode": electrode_stacking_mode}

    @action(description="设置电池二维码序列号")
    def set_battery_qr_serial(self, battery_qr_serial: str = "") -> Dict[str, Any]:
        """设置电池二维码序列号：写入设定值节点 Battery_Qr_Serial_Setpoint。"""
        self.set_node_value("Battery_Qr_Serial_Setpoint", battery_qr_serial)
        return {"success": True, "message": "设置电池二维码序列号已下发", "battery_qr_serial": battery_qr_serial}

    @action(description="设置开路电压OK下限值")
    def set_ocv_ok_lower_limit(self, ocv_ok_lower_limit: float = 0.0) -> Dict[str, Any]:
        """设置开路电压OK下限值：写入设定值节点 Ocv_Ok_Lower_Limit_Setpoint。"""
        self.set_node_value("Ocv_Ok_Lower_Limit_Setpoint", ocv_ok_lower_limit)
        return {"success": True, "message": "设置开路电压OK下限值已下发", "ocv_ok_lower_limit": ocv_ok_lower_limit}

    @action(description="设置开路电压OK上限值")
    def set_ocv_ok_upper_limit(self, ocv_ok_upper_limit: float = 0.0) -> Dict[str, Any]:
        """设置开路电压OK上限值：写入设定值节点 Ocv_Ok_Upper_Limit_Setpoint。"""
        self.set_node_value("Ocv_Ok_Upper_Limit_Setpoint", ocv_ok_upper_limit)
        return {"success": True, "message": "设置开路电压OK上限值已下发", "ocv_ok_upper_limit": ocv_ok_upper_limit}

    @action(description="设置10mm正极片厚度")
    def set_cathode_sheet_thickness_10mm(self, cathode_sheet_thickness_10mm: float = 0.0) -> Dict[str, Any]:
        """设置10mm正极片厚度：写入设定值节点 Cathode_Sheet_Thickness_10mm_Setpoint。"""
        self.set_node_value("Cathode_Sheet_Thickness_10mm_Setpoint", cathode_sheet_thickness_10mm)
        return {"success": True, "message": "设置10mm正极片厚度已下发", "cathode_sheet_thickness_10mm": cathode_sheet_thickness_10mm}

    @action(description="设置12mm正极片厚度")
    def set_cathode_sheet_thickness_12mm(self, cathode_sheet_thickness_12mm: float = 0.0) -> Dict[str, Any]:
        """设置12mm正极片厚度：写入设定值节点 Cathode_Sheet_Thickness_12mm_Setpoint。"""
        self.set_node_value("Cathode_Sheet_Thickness_12mm_Setpoint", cathode_sheet_thickness_12mm)
        return {"success": True, "message": "设置12mm正极片厚度已下发", "cathode_sheet_thickness_12mm": cathode_sheet_thickness_12mm}

    @action(description="设置16mm正极片厚度")
    def set_cathode_sheet_thickness_16mm(self, cathode_sheet_thickness_16mm: float = 0.0) -> Dict[str, Any]:
        """设置16mm正极片厚度：写入设定值节点 Cathode_Sheet_Thickness_16mm_Setpoint。"""
        self.set_node_value("Cathode_Sheet_Thickness_16mm_Setpoint", cathode_sheet_thickness_16mm)
        return {"success": True, "message": "设置16mm正极片厚度已下发", "cathode_sheet_thickness_16mm": cathode_sheet_thickness_16mm}

    @action(description="设置铝箔厚度")
    def set_aluminum_foil_thickness(self, aluminum_foil_thickness: float = 0.0) -> Dict[str, Any]:
        """设置铝箔厚度：写入设定值节点 Aluminum_Foil_Thickness_Setpoint。"""
        self.set_node_value("Aluminum_Foil_Thickness_Setpoint", aluminum_foil_thickness)
        return {"success": True, "message": "设置铝箔厚度已下发", "aluminum_foil_thickness": aluminum_foil_thickness}

    @action(description="设置正极壳厚度")
    def set_cathode_case_thickness(self, cathode_case_thickness: float = 0.0) -> Dict[str, Any]:
        """设置正极壳厚度：写入设定值节点 Cathode_Case_Thickness_Setpoint。"""
        self.set_node_value("Cathode_Case_Thickness_Setpoint", cathode_case_thickness)
        return {"success": True, "message": "设置正极壳厚度已下发", "cathode_case_thickness": cathode_case_thickness}

    @action(description="设置平垫厚度")
    def set_flat_washer_thickness(self, flat_washer_thickness: float = 0.0) -> Dict[str, Any]:
        """设置平垫厚度：写入设定值节点 Flat_Washer_Thickness_Setpoint。"""
        self.set_node_value("Flat_Washer_Thickness_Setpoint", flat_washer_thickness)
        return {"success": True, "message": "设置平垫厚度已下发", "flat_washer_thickness": flat_washer_thickness}

    @action(description="设置负极壳厚度")
    def set_anode_case_thickness(self, anode_case_thickness: float = 0.0) -> Dict[str, Any]:
        """设置负极壳厚度：写入设定值节点 Anode_Case_Thickness_Setpoint。"""
        self.set_node_value("Anode_Case_Thickness_Setpoint", anode_case_thickness)
        return {"success": True, "message": "设置负极壳厚度已下发", "anode_case_thickness": anode_case_thickness}

    @action(description="设置弹垫厚度")
    def set_spring_washer_thickness(self, spring_washer_thickness: float = 0.0) -> Dict[str, Any]:
        """设置弹垫厚度：写入设定值节点 Spring_Washer_Thickness_Setpoint。"""
        self.set_node_value("Spring_Washer_Thickness_Setpoint", spring_washer_thickness)
        return {"success": True, "message": "设置弹垫厚度已下发", "spring_washer_thickness": spring_washer_thickness}

    @action(description="设置成品电池厚度")
    def set_finished_cell_thickness(self, finished_cell_thickness: float = 0.0) -> Dict[str, Any]:
        """设置成品电池厚度：写入设定值节点 Finished_Cell_Thickness_Setpoint。"""
        self.set_node_value("Finished_Cell_Thickness_Setpoint", finished_cell_thickness)
        return {"success": True, "message": "设置成品电池厚度已下发", "finished_cell_thickness": finished_cell_thickness}

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

    @action(description="切换手动模式")
    def set_manual_mode(self) -> Dict[str, Any]:
        """切换手动模式：写 Set_Manual_Mode_Trigger 触发，等待 Set_Manual_Mode_Complete 完成后复位。"""
        logger.info("切换手动模式...")
        self.set_node_value("Set_Manual_Mode_Trigger", True)
        if not self._wait_until_true("Set_Manual_Mode_Complete", description="切换手动模式完成"):
            raise ValueError("切换手动模式失败：动作未完成")
        self.set_node_value("Set_Manual_Mode_Trigger", False)
        if not self._wait_until_false("Set_Manual_Mode_Complete", description="切换手动模式完成复位"):
            raise ValueError("切换手动模式失败：完成状态复位超时")
        return {"success": True, "message": "切换手动模式完成"}

    @action(description="切换自动模式")
    def set_auto_mode(self) -> Dict[str, Any]:
        """切换自动模式：写 Set_Auto_Mode_Trigger 触发，等待 Set_Auto_Mode_Complete 完成后复位。"""
        logger.info("切换自动模式...")
        self.set_node_value("Set_Auto_Mode_Trigger", True)
        if not self._wait_until_true("Set_Auto_Mode_Complete", description="切换自动模式完成"):
            raise ValueError("切换自动模式失败：动作未完成")
        self.set_node_value("Set_Auto_Mode_Trigger", False)
        if not self._wait_until_false("Set_Auto_Mode_Complete", description="切换自动模式完成复位"):
            raise ValueError("切换自动模式失败：完成状态复位超时")
        return {"success": True, "message": "切换自动模式完成"}

    @action(description="配方下发")
    def load_recipe(self) -> Dict[str, Any]:
        """配方下发：写 Load_Recipe_Trigger 触发，等待 Load_Recipe_Complete 完成后复位。"""
        logger.info("配方下发...")
        self.set_node_value("Load_Recipe_Trigger", True)
        if not self._wait_until_true("Load_Recipe_Complete", description="配方下发完成"):
            raise ValueError("配方下发失败：动作未完成")
        self.set_node_value("Load_Recipe_Trigger", False)
        if not self._wait_until_false("Load_Recipe_Complete", description="配方下发完成复位"):
            raise ValueError("配方下发失败：完成状态复位超时")
        return {"success": True, "message": "配方下发完成"}

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态（读节点 Status）。"""
        v = self.get_node_value("Status")
        return v if v is not None else ""

    @property
    @topic_config()
    def electrolyte_bottle_count(self) -> int:
        """电解液使用瓶数（读节点 Electrolyte_Bottle_Count）。"""
        v = self.get_node_value("Electrolyte_Bottle_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def electrolyte_uses_per_bottle(self) -> int:
        """单瓶电解液使用次数（读节点 Electrolyte_Uses_Per_Bottle）。"""
        v = self.get_node_value("Electrolyte_Uses_Per_Bottle")
        return v if v is not None else 0

    @property
    @topic_config()
    def electrolyte_draw_volume(self) -> int:
        """电解液吸取量（读节点 Electrolyte_Draw_Volume）。"""
        v = self.get_node_value("Electrolyte_Draw_Volume")
        return v if v is not None else 0

    @property
    @topic_config()
    def electrolyte_qr_serial(self) -> str:
        """电解液二维码序列号（读节点 Electrolyte_Qr_Serial）。"""
        v = self.get_node_value("Electrolyte_Qr_Serial")
        return v if v is not None else ""

    @property
    @topic_config()
    def aluminum_foil_material(self) -> bool:
        """铝箔物料（读节点 Aluminum_Foil_Material）。"""
        v = self.get_node_value("Aluminum_Foil_Material")
        return v if v is not None else False

    @property
    @topic_config()
    def pressing_mode(self) -> bool:
        """压制模式（读节点 Pressing_Mode）。"""
        v = self.get_node_value("Pressing_Mode")
        return v if v is not None else False

    @property
    @topic_config()
    def cathode_weigh(self) -> bool:
        """正极片称重（读节点 Cathode_Weigh）。"""
        v = self.get_node_value("Cathode_Weigh")
        return v if v is not None else False

    @property
    @topic_config()
    def pipette_dispense_volume(self) -> int:
        """移液枪排液量（读节点 Pipette_Dispense_Volume）。"""
        v = self.get_node_value("Pipette_Dispense_Volume")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_cell_cathode_weigh_data(self) -> str:
        """当前电池正极片称重数据（读节点 Current_Cell_Cathode_Weigh_Data）。"""
        v = self.get_node_value("Current_Cell_Cathode_Weigh_Data")
        return v if v is not None else ""

    @property
    @topic_config()
    def current_single_cell_assembly_time(self) -> str:
        """当前单颗电池组装时间（读节点 Current_Single_Cell_Assembly_Time）。"""
        v = self.get_node_value("Current_Single_Cell_Assembly_Time")
        return v if v is not None else ""

    @property
    @topic_config()
    def current_cell_assembly_press_force(self) -> int:
        """当前电池组装压制力（读节点 Current_Cell_Assembly_Press_Force）。"""
        v = self.get_node_value("Current_Cell_Assembly_Press_Force")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_electrolyte_fill_volume(self) -> int:
        """当前电解液加注量（读节点 Current_Electrolyte_Fill_Volume）。"""
        v = self.get_node_value("Current_Electrolyte_Fill_Volume")
        return v if v is not None else 0

    @property
    @topic_config()
    def electrode_stacking_mode(self) -> str:
        """组装参数：极片堆叠方式(7/8)（读节点 Electrode_Stacking_Mode）。"""
        v = self.get_node_value("Electrode_Stacking_Mode")
        return v if v is not None else ""

    @property
    @topic_config()
    def battery_qr_serial(self) -> str:
        """电池二维码序列号（读节点 Battery_Qr_Serial）。"""
        v = self.get_node_value("Battery_Qr_Serial")
        return v if v is not None else ""

    @property
    @topic_config()
    def current_electrolyte_cell_count(self) -> int:
        """当前电极液组装电池数量（读节点 Current_Electrolyte_Cell_Count）。"""
        v = self.get_node_value("Current_Electrolyte_Cell_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_cell_voltage_data(self) -> str:
        """当前电池电压数据（读节点 Current_Cell_Voltage_Data）。"""
        v = self.get_node_value("Current_Cell_Voltage_Data")
        return v if v is not None else ""

    @property
    @topic_config()
    def current_anode_sheet_remaining_reels(self) -> int:
        """当前负极片剩余盘数量（读节点 Current_Anode_Sheet_Remaining_Reels）。"""
        v = self.get_node_value("Current_Anode_Sheet_Remaining_Reels")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_separator_remaining_reels(self) -> int:
        """当前隔膜剩余盘数量（读节点 Current_Separator_Remaining_Reels）。"""
        v = self.get_node_value("Current_Separator_Remaining_Reels")
        return v if v is not None else 0

    @property
    @topic_config()
    def electrolyte_status_code(self) -> int:
        """电解液状态码（读节点 Electrolyte_Status_Code）。"""
        v = self.get_node_value("Electrolyte_Status_Code")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_in_progress_cell_count(self) -> int:
        """当前进行组装电池数量（读节点 Current_In_Progress_Cell_Count）。"""
        v = self.get_node_value("Current_In_Progress_Cell_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def current_completed_cell_count(self) -> int:
        """当前完成组装电池数量（读节点 Current_Completed_Cell_Count）。"""
        v = self.get_node_value("Current_Completed_Cell_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def p_10mm_cathode_sheet_remaining_material_count(self) -> int:
        """10mm正极片剩余物料数量（读节点 P_10mm_Cathode_Sheet_Remaining_Material_Count）。"""
        v = self.get_node_value("P_10mm_Cathode_Sheet_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def p_12mm_cathode_sheet_remaining_material_count(self) -> int:
        """12mm正极片剩余物料数量（读节点 P_12mm_Cathode_Sheet_Remaining_Material_Count）。"""
        v = self.get_node_value("P_12mm_Cathode_Sheet_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def p_16mm_cathode_sheet_remaining_material_count(self) -> int:
        """16mm正极片剩余物料数量（读节点 P_16mm_Cathode_Sheet_Remaining_Material_Count）。"""
        v = self.get_node_value("P_16mm_Cathode_Sheet_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def aluminum_foil_remaining_material_count(self) -> int:
        """铝箔剩余物料数量（读节点 Aluminum_Foil_Remaining_Material_Count）。"""
        v = self.get_node_value("Aluminum_Foil_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def cathode_case_remaining_material_count(self) -> int:
        """正极壳剩余物料数量（读节点 Cathode_Case_Remaining_Material_Count）。"""
        v = self.get_node_value("Cathode_Case_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def flat_washer_remaining_material_count(self) -> int:
        """平垫剩余物料数量（读节点 Flat_Washer_Remaining_Material_Count）。"""
        v = self.get_node_value("Flat_Washer_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def anode_case_remaining_material_count(self) -> int:
        """负极壳剩余物料数量（读节点 Anode_Case_Remaining_Material_Count）。"""
        v = self.get_node_value("Anode_Case_Remaining_Material_Count")
        return v if v is not None else 0

    @property
    @topic_config()
    def spring_washer_remaining_material_count(self) -> int:
        """弹垫剩余物料数量（读节点 Spring_Washer_Remaining_Material_Count）。"""
        v = self.get_node_value("Spring_Washer_Remaining_Material_Count")
        return v if v is not None else 0

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
