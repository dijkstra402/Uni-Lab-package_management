# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: plain HTML/CSS/JavaScript served by the existing Python package-builder CLI; keep the first UI dependency-free.

## Users

实验室自动化开发者和设备集成工程师，在开始品牌通信适配前，从 139 个标准设备模块中选择自己的设备包组成。

## Product Purpose

让用户快速浏览设备分类、选择标准设备模块、确认动作和状态属性合同，并导出可供 `unilab-package-builder init` 使用的项目配置。

## Positioning

它把已校验的 Uni-Lab-OS 设备模块目录直接变成可操作的选配工作台，而不是让用户手写设备 ID 或复制模板。

## Operating Context

首版作为 package-management 仓库中的本地工具运行，目录数据来自仓库内的分类清单和动作合同；生成后的真实通信适配、PLC 点表和验收继续在对应工程内完成。

## Capabilities and Constraints

- 首版提供模块搜索、分类筛选、多选、详情预览、项目元数据编辑和配置 JSON 下载。
- 选择配置必须使用稳定 `device_id`，不能把显示名称作为唯一标识。
- 不在浏览器导入或执行设备 Python；不伪造真实设备状态、PLC NodeId 或动作成功。
- 选配页面需复用 FE 仓库 Uni-Lab 设计系统的仪器青、冷灰工作区、白色表面和等宽数据语言。
- 直连本地生成工程可以作为后续版本，不改变首版导出协议。

## Brand Commitments

继承 `/home/raoyi/uni-lab-fe/DESIGN.md` 和 `.impeccable/design.json` 的“精密仪器台”视觉系统；控制色、状态语义和响应式断点以 FE 设计系统为准。

## Evidence on Hand

- `instrument_category_paths.csv`：139 个设备模块的完整飞书分类路径。
- `device_templates_actions.csv`：设备动作与状态属性合同。
- `unilab_package_builder`：现有静态目录、配置校验和设备包脚手架。

## Product Principles

- 选择先于生成：先让用户看懂模块，再允许导出。
- 合同可见：动作、属性和分类路径必须可检查。
- 稳定可复现：相同选择产生相同 JSON 配置。
- 失败诚实：未实现通信和验收能力不在 UI 中伪造。

## Accessibility & Inclusion

键盘可完成搜索、分类、多选、详情切换和导出；状态不只依赖颜色；页面在 720px 和 600px 以下重排为单列。
