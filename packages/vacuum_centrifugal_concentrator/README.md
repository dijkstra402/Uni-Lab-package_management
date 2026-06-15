# 真空离心浓缩仪 — 标准设备类模板

基于 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 的 Uni-Lab-OS 外部设备包。

定义「真空离心浓缩仪」这一设备**大类**的标准动作(`@action`)与状态属性(`@property`)。
方法体为 `pass`（占位）——同一大类下不同品牌的设备继承本模板并填入真实实现，
即可让**一套工作流跨品牌控制整类设备**。

## 结构

```
vacuum_centrifugal_concentrator/
├── pyproject.toml
├── requirements.txt
├── .github/workflows/check_registry.yml
└── vacuum_centrifugal_concentrator/
    ├── __init__.py
    └── vacuum_centrifugal_concentrator.py        # 真空离心浓缩仪 标准类定义
```

## 本地验证

```bash
unilab --check_mode --devices ./vacuum_centrifugal_concentrator --external_devices_only
```

## License

MIT
