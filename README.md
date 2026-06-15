# Uni-Lab-OS 设备大类标准模板集

基于 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 的 Uni-Lab-OS 外部设备包。

每个设备**大类**一个 device template，预先定义好统一的动作(`@action`)与状态属性(`@property`)。
方法体为 `pass`（占位）——同一大类下不同品牌的设备继承本模板并填入真实实现，即可让**一套工作流跨品牌控制整类设备**。

## 已收录设备大类 (139)

| 设备大类 | device id |
|---------|-----------|
| 冷藏箱 | `refrigerator` |
| 冷冻箱 | `freezer` |
| 冷冻冷藏箱 | `fridge_freezer` |
| 低温冰箱 | `low_temp_freezer` |
| 超低温冰箱 | `ultra_low_temp_freezer` |
| 深低温冰箱 | `deep_low_temp_freezer` |
| 血液柜 | `blood_bank_refrigerator` |
| 药品柜 | `pharmacy_refrigerator` |
| 疫苗柜 | `vaccine_refrigerator` |
| 食品柜 | `food_refrigerator` |
| 高温金属浴 | `high_temp_metal_bath` |
| 高低温金属浴 | `high_low_temp_metal_bath` |
| 振荡金属浴 | `shaking_metal_bath` |
| 干体温度校正炉 | `dry_block_temp_calibrator` |
| 砂浴 | `sand_bath` |
| 黑体辐射源 | `blackbody_radiation_source` |
| 高温恒温槽 | `high_temp_thermostatic_bath` |
| 高低温恒温槽 | `high_low_temp_thermostatic_bath` |
| 低温恒温槽 | `low_temp_thermostatic_bath` |
| 振荡恒温槽 | `shaking_thermostatic_bath` |
| 透明视窗恒温槽 | `transparent_window_thermostatic_bath` |
| 温度检定恒温槽 | `temp_verification_thermostatic_bath` |
| 管式炉 | `tube_furnace` |
| 箱式电阻炉 | `box_resistance_furnace` |
| 高频感应炉 | `high_freq_induction_furnace` |
| 电热干燥箱 | `electric_drying_oven` |
| 电热鼓风干燥箱 | `forced_air_drying_oven` |
| 真空干燥箱 | `vacuum_drying_oven` |
| 气体保护干燥箱 | `gas_protection_drying_oven` |
| 电烤箱 | `electric_oven` |
| 蒸箱 | `steam_oven` |
| 微波炉 | `microwave_oven` |
| 反应釜 | `reactor_kettle` |
| 塔式反应器 | `tower_reactor` |
| 管式反应器 | `tubular_reactor` |
| 床层反应器 | `bed_reactor` |
| 固定床反应器 | `fixed_bed_reactor` |
| 流化床反应器 | `fluidized_bed_reactor` |
| 微通道反应器 | `microchannel_reactor` |
| 微波合成反应仪 | `microwave_synthesis_reactor` |
| 组合合成反应仪 | `combinatorial_synthesis_reactor` |
| 合成反应仪 | `synthesis_reactor` |
| 机械搅拌反应釜 | `mechanical_stirred_reactor` |
| 并行反应仪 | `parallel_reactor` |
| 催化剂评价装置 | `catalyst_evaluation_unit` |
| 光化学反应器 | `photochemical_reactor` |
| 电化学反应器 | `electrochemical_reactor` |
| 高压反应器 | `high_pressure_reactor` |
| 固体称量工作站 | `solid_weighing_station` |
| 顶置失重固体投料模块 | `overhead_loss_in_weight_feeder` |
| 振动固体加料模块 | `vibratory_solid_feeder` |
| 蠕动泵 | `peristaltic_pump` |
| 恒流泵 | `constant_flow_pump` |
| 柱塞泵 | `plunger_pump` |
| 注射泵 | `syringe_pump` |
| 真空泵 | `vacuum_pump` |
| 多通阀 | `multiway_valve` |
| 电磁开关阀 | `solenoid_on_off_valve` |
| 电磁三通阀 | `solenoid_three_way_valve` |
| 一体化配粉配液站 | `integrated_powder_liquid_station` |
| 投料反应站 | `charging_reaction_station` |
| 移液器 | `pipette` |
| 移液工作站 | `liquid_handling_workstation` |
| 自动滴定仪 | `auto_titrator` |
| 真空吸液系统 | `vacuum_aspiration_system` |
| 开关盖加液模块 | `cap_and_dispense_module` |
| 封膜仪 | `plate_sealer` |
| 撕膜仪 | `plate_peeler` |
| 离心机 | `centrifuge` |
| 低温或冷冻离心机 | `refrigerated_centrifuge` |
| 电泳仪 | `electrophoresis_device` |
| 过滤器 | `filter` |
| 冷冻干燥机 | `freeze_dryer` |
| 喷雾干燥机 | `spray_dryer` |
| 喷雾沉淀装置 | `spray_precipitation_unit` |
| 微波萃取设备 | `microwave_extractor` |
| 抽提萃取设备 | `solvent_extractor` |
| 固相萃取设备 | `solid_phase_extractor` |
| 超声波萃取设备 | `ultrasonic_extractor` |
| 索氏提取仪 | `soxhlet_extractor` |
| 超临界萃取设备 | `supercritical_extractor` |
| 离心萃取机 | `centrifugal_extractor` |
| 大气采样器 | `air_sampler` |
| 熔样机 | `sample_fusion_machine` |
| 磨样机 | `sample_grinder` |
| 抛光机 | `polishing_machine` |
| 磨抛机 | `grinding_polishing_machine` |
| 切割机 | `cutting_machine` |
| 切片机 | `microtome` |
| 压片机 | `tablet_press` |
| 镶嵌机 | `mounting_press` |
| 等离子体表面处理机 | `plasma_surface_treater` |
| 均胶机 | `spin_coater` |
| 自动涂布机 | `auto_coater` |
| 蒸馏器 | `distiller` |
| 旋转蒸发器 | `rotary_evaporator` |
| 氮吹仪 | `nitrogen_evaporator` |
| 真空离心浓缩仪 | `vacuum_centrifugal_concentrator` |
| 高压消毒机 | `autoclave_sterilizer` |
| 化学消毒机 | `chemical_sterilizer` |
| 紫外消毒机 | `uv_sterilizer` |
| 臭氧消毒机 | `ozone_sterilizer` |
| 电热消解仪 | `electric_digester` |
| 微波消解仪 | `microwave_digester` |
| 振荡器（非恒温） | `shaker` |
| 涡旋混匀仪 | `vortex_mixer` |
| 控温磁力搅拌器 | `temperature_controlled_magnetic_stirrer` |
| 机械搅拌器 | `overhead_stirrer` |
| 热混匀仪 | `thermomixer` |
| 分散机 | `disperser` |
| 均质器 | `homogenizer` |
| 匀浆机 | `blender_homogenizer` |
| 超声波清洗机 | `ultrasonic_cleaner` |
| 喷淋式清洗机 | `spray_washer` |
| 蒸汽清洗机 | `steam_cleaner` |
| 激光清洗机 | `laser_cleaner` |
| 干冰清洗机 | `dry_ice_cleaner` |
| 等离子体清洗机 | `plasma_cleaner` |
| 复合型清洗机 | `composite_cleaner` |
| 打粉机 | `pulverizer` |
| 球磨机 | `ball_mill` |
| 粉碎机 | `crusher` |
| 组织破碎机 | `tissue_disruptor` |
| 超声破碎仪 | `ultrasonic_disruptor` |
| 纯水设备 | `pure_water_system` |
| 蒸馏水设备 | `distilled_water_system` |
| 凝胶渗透净化系统 | `gpc_cleanup_system` |
| 凝胶色谱净化系统 | `gel_chromatography_cleanup_system` |
| 制备色谱仪 | `preparative_chromatograph` |
| 气体净化机 | `gas_purifier` |
| 组织研磨仪 | `tissue_grinder` |
| 研磨机 | `grinder` |
| 电子束刻蚀系统 | `electron_beam_etching_system` |
| 纽扣电池组装工站 | `coin_cell_assembly_station` |
| 软包电池组装工站 | `pouch_cell_assembly_station` |
| 模具电池组装工站 | `mold_cell_assembly_station` |
| 薄膜电池组装工站 | `thin_film_cell_assembly_station` |
| 化学气相沉积设备 | `cvd_system` |
| 蒸镀仪 | `evaporation_coater` |

## 本地验证

```bash
unilab --check_mode --devices ./unilab_device_templates --external_devices_only
```

## License

MIT
