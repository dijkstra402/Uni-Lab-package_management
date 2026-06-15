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
    def gas_gong_ying_state(self) -> bool:
        """气体供应状态。"""
        return self.data.get("gas_gong_ying_state", False)

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
    def vacuum_status_code(self) -> int:
        """真空状态码。"""
        return self.data.get("vacuum_status_code", 0)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)
