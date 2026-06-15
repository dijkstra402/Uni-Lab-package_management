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
