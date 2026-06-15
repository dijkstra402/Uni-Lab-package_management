# Uni-Lab-OS 设备大类标准模板集

基于 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 的 Uni-Lab-OS 外部设备包。

每个设备**大类**一个 device template，预先定义好统一的动作(`@action`)与状态属性(`@property`)。
方法体为 `pass`（占位）——同一大类下不同品牌的设备继承本模板并填入真实实现，即可让**一套工作流跨品牌控制整类设备**。

## 已收录设备大类 (18)

| 设备大类 | device id |
|---------|-----------|
| 蠕动泵 | `peristaltic_pump` |
| 注射泵 | `syringe_pump` |
| 多通阀 | `multiway_valve` |
| 低温或冷冻离心机 | `refrigerated_centrifuge` |
| 旋转蒸发器 | `rotary_evaporator` |
| 制备色谱仪 | `preparative_chromatograph` |
| 控温磁力搅拌器 | `temperature_controlled_magnetic_stirrer` |
| 光化学反应器 | `photochemical_reactor` |
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

## 本地验证

```bash
unilab --check_mode --devices ./unilab_device_templates --external_devices_only
```

## 为某品牌实现

1. 继承对应标准类，在子类中以同名 `@action` / `@property` 覆盖；
2. 方法体内填入该品牌真实通信逻辑（替换 `pass`）；
3. 保持动作名 / 参数名 / 属性名不变，确保跨品牌工作流兼容。

## License

MIT
