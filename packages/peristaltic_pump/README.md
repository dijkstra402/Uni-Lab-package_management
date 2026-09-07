# 蠕动泵 — 标准设备类模板

基于 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 的 Uni-Lab-OS 外部设备包。

定义「蠕动泵」这一设备**大类**的标准动作(`@action`)与状态属性(`@property`)。
未实现动作明确抛出 `NotImplementedError`——同一大类下不同品牌的设备继承本模板并填入真实实现，
即可让**一套工作流跨品牌控制整类设备**。

## 结构

```
peristaltic_pump/
├── pyproject.toml
├── requirements.txt
├── .github/workflows/check_registry.yml
└── peristaltic_pump/
    ├── __init__.py
    └── peristaltic_pump.py        # 蠕动泵 标准类定义
```

## 本地验证

```bash
unilab --check_mode --devices ./peristaltic_pump --external_devices_only
```

## License

MIT
