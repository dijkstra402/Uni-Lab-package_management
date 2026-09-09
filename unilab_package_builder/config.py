"""设备包选择配置的解析与校验。"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    """设备包选择配置无效。"""


DRIVER_MODES = ("template", "opcua")


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    """一次设备包生成请求。"""

    distribution_name: str
    package_name: str
    modules: tuple[str, ...]
    version: str = "0.1.0"
    description: str = "Uni-Lab-OS 设备包"
    driver_mode: str = "template"

    def validate(self) -> None:
        """校验发行身份、导入包身份和选择集合。"""

        if not self.distribution_name.strip():
            raise ConfigError("distribution_name 不能为空")
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", self.distribution_name):
            raise ConfigError(f"distribution_name 非法: {self.distribution_name}")
        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", self.package_name):
            raise ConfigError(f"package_name 非法: {self.package_name}")
        if not self.modules:
            raise ConfigError("modules 至少包含一个设备模块")
        if len(set(self.modules)) != len(self.modules):
            raise ConfigError("modules 不允许重复")
        if not re.fullmatch(r"\d+\.\d+\.\d+", self.version):
            raise ConfigError(f"version 必须是三段版本号: {self.version}")
        if self.driver_mode not in DRIVER_MODES:
            choices = ", ".join(DRIVER_MODES)
            raise ConfigError(f"driver_mode 必须是 {choices} 之一: {self.driver_mode}")

    def to_dict(self) -> dict[str, object]:
        """返回可写入生成工程的配置投影。"""

        return {
            "distribution_name": self.distribution_name,
            "package_name": self.package_name,
            "version": self.version,
            "description": self.description,
            "driver_mode": self.driver_mode,
            "modules": list(self.modules),
        }


def load_project_config(path: Path) -> ProjectConfig:
    """从 JSON 读取选择配置。"""

    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ConfigError(f"配置不是合法 JSON: {path}: {error}") from error
    return project_config_from_dict(data)


def project_config_from_dict(data: object) -> ProjectConfig:
    """从已解析的 JSON 对象构造并校验选择配置。"""

    if not isinstance(data, dict):
        raise ConfigError("配置根节点必须是 JSON 对象")
    modules = data.get("modules")
    if not isinstance(modules, list) or not all(isinstance(item, str) for item in modules):
        raise ConfigError("modules 必须是字符串数组")
    package_name = data.get("package_name")
    if not isinstance(package_name, str):
        raise ConfigError("package_name 必填且必须是字符串")
    distribution_name = data.get("distribution_name", package_name)
    if not isinstance(distribution_name, str):
        raise ConfigError("distribution_name 必须是字符串")
    version = data.get("version", "0.1.0")
    description = data.get("description", "Uni-Lab-OS 设备包")
    driver_mode = data.get("driver_mode", "template")
    if not isinstance(version, str) or not isinstance(description, str):
        raise ConfigError("version 和 description 必须是字符串")
    if not isinstance(driver_mode, str):
        raise ConfigError("driver_mode 必须是字符串")
    config = ProjectConfig(
        distribution_name=distribution_name,
        package_name=package_name,
        modules=tuple(modules),
        version=version,
        description=description,
        driver_mode=driver_mode,
    )
    config.validate()
    return config
