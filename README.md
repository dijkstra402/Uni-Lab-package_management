# Uni-Lab-OS 设备包管理仓库

每个设备**大类**一个**独立设备包**（标准 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 结构）。
每个包都可单独 fork / `pip install -e .` / 上报，预先定义好该大类统一的动作(`@action`)与状态属性(`@property`)，
未实现的方法体会抛出 `NotImplementedError`，避免占位动作误报成功。同一大类下不同品牌的设备继承对应包即可让**一套工作流跨品牌控制整类设备**。

## 包列表 (139)

| 设备大类 | 设备包 |
|---------|--------|
| 冷藏箱 | [`refrigerator`](packages/refrigerator/) |
| 冷冻箱 | [`freezer`](packages/freezer/) |
| 冷冻冷藏箱 | [`fridge_freezer`](packages/fridge_freezer/) |
| 低温冰箱 | [`low_temp_freezer`](packages/low_temp_freezer/) |
| 超低温冰箱 | [`ultra_low_temp_freezer`](packages/ultra_low_temp_freezer/) |
| 深低温冰箱 | [`deep_low_temp_freezer`](packages/deep_low_temp_freezer/) |
| 血液柜 | [`blood_bank_refrigerator`](packages/blood_bank_refrigerator/) |
| 药品柜 | [`pharmacy_refrigerator`](packages/pharmacy_refrigerator/) |
| 疫苗柜 | [`vaccine_refrigerator`](packages/vaccine_refrigerator/) |
| 食品柜 | [`food_refrigerator`](packages/food_refrigerator/) |
| 高温金属浴 | [`high_temp_metal_bath`](packages/high_temp_metal_bath/) |
| 高低温金属浴 | [`high_low_temp_metal_bath`](packages/high_low_temp_metal_bath/) |
| 振荡金属浴 | [`shaking_metal_bath`](packages/shaking_metal_bath/) |
| 干体温度校正炉 | [`dry_block_temp_calibrator`](packages/dry_block_temp_calibrator/) |
| 砂浴 | [`sand_bath`](packages/sand_bath/) |
| 黑体辐射源 | [`blackbody_radiation_source`](packages/blackbody_radiation_source/) |
| 高温恒温槽 | [`high_temp_thermostatic_bath`](packages/high_temp_thermostatic_bath/) |
| 高低温恒温槽 | [`high_low_temp_thermostatic_bath`](packages/high_low_temp_thermostatic_bath/) |
| 低温恒温槽 | [`low_temp_thermostatic_bath`](packages/low_temp_thermostatic_bath/) |
| 振荡恒温槽 | [`shaking_thermostatic_bath`](packages/shaking_thermostatic_bath/) |
| 透明视窗恒温槽 | [`transparent_window_thermostatic_bath`](packages/transparent_window_thermostatic_bath/) |
| 温度检定恒温槽 | [`temp_verification_thermostatic_bath`](packages/temp_verification_thermostatic_bath/) |
| 管式炉 | [`tube_furnace`](packages/tube_furnace/) |
| 箱式电阻炉 | [`box_resistance_furnace`](packages/box_resistance_furnace/) |
| 高频感应炉 | [`high_freq_induction_furnace`](packages/high_freq_induction_furnace/) |
| 电热干燥箱 | [`electric_drying_oven`](packages/electric_drying_oven/) |
| 电热鼓风干燥箱 | [`forced_air_drying_oven`](packages/forced_air_drying_oven/) |
| 真空干燥箱 | [`vacuum_drying_oven`](packages/vacuum_drying_oven/) |
| 气体保护干燥箱 | [`gas_protection_drying_oven`](packages/gas_protection_drying_oven/) |
| 电烤箱 | [`electric_oven`](packages/electric_oven/) |
| 蒸箱 | [`steam_oven`](packages/steam_oven/) |
| 微波炉 | [`microwave_oven`](packages/microwave_oven/) |
| 反应釜 | [`reactor_kettle`](packages/reactor_kettle/) |
| 塔式反应器 | [`tower_reactor`](packages/tower_reactor/) |
| 管式反应器 | [`tubular_reactor`](packages/tubular_reactor/) |
| 床层反应器 | [`bed_reactor`](packages/bed_reactor/) |
| 固定床反应器 | [`fixed_bed_reactor`](packages/fixed_bed_reactor/) |
| 流化床反应器 | [`fluidized_bed_reactor`](packages/fluidized_bed_reactor/) |
| 微通道反应器 | [`microchannel_reactor`](packages/microchannel_reactor/) |
| 微波合成反应仪 | [`microwave_synthesis_reactor`](packages/microwave_synthesis_reactor/) |
| 组合合成反应仪 | [`combinatorial_synthesis_reactor`](packages/combinatorial_synthesis_reactor/) |
| 合成反应仪 | [`synthesis_reactor`](packages/synthesis_reactor/) |
| 机械搅拌反应釜 | [`mechanical_stirred_reactor`](packages/mechanical_stirred_reactor/) |
| 并行反应仪 | [`parallel_reactor`](packages/parallel_reactor/) |
| 催化剂评价装置 | [`catalyst_evaluation_unit`](packages/catalyst_evaluation_unit/) |
| 光化学反应器 | [`photochemical_reactor`](packages/photochemical_reactor/) |
| 电化学反应器 | [`electrochemical_reactor`](packages/electrochemical_reactor/) |
| 高压反应器 | [`high_pressure_reactor`](packages/high_pressure_reactor/) |
| 固体称量工作站 | [`solid_weighing_station`](packages/solid_weighing_station/) |
| 顶置失重固体投料模块 | [`overhead_loss_in_weight_feeder`](packages/overhead_loss_in_weight_feeder/) |
| 振动固体加料模块 | [`vibratory_solid_feeder`](packages/vibratory_solid_feeder/) |
| 蠕动泵 | [`peristaltic_pump`](packages/peristaltic_pump/) |
| 恒流泵 | [`constant_flow_pump`](packages/constant_flow_pump/) |
| 柱塞泵 | [`plunger_pump`](packages/plunger_pump/) |
| 注射泵 | [`syringe_pump`](packages/syringe_pump/) |
| 真空泵 | [`vacuum_pump`](packages/vacuum_pump/) |
| 多通阀 | [`multiway_valve`](packages/multiway_valve/) |
| 电磁开关阀 | [`solenoid_on_off_valve`](packages/solenoid_on_off_valve/) |
| 电磁三通阀 | [`solenoid_three_way_valve`](packages/solenoid_three_way_valve/) |
| 一体化配粉配液站 | [`integrated_powder_liquid_station`](packages/integrated_powder_liquid_station/) |
| 投料反应站 | [`charging_reaction_station`](packages/charging_reaction_station/) |
| 移液器 | [`pipette`](packages/pipette/) |
| 移液工作站 | [`liquid_handling_workstation`](packages/liquid_handling_workstation/) |
| 自动滴定仪 | [`auto_titrator`](packages/auto_titrator/) |
| 真空吸液系统 | [`vacuum_aspiration_system`](packages/vacuum_aspiration_system/) |
| 开关盖加液模块 | [`cap_and_dispense_module`](packages/cap_and_dispense_module/) |
| 封膜仪 | [`plate_sealer`](packages/plate_sealer/) |
| 撕膜仪 | [`plate_peeler`](packages/plate_peeler/) |
| 离心机 | [`centrifuge`](packages/centrifuge/) |
| 低温或冷冻离心机 | [`refrigerated_centrifuge`](packages/refrigerated_centrifuge/) |
| 电泳仪 | [`electrophoresis_device`](packages/electrophoresis_device/) |
| 过滤器 | [`filter`](packages/filter/) |
| 冷冻干燥机 | [`freeze_dryer`](packages/freeze_dryer/) |
| 喷雾干燥机 | [`spray_dryer`](packages/spray_dryer/) |
| 喷雾沉淀装置 | [`spray_precipitation_unit`](packages/spray_precipitation_unit/) |
| 微波萃取设备 | [`microwave_extractor`](packages/microwave_extractor/) |
| 抽提萃取设备 | [`solvent_extractor`](packages/solvent_extractor/) |
| 固相萃取设备 | [`solid_phase_extractor`](packages/solid_phase_extractor/) |
| 超声波萃取设备 | [`ultrasonic_extractor`](packages/ultrasonic_extractor/) |
| 索氏提取仪 | [`soxhlet_extractor`](packages/soxhlet_extractor/) |
| 超临界萃取设备 | [`supercritical_extractor`](packages/supercritical_extractor/) |
| 离心萃取机 | [`centrifugal_extractor`](packages/centrifugal_extractor/) |
| 大气采样器 | [`air_sampler`](packages/air_sampler/) |
| 熔样机 | [`sample_fusion_machine`](packages/sample_fusion_machine/) |
| 磨样机 | [`sample_grinder`](packages/sample_grinder/) |
| 抛光机 | [`polishing_machine`](packages/polishing_machine/) |
| 磨抛机 | [`grinding_polishing_machine`](packages/grinding_polishing_machine/) |
| 切割机 | [`cutting_machine`](packages/cutting_machine/) |
| 切片机 | [`microtome`](packages/microtome/) |
| 压片机 | [`tablet_press`](packages/tablet_press/) |
| 镶嵌机 | [`mounting_press`](packages/mounting_press/) |
| 等离子体表面处理机 | [`plasma_surface_treater`](packages/plasma_surface_treater/) |
| 均胶机 | [`spin_coater`](packages/spin_coater/) |
| 自动涂布机 | [`auto_coater`](packages/auto_coater/) |
| 蒸馏器 | [`distiller`](packages/distiller/) |
| 旋转蒸发器 | [`rotary_evaporator`](packages/rotary_evaporator/) |
| 氮吹仪 | [`nitrogen_evaporator`](packages/nitrogen_evaporator/) |
| 真空离心浓缩仪 | [`vacuum_centrifugal_concentrator`](packages/vacuum_centrifugal_concentrator/) |
| 高压消毒机 | [`autoclave_sterilizer`](packages/autoclave_sterilizer/) |
| 化学消毒机 | [`chemical_sterilizer`](packages/chemical_sterilizer/) |
| 紫外消毒机 | [`uv_sterilizer`](packages/uv_sterilizer/) |
| 臭氧消毒机 | [`ozone_sterilizer`](packages/ozone_sterilizer/) |
| 电热消解仪 | [`electric_digester`](packages/electric_digester/) |
| 微波消解仪 | [`microwave_digester`](packages/microwave_digester/) |
| 振荡器（非恒温） | [`shaker`](packages/shaker/) |
| 涡旋混匀仪 | [`vortex_mixer`](packages/vortex_mixer/) |
| 控温磁力搅拌器 | [`temperature_controlled_magnetic_stirrer`](packages/temperature_controlled_magnetic_stirrer/) |
| 机械搅拌器 | [`overhead_stirrer`](packages/overhead_stirrer/) |
| 热混匀仪 | [`thermomixer`](packages/thermomixer/) |
| 分散机 | [`disperser`](packages/disperser/) |
| 均质器 | [`homogenizer`](packages/homogenizer/) |
| 匀浆机 | [`blender_homogenizer`](packages/blender_homogenizer/) |
| 超声波清洗机 | [`ultrasonic_cleaner`](packages/ultrasonic_cleaner/) |
| 喷淋式清洗机 | [`spray_washer`](packages/spray_washer/) |
| 蒸汽清洗机 | [`steam_cleaner`](packages/steam_cleaner/) |
| 激光清洗机 | [`laser_cleaner`](packages/laser_cleaner/) |
| 干冰清洗机 | [`dry_ice_cleaner`](packages/dry_ice_cleaner/) |
| 等离子体清洗机 | [`plasma_cleaner`](packages/plasma_cleaner/) |
| 复合型清洗机 | [`composite_cleaner`](packages/composite_cleaner/) |
| 打粉机 | [`pulverizer`](packages/pulverizer/) |
| 球磨机 | [`ball_mill`](packages/ball_mill/) |
| 粉碎机 | [`crusher`](packages/crusher/) |
| 组织破碎机 | [`tissue_disruptor`](packages/tissue_disruptor/) |
| 超声破碎仪 | [`ultrasonic_disruptor`](packages/ultrasonic_disruptor/) |
| 纯水设备 | [`pure_water_system`](packages/pure_water_system/) |
| 蒸馏水设备 | [`distilled_water_system`](packages/distilled_water_system/) |
| 凝胶渗透净化系统 | [`gpc_cleanup_system`](packages/gpc_cleanup_system/) |
| 凝胶色谱净化系统 | [`gel_chromatography_cleanup_system`](packages/gel_chromatography_cleanup_system/) |
| 制备色谱仪 | [`preparative_chromatograph`](packages/preparative_chromatograph/) |
| 气体净化机 | [`gas_purifier`](packages/gas_purifier/) |
| 组织研磨仪 | [`tissue_grinder`](packages/tissue_grinder/) |
| 研磨机 | [`grinder`](packages/grinder/) |
| 电子束刻蚀系统 | [`electron_beam_etching_system`](packages/electron_beam_etching_system/) |
| 纽扣电池组装工站 | [`coin_cell_assembly_station`](packages/coin_cell_assembly_station/) |
| 软包电池组装工站 | [`pouch_cell_assembly_station`](packages/pouch_cell_assembly_station/) |
| 模具电池组装工站 | [`mold_cell_assembly_station`](packages/mold_cell_assembly_station/) |
| 薄膜电池组装工站 | [`thin_film_cell_assembly_station`](packages/thin_film_cell_assembly_station/) |
| 化学气相沉积设备 | [`cvd_system`](packages/cvd_system/) |
| 蒸镀仪 | [`evaporation_coater`](packages/evaporation_coater/) |

## 使用某个包

```bash
cd packages/<en_id>
unilab --check_mode --devices ./<en_id> --external_devices_only
```

## 选择模块生成设备包

仓库根目录提供 `unilab-package-builder`，可从 139 个标准模块中选择设备并生成独立的
Uni-Lab-OS 外部设备包：

```bash
python -m unilab_package_builder list --category '合成制备仪器与设备 > 反应器'
python -m unilab_package_builder validate --config ./package_builder.example.json
python -m unilab_package_builder init --config ./package_builder.example.json --out ./my-lab-devices
python -m unilab_package_builder init --package-name my_lab_devices --module reactor_kettle --out ./my-lab-devices
python -m unilab_package_builder ui
```

UI 中的 `生成并下载设备包` 会直接执行 `init` 生成 OS 设备包；相邻的
`生成并下载自动验收包` 会生成遵循 PLC-Sim `automation-acceptance` 目录规范的 L0 合同模板。
完整配置、生成工程结构和 PLC-Sim 自动验收接缝见 [`PACKAGE_BUILDER.md`](PACKAGE_BUILDER.md)。

## License

MIT
