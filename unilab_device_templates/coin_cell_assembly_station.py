"""
纽扣电池组装工站 — 标准设备类模板 (Device Class Template)

定义「纽扣电池组装工站」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="coin_cell_assembly_station",
    category=["纽扣电池组装工站"],
    description="纽扣电池组装工站标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="纽扣电池组装工站",
)
class CoinCellAssemblyStation:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "coin_cell_assembly_station"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置电解液使用瓶数")
    def set_electrolyte_bottle_count(self, electrolyte_bottle_count: int = 0) -> Dict[str, Any]:
        """
        设置电解液使用瓶数。

        Args:
            electrolyte_bottle_count[设置电解液使用瓶数]: 设置电解液使用瓶数。
        """
        pass

    @action(description="设置负极片盘数")
    def set_anode_sheet_reels(self, anode_sheet_reels: int = 0) -> Dict[str, Any]:
        """
        设置负极片盘数。

        Args:
            anode_sheet_reels[设置负极片盘数]: 设置负极片盘数。
        """
        pass

    @action(description="设置隔膜盘数")
    def set_separator_reels(self, separator_reels: int = 0) -> Dict[str, Any]:
        """
        设置隔膜盘数。

        Args:
            separator_reels[设置隔膜盘数]: 设置隔膜盘数。
        """
        pass

    @action(description="设置单瓶电解液使用次数")
    def set_electrolyte_uses_per_bottle(self, electrolyte_uses_per_bottle: int = 0) -> Dict[str, Any]:
        """
        设置单瓶电解液使用次数。

        Args:
            electrolyte_uses_per_bottle[设置单瓶电解液使用次数]: 设置单瓶电解液使用次数。
        """
        pass

    @action(description="设置电解液吸取量")
    def set_electrolyte_draw_volume(self, electrolyte_draw_volume: int = 0) -> Dict[str, Any]:
        """
        设置电解液吸取量。

        Args:
            electrolyte_draw_volume[设置电解液吸取量]: 设置电解液吸取量。
        """
        pass

    @action(description="设置电池组装压制力")
    def set_cell_assembly_press_force(self, cell_assembly_press_force: int = 0) -> Dict[str, Any]:
        """
        设置电池组装压制力。

        Args:
            cell_assembly_press_force[设置电池组装压制力]: 设置电池组装压制力。
        """
        pass

    @action(description="设置电解液二维码序列号")
    def set_electrolyte_qr_serial(self, electrolyte_qr_serial: str = "") -> Dict[str, Any]:
        """
        设置电解液二维码序列号。

        Args:
            electrolyte_qr_serial[设置电解液二维码序列号]: 设置电解液二维码序列号。
        """
        pass

    @action(description="设置移液枪排液量")
    def set_pipette_dispense_volume(self, pipette_dispense_volume: int = 0) -> Dict[str, Any]:
        """
        设置移液枪排液量。

        Args:
            pipette_dispense_volume[设置移液枪排液量]: 设置移液枪排液量。
        """
        pass

    @action(description="设置组装参数：极片堆叠方式(7/8)")
    def set_assembly_parameter_electrode_stacking_mode_7_8(self, assembly_parameter_electrode_stacking_mode_7_8: int = 0) -> Dict[str, Any]:
        """
        设置组装参数：极片堆叠方式(7/8)。

        Args:
            assembly_parameter_electrode_stacking_mode_7_8[设置组装参数：极片堆叠方式(7/8)]: 设置组装参数：极片堆叠方式(7/8)。
        """
        pass

    @action(description="设置电池二维码序列号")
    def set_battery_qr_serial(self, battery_qr_serial: str = "") -> Dict[str, Any]:
        """
        设置电池二维码序列号。

        Args:
            battery_qr_serial[设置电池二维码序列号]: 设置电池二维码序列号。
        """
        pass

    @action(description="设置开路电压OK下限值")
    def set_ocv_ok_lower_limit(self, ocv_ok_lower_limit: float = 0.0) -> Dict[str, Any]:
        """
        设置开路电压OK下限值。

        Args:
            ocv_ok_lower_limit[设置开路电压OK下限值]: 设置开路电压OK下限值。
        """
        pass

    @action(description="设置开路电压OK上限值")
    def set_ocv_ok_upper_limit(self, ocv_ok_upper_limit: float = 0.0) -> Dict[str, Any]:
        """
        设置开路电压OK上限值。

        Args:
            ocv_ok_upper_limit[设置开路电压OK上限值]: 设置开路电压OK上限值。
        """
        pass

    @action(description="设置10mm正极片厚度")
    def set_v_10mm_cathode_sheet_thickness(self, v_10mm_cathode_sheet_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置10mm正极片厚度。

        Args:
            v_10mm_cathode_sheet_thickness[设置10mm正极片厚度]: 设置10mm正极片厚度。
        """
        pass

    @action(description="设置12mm正极片厚度")
    def set_v_12mm_cathode_sheet_thickness(self, v_12mm_cathode_sheet_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置12mm正极片厚度。

        Args:
            v_12mm_cathode_sheet_thickness[设置12mm正极片厚度]: 设置12mm正极片厚度。
        """
        pass

    @action(description="设置16mm正极片厚度")
    def set_v_16mm_cathode_sheet_thickness(self, v_16mm_cathode_sheet_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置16mm正极片厚度。

        Args:
            v_16mm_cathode_sheet_thickness[设置16mm正极片厚度]: 设置16mm正极片厚度。
        """
        pass

    @action(description="设置铝箔厚度")
    def set_aluminum_foil_thickness(self, aluminum_foil_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置铝箔厚度。

        Args:
            aluminum_foil_thickness[设置铝箔厚度]: 设置铝箔厚度。
        """
        pass

    @action(description="设置正极壳厚度")
    def set_cathode_case_thickness(self, cathode_case_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置正极壳厚度。

        Args:
            cathode_case_thickness[设置正极壳厚度]: 设置正极壳厚度。
        """
        pass

    @action(description="设置平垫厚度")
    def set_flat_washer_thickness(self, flat_washer_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置平垫厚度。

        Args:
            flat_washer_thickness[设置平垫厚度]: 设置平垫厚度。
        """
        pass

    @action(description="设置负极壳厚度")
    def set_anode_case_thickness(self, anode_case_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置负极壳厚度。

        Args:
            anode_case_thickness[设置负极壳厚度]: 设置负极壳厚度。
        """
        pass

    @action(description="设置弹垫厚度")
    def set_spring_washer_thickness(self, spring_washer_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置弹垫厚度。

        Args:
            spring_washer_thickness[设置弹垫厚度]: 设置弹垫厚度。
        """
        pass

    @action(description="设置成品电池厚度")
    def set_finished_cell_thickness(self, finished_cell_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置成品电池厚度。

        Args:
            finished_cell_thickness[设置成品电池厚度]: 设置成品电池厚度。
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

    @action(description="切换手动模式")
    def set_manual_mode(self) -> Dict[str, Any]:
        """切换手动模式。"""
        pass

    @action(description="切换自动模式")
    def set_auto_mode(self) -> Dict[str, Any]:
        """切换自动模式。"""
        pass

    @action(description="配方下发")
    def load_recipe(self) -> Dict[str, Any]:
        """配方下发。"""
        pass

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态。"""
        return self.data.get("status", "idle")

    @property
    @topic_config()
    def current_cell_cathode_weigh_data(self) -> str:
        """当前电池正极片称重数据。"""
        return self.data.get("current_cell_cathode_weigh_data", "")

    @property
    @topic_config()
    def current_single_cell_assembly_time(self) -> str:
        """当前单颗电池组装时间。"""
        return self.data.get("current_single_cell_assembly_time", "")

    @property
    @topic_config()
    def current_cell_assembly_press_force(self) -> int:
        """当前电池组装压制力。"""
        return self.data.get("current_cell_assembly_press_force", 0)

    @property
    @topic_config()
    def current_electrolyte_fill_volume(self) -> int:
        """当前电解液加注量。"""
        return self.data.get("current_electrolyte_fill_volume", 0)

    @property
    @topic_config()
    def current_electrolyte_cell_count(self) -> int:
        """当前电极液组装电池数量。"""
        return self.data.get("current_electrolyte_cell_count", 0)

    @property
    @topic_config()
    def current_cell_voltage_data(self) -> str:
        """当前电池电压数据。"""
        return self.data.get("current_cell_voltage_data", "")

    @property
    @topic_config()
    def current_anode_sheet_remaining_reels(self) -> int:
        """当前负极片剩余盘数量。"""
        return self.data.get("current_anode_sheet_remaining_reels", 0)

    @property
    @topic_config()
    def current_separator_remaining_reels(self) -> int:
        """当前隔膜剩余盘数量。"""
        return self.data.get("current_separator_remaining_reels", 0)

    @property
    @topic_config()
    def electrolyte_status_code(self) -> int:
        """电解液状态码。"""
        return self.data.get("electrolyte_status_code", 0)

    @property
    @topic_config()
    def current_in_progress_cell_count(self) -> int:
        """当前进行组装电池数量。"""
        return self.data.get("current_in_progress_cell_count", 0)

    @property
    @topic_config()
    def current_completed_cell_count(self) -> int:
        """当前完成组装电池数量。"""
        return self.data.get("current_completed_cell_count", 0)
