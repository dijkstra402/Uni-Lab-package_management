# 固定床反应器 — 标准设备类模板

基于 [LabDeviceTemplate](https://github.com/Xuwznln/LabDeviceTemplate) 的 Uni-Lab-OS 外部设备包。

定义「固定床反应器」这一设备**大类**的标准动作(`@action`)与状态属性(`@property`)。
未实现动作明确抛出 `NotImplementedError`——同一大类下不同品牌的设备继承本模板并填入真实实现，
即可让**一套工作流跨品牌控制整类设备**。

## 结构

```
fixed_bed_reactor/
├── pyproject.toml
├── requirements.txt
├── .github/workflows/check_registry.yml
└── fixed_bed_reactor/
    ├── __init__.py
    └── fixed_bed_reactor.py        # 固定床反应器 标准类定义
```

## 本地验证

```bash
unilab --check_mode --devices ./fixed_bed_reactor --external_devices_only
```

## License

MIT
