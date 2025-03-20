"""配置模块。

此模块负责管理项目的配置信息。
"""

from typing import Any, Dict, Optional
import os
from pathlib import Path

from ..utils import load_json, save_json

__all__ = ["Config"]


class Config:
    """配置管理类。

    用于加载、保存和管理项目配置。

    Attributes:
        config_path: 配置文件路径
        _config: 配置数据字典
    """

    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器。

        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        if config_path is None:
            config_path = os.path.join(
                str(Path.home()),
                ".{{cookiecutter.package_name}}",
                "config.json"
            )
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件。

        如果配置文件不存在，则创建默认配置。
        """
        try:
            self._config = load_json(self.config_path)
        except FileNotFoundError:
            self._config = self._create_default_config()
            self.save()

    def _create_default_config(self) -> Dict[str, Any]:
        """创建默认配置。

        Returns:
            默认配置字典
        """
        return {
            "version": "{{cookiecutter.version}}",
            "log_level": "INFO",
            "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "log_file": None
        }

    def save(self) -> None:
        """保存当前配置到文件。"""
        save_json(self._config, self.config_path)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项。

        Args:
            key: 配置项键名
            default: 默认值，当配置项不存在时返回

        Returns:
            配置项的值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """设置配置项。

        Args:
            key: 配置项键名
            value: 配置项的值
        """
        self._config[key] = value

    def update(self, config_dict: Dict[str, Any]) -> None:
        """更新多个配置项。

        Args:
            config_dict: 包含配置项的字典
        """
        self._config.update(config_dict)

    @property
    def all(self) -> Dict[str, Any]:
        """获取所有配置项。

        Returns:
            包含所有配置项的字典
        """
        return self._config.copy() 