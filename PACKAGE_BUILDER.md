# 设备包选择与开发工程

## 目标

本仓库同时维护 139 个标准设备模块和 `unilab-package-builder`。用户通过一个 JSON 配置选择
设备模块，工具生成一个独立、可安装、可被 Uni-Lab-OS 静态 Registry 检查的设备包工程。

设备包工程是领域实现的唯一所有者：设备类、动作、状态、通信适配器、资源、工作流和领域资产
都留在生成后的设备包中。Uni-Lab-OS 只提供已发布的 Registry、包目录、工作区和调度接口；
PLC-Sim/自动化验收包只通过 OPC UA、HTTP 或安装后的公开包接口提供仿真与验收，不导入本仓库
或生成包的内部源码。

## 选择模块

```bash
python -m unilab_package_builder list --format table
python -m unilab_package_builder list --category '合成制备仪器与设备 > 反应器'
python -m unilab_package_builder list --query '反应釜' --format json
```

也可以启动本地无依赖选配 UI，在浏览器中搜索、筛选、查看合同并导出配置：

```bash
python -m unilab_package_builder ui
# 打开 http://127.0.0.1:8765
```

UI 继承 Uni-Lab FE 的“精密仪器台”设计系统：冷灰工作区、仪器青主操作色、白色结构表面、
等宽设备数据和 720px / 600px 响应式降级。页面只读取本地模块目录，不在浏览器执行设备源码。

## 生成设备包

复制 `package_builder.example.json`，修改发行名称、导入包名称和 `modules`，然后运行：

```bash
python -m unilab_package_builder validate --config ./my-package.json
python -m unilab_package_builder init \
  --config ./my-package.json \
  --out ./my-lab-devices
```

也可以直接重复传入 `--module`，不创建配置文件：

```bash
python -m unilab_package_builder init \
  --package-name my_lab_devices \
  --module reactor_kettle \
  --module syringe_pump \
  --out ./my-lab-devices
```

输出工程包含：

- `pyproject.toml`：Python 3.11、`unilabos>=0.11.3` 和 setuptools 包发现配置；
- `package.yaml`：当前 OS 包清单，工作流可在后续开发阶段登记；
- `<package>/devices/<module>.py`：选中模块的标准设备接口；
- `device_selection.json`：不含物理 NodeId 的选择快照，供后续验收工程生成协议覆盖；
- `README.md`：编辑、Registry 检查、PackageCatalog inspect/build 命令。

生成后的标准动作未实现时会抛出 `NotImplementedError`。这保证脚手架不会把占位动作报告为
成功；真正的供应商通信和状态转换必须由设备包开发者实现并在仿真、软 PLC 或真机环境分别验收。

## 两个工程的接缝

1. **设备包工程**：从本工具选择模块，完成 OS 设备类、动作、状态、资源和工作流开发；
   使用 OS v2 的 `unilab --check_mode --devices <package> --external_devices_only` 和
   `unilab package inspect/build` 校验。
2. **自动验收工程**：在 PLC-Sim `automation-acceptance` 中为具体项目声明逻辑变量、点表映射、
   用例、环境和证据等级。用例只引用逻辑变量，通过公开 OPC UA/HTTP 进程验证设备包可观察行为，
   不把 NodeId、PLC 完成位或库存状态复制进设备包选择配置。

当前仓库实现的是第一个工程的可执行选择与脚手架闭环；PLC-Sim 的通用 139 模块验收矩阵仍需在
其 owning branch 中按供应商点表逐项补齐，不能由本工具猜测物理地址或完成条件。
