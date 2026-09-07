# 软包电池组装工站 — 标准设备类模板

基于 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 的 Uni-Lab-OS 外部设备包。

定义「软包电池组装工站」这一设备**大类**的标准动作(`@action`)与状态属性(`@property`)。
未实现动作明确抛出 `NotImplementedError`——同一大类下不同品牌的设备继承本模板并填入真实实现，
即可让**一套工作流跨品牌控制整类设备**。

## 结构

```
pouch_cell_assembly_station/
├── pyproject.toml
├── requirements.txt
├── .github/workflows/check_registry.yml
└── pouch_cell_assembly_station/
    ├── __init__.py
    └── pouch_cell_assembly_station.py        # 软包电池组装工站 标准类定义
```

## 本地验证

```bash
unilab --check_mode --devices ./pouch_cell_assembly_station --external_devices_only
```

## License

MIT
